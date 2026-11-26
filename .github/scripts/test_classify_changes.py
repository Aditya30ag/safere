# Copyright (c) 2026 Eddie Aftandilian.
# Licensed under the BSD 3-Clause License (see LICENSE file).
"""Regression checks for skipping CI on documentation-only changes."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("classify-changes.sh")


class ClassifyChangesTest(unittest.TestCase):
    def test_documentation_only_changes_skip_ci(self):
        for files in [
            "",
            "README.md",
            "docs/TESTING.md\nINTENTIONAL_DIVERGENCES.md",
            "safere-fuzz/README.md",
            "LICENSE",
            ".agents/skills/divergence-bug-fix/SKILL.md",
            ".agents/skills/repo-assist/src/repo_assist/cli.py",
        ]:
            with self.subTest(files=files):
                self.assertEqual(self.classify(files), "code=false\n")

    def test_build_inputs_run_ci(self):
        for files in [
            "safere/src/main/java/org/safere/Matcher.java",
            "pom.xml",
            ".github/workflows/ci.yml",
            # Test data and build files that use the .txt extension.
            "safere/src/test/resources/re2-search.txt",
            "safere/src/test/resources/org/safere/GraphemeBreakTest.txt",
            "safere-fuzz/src/test/resources/intentional-reproductions/index.txt",
            "safere/src/main/resources/META-INF/LICENSE-Unicode.txt",
            "safere-benchmarks/cpp/CMakeLists.txt",
            "safere-ffm-re2/src/main/native/CMakeLists.txt",
            "README.md\nsafere-ffm-re2/src/main/native/CMakeLists.txt",
        ]:
            with self.subTest(files=files):
                self.assertEqual(self.classify(files), "code=true\n")

    def classify(self, files):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            output.touch()
            result = subprocess.run(
                ["bash", str(SCRIPT)],
                input=files + "\n",
                env={**os.environ, "GITHUB_OUTPUT": str(output)},
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            return output.read_text()


if __name__ == "__main__":
    unittest.main()
