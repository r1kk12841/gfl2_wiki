"""
tests/conftest.py
Session fixtures for self-contained, isolated test runs.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Load site/build.py safely avoiding standard library 'site' module collision
_spec = importlib.util.spec_from_file_location("gfl2_site_builder", ROOT / "site" / "build.py")
if _spec is None or _spec.loader is None:
    raise ImportError(f"Could not load build script from {ROOT / 'site' / 'build.py'}")
_builder_mod = importlib.util.module_from_spec(_spec)
sys.modules["gfl2_site_builder"] = _builder_mod
_spec.loader.exec_module(_builder_mod)
build_site = _builder_mod.build_site
sanitize_guide_html = _builder_mod.sanitize_guide_html
load_guides = _builder_mod.load_guides


@pytest.fixture(scope="session")
def built_site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Build the static site once per test session in an isolated temporary directory."""
    output = tmp_path_factory.mktemp("site-output")
    result = build_site(output_dir=output)
    assert result == 0, "Initial site build in tmp directory failed"
    return output
