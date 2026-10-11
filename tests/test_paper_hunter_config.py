import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "paper-search/scripts/paper_hunter.py"
spec = importlib.util.spec_from_file_location("paper_hunter", SCRIPT)
hunter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hunter)


class HunterConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.env = patch.dict(os.environ, {}, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)

    def config(self, name="research.yaml", **values):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(values), encoding="utf-8")
        return path

    def test_explicit_config_and_vault_override_environment(self):
        config = self.config(vault_path=str(self.root / "yaml-vault"))
        os.environ["RESEARCH_CONFIG_PATH"] = str(self.root / "missing.yaml")
        os.environ["OBSIDIAN_VAULT_PATH"] = str(self.root / "env-vault")
        hunter.configure(str(config), str(self.root / "chosen vault"), "Research/Papers")
        self.assertEqual(hunter.PAPERS_DIR, self.root / "chosen vault/Research/Papers")
        self.assertFalse(hunter.VAULT_PATH.exists())

    def test_environment_config_and_vault_work_outside_repository(self):
        config = self.config(vault_path=str(self.root / "yaml-vault"))
        os.environ["RESEARCH_CONFIG_PATH"] = str(config)
        os.environ["OBSIDIAN_VAULT_PATH"] = str(self.root / "env-vault")
        with patch.object(Path, "cwd", return_value=self.root):
            hunter.configure()
        self.assertEqual(hunter.PAPERS_DIR, self.root / "env-vault/20_Research/Papers")

    def test_vault_research_config_is_discovered(self):
        vault = self.root / "vault"
        self.config("vault/99_System/Config/research_interests.yaml", papers_dir="Custom")
        hunter.configure(vault_path=str(vault))
        self.assertEqual(hunter.PAPERS_DIR, vault / "Custom")

    def test_explicit_missing_config_does_not_fall_back(self):
        with self.assertRaises(FileNotFoundError):
            hunter.configure(str(self.root / "missing.yaml"), str(self.root / "vault"))

    def test_yaml_vault_and_custom_directory_are_preserved(self):
        config = self.config(vault_path=str(self.root / "vault"), papers_dir="Papers")
        hunter.configure(str(config))
        self.assertEqual(hunter.PDF_DIR, self.root / "vault/Papers/PDFs")

    def test_unknown_or_placeholder_vault_is_rejected_before_writing(self):
        for value in (None, "", "/path/to/your/obsidian-vault"):
            with self.subTest(vault=value):
                config = self.config(vault_path=value)
                with self.assertRaises(ValueError):
                    hunter.configure(str(config))

    def test_directory_cannot_escape_vault(self):
        config = self.config(vault_path=str(self.root / "vault"))
        for directory in ("../outside", str(self.root / "outside")):
            with self.subTest(directory=directory), self.assertRaises(ValueError):
                hunter.configure(str(config), papers_dir=directory)

    def test_config_must_be_a_mapping(self):
        config = self.root / "invalid.yaml"
        config.write_text("- item\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            hunter.load_config(str(config))

    def test_cli_help_from_unrelated_working_directory(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--config", result.stdout)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_cli_bad_config_exits_before_downloading(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--config", "missing.yaml"],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("Research config not found", result.stderr)
        self.assertEqual(list(self.root.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
