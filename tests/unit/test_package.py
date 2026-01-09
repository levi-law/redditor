"""Black-box tests for Redditor package structure and imports.

These tests verify that the package is properly structured and all
expected modules can be imported successfully.
"""

import pytest
from pathlib import Path


class TestPackageStructure:
    """Tests for verifying the project structure matches tech-stack.yml."""
    
    def test_src_redditor_package_exists(self, project_root: Path):
        """The src/redditor package directory must exist."""
        package_dir = project_root / "src" / "redditor"
        assert package_dir.exists(), f"Package directory not found: {package_dir}"
        assert package_dir.is_dir(), f"Expected directory, got file: {package_dir}"
    
    def test_src_redditor_has_init(self, project_root: Path):
        """The src/redditor package must have __init__.py."""
        init_file = project_root / "src" / "redditor" / "__init__.py"
        assert init_file.exists(), f"__init__.py not found: {init_file}"
    
    def test_required_subdirectories_exist(self, project_root: Path):
        """All required subdirectories from tech-stack.yml must exist."""
        required_dirs = [
            "src/redditor/api",
            "src/redditor/agents",
            "src/redditor/pipelines",
            "src/redditor/reddit",
            "src/redditor/database",
            "src/redditor/utils",
            "tests/unit",
            "tests/integration",
        ]
        for dir_path in required_dirs:
            full_path = project_root / dir_path
            assert full_path.exists(), f"Required directory not found: {dir_path}"
    
    def test_project_has_requirements_file(self, project_root: Path):
        """Project must have requirements.txt for dependencies."""
        req_file = project_root / "requirements.txt"
        assert req_file.exists(), "requirements.txt not found in project root"
    
    def test_project_has_readme(self, project_root: Path):
        """Project must have README.md with documentation."""
        readme = project_root / "README.md"
        assert readme.exists(), "README.md not found in project root"
        content = readme.read_text()
        assert len(content) > 100, "README.md is too short"


class TestPackageImports:
    """Tests for verifying package imports work correctly."""
    
    def test_import_redditor_package(self):
        """The redditor package must be importable."""
        import redditor
        assert hasattr(redditor, "__version__"), "Package must define __version__"
    
    def test_import_config_module(self):
        """The config module must be importable."""
        from redditor import config
        assert hasattr(config, "Settings"), "Config must define Settings class"
    
    def test_import_cli_module(self):
        """The CLI module must be importable."""
        from redditor import cli
        assert hasattr(cli, "main"), "CLI must define main function/group"
    
    def test_import_reddit_client(self):
        """The Reddit client must be importable."""
        from redditor.reddit import client
        assert hasattr(client, "RedditClient"), "Reddit module must define RedditClient"
    
    def test_import_pipeline_base(self):
        """The Pipeline base class must be importable."""
        from redditor.pipelines import base
        assert hasattr(base, "Pipeline"), "Pipelines module must define Pipeline class"


class TestVersioning:
    """Tests for version information."""
    
    def test_version_format(self):
        """Version must follow semantic versioning format."""
        import redditor
        import re
        
        version = redditor.__version__
        # Matches patterns like 0.1.0, 1.0.0, 2.1.3-alpha, etc.
        pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$"
        assert re.match(pattern, version), f"Invalid version format: {version}"
