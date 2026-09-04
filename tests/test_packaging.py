import subprocess
from pathlib import Path

import pytest


REPOSITORY_ROOT = Path(__file__).parent.parent
PREBUILT_JAVASCRIPT = (
    "nbgitpuller/static/dist/bundle.js",
    "nbgitpuller/static/dist/bundle.js.LICENSE.txt",
)


def test_vcs_checkout_contains_prebuilt_javascript():
    """A direct VCS install must not require npm to build the wheel."""
    if not (REPOSITORY_ROOT / ".git").exists():
        pytest.skip("test requires a Git checkout")

    for path in PREBUILT_JAVASCRIPT:
        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", path],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            text=True,
        )

        assert tracked.returncode == 0, (
            f"{path} must be committed so pip can build directly from a VCS checkout "
            "without npm"
        )
        assert (REPOSITORY_ROOT / path).is_file()
