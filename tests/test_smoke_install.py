"""The reusable artifact smoke check also works in the development install."""

from importlib.metadata import version

from scripts.smoke_install import verify


def test_verify_current_install() -> None:
    verify(version("inkpaper"))
