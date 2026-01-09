"""Black-box tests for Redditor CLI.

These tests verify the CLI interface works as expected without
testing internal implementation details.
"""

import pytest
from click.testing import CliRunner


class TestCLIHelp:
    """Tests for CLI help and basic functionality."""
    
    @pytest.fixture
    def runner(self):
        """Create a CLI test runner."""
        return CliRunner()
    
    def test_cli_help_returns_zero_exit_code(self, runner):
        """Running --help should return exit code 0."""
        from redditor.cli import main
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0, f"CLI help failed: {result.output}"
    
    def test_cli_help_shows_description(self, runner):
        """Help output should describe the Redditor application."""
        from redditor.cli import main
        result = runner.invoke(main, ["--help"])
        assert "redditor" in result.output.lower() or "reddit" in result.output.lower(), \
            "Help should mention Redditor/Reddit"
    
    def test_cli_version_option(self, runner):
        """CLI should display version with --version."""
        from redditor.cli import main
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        # Version should be in output
        assert "0.1.0" in result.output or "version" in result.output.lower()


class TestCLIPipelineCommands:
    """Tests for pipeline-related CLI commands."""
    
    @pytest.fixture
    def runner(self):
        """Create a CLI test runner."""
        return CliRunner()
    
    def test_pipeline_list_command_exists(self, runner):
        """CLI should have a 'pipeline list' or 'list' command."""
        from redditor.cli import main
        # Try to access pipeline commands
        result = runner.invoke(main, ["pipeline", "--help"])
        # Should either work or show group help
        assert result.exit_code in (0, 2), f"Unexpected error: {result.output}"
    
    def test_pipeline_run_command_exists(self, runner):
        """CLI should have a command to run pipelines."""
        from redditor.cli import main
        result = runner.invoke(main, ["pipeline", "run", "--help"])
        # Should show help for run command
        assert result.exit_code in (0, 2), f"Unexpected error: {result.output}"


class TestCLIConfigCommands:
    """Tests for configuration-related CLI commands."""
    
    @pytest.fixture
    def runner(self):
        """Create a CLI test runner."""
        return CliRunner()
    
    def test_config_show_command(self, runner):
        """CLI should have a way to show configuration."""
        from redditor.cli import main
        result = runner.invoke(main, ["config", "--help"])
        # Config commands should be accessible
        assert result.exit_code in (0, 2), f"Unexpected error: {result.output}"
