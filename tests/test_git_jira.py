from unittest import TestCase

from git_jira.git_jira import format_branch


class Test(TestCase):
    def test_format_branch(self):
        formatted_branch = format_branch('SUP 32372 Gradle Module Organization', '')
        self.assertEqual('SUP-32372-gradle-module-organization', formatted_branch)

    def test_format_branch_with_prefix(self):
        formatted_branch = format_branch('SUP 32372 Gradle Module Organization', 'feature')
        self.assertEqual('feature/SUP-32372-gradle-module-organization', formatted_branch)
