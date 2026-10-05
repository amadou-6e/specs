"""Focused tests for typed specification validation."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.validate_specs import check_fixed_category, check_references


class FixedImplementationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.partition = self.project / "implementation" / "rust"
        self.partition.mkdir(parents=True)
        (self.project / "implementation" / "README.md").write_text("# Implementation\n")
        (self.partition / "README.md").write_text("# Rust\n")

    def write_entry(
        self, *, status: str = "draft", kind: str = "implementation", related: str = "[]"
    ) -> Path:
        path = self.partition / "testing.md"
        path.write_text(
            "---\n"
            "title: Rust testing\n"
            f"status: {status}\n"
            f"kind: {kind}\n"
            "owners: [team]\n"
            "last_reviewed: 2026-09-29\n"
            "applies_to: [project]\n"
            f"related: {related}\n"
            "---\n\n# Rust testing\n",
            encoding="utf-8",
        )
        return path

    def check(self) -> tuple[list[str], set[str]]:
        errors: list[str] = []
        refs = check_fixed_category(
            self.project,
            "implementation",
            errors,
            allowed_statuses={"draft", "active"},
            partitions=["rust"],
            expected_kind="implementation",
        )
        check_references(self.project, "implementation", "fixed", errors, refs)
        return errors, refs

    def test_nested_leaf_is_validated_and_referenceable(self) -> None:
        self.write_entry()
        errors, refs = self.check()
        self.assertEqual(errors, [])
        self.assertIn("implementation/rust/testing", refs)

    def test_nested_status_and_kind_fail(self) -> None:
        self.write_entry(status="bogus-status", kind="nonsense")
        errors, _ = self.check()
        self.assertTrue(any("frontmatter status" in error for error in errors))
        self.assertTrue(any("frontmatter kind" in error for error in errors))

    def test_broken_nested_reference_fails(self) -> None:
        self.write_entry(related="[implementation/rust/missing]")
        errors, _ = self.check()
        self.assertTrue(any("does not resolve" in error for error in errors))

    def test_container_readme_is_not_an_entry(self) -> None:
        self.write_entry(related="[implementation/rust/testing]")
        errors, refs = self.check()
        self.assertEqual(errors, [])
        self.assertNotIn("implementation/rust/README", refs)

    def test_support_skill_is_not_an_entry(self) -> None:
        self.write_entry()
        (self.partition / "SKILL.md").write_text("# Helper skill\n", encoding="utf-8")
        errors, refs = self.check()
        self.assertEqual(errors, [])
        self.assertNotIn("implementation/rust/SKILL", refs)

    def test_undeclared_partition_fails(self) -> None:
        self.write_entry()
        (self.project / "implementation" / "unexpected").mkdir()
        errors, _ = self.check()
        self.assertTrue(any("undeclared fixed partition" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
