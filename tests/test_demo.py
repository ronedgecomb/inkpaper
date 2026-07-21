"""The kitchen-sink demo keeps every showcase control genuinely live."""

import importlib.util
from pathlib import Path
from types import ModuleType

import gradio as gr
import pytest

import inkpaper

APP_PATH = Path(__file__).resolve().parent.parent / "demo" / "app.py"


def _load_demo() -> ModuleType:
    spec = importlib.util.spec_from_file_location("demo_app", APP_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_showcase_inputs_are_interactive() -> None:
    demo = _load_demo().demo
    by_label = {getattr(block, "label", None): block for block in demo.blocks.values()}
    for label in ("Dropdown", "Radio", "Checkboxes", "Number"):
        assert by_label[label].interactive is True, label


def test_checkbox_choices_are_neutral() -> None:
    demo = _load_demo().demo
    checks = next(
        block
        for block in demo.blocks.values()
        if isinstance(block, gr.CheckboxGroup)
        and getattr(block, "label", None) == "Checkboxes"
    )
    values = [value for _, value in checks.choices]
    assert values == ["option a", "option b"]


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, 0),
        (-3, 0),
        (0, 0),
        (2.9, 2),
        (4, 4),
    ],
)
def test_normalize_steps(value: float | None, expected: int) -> None:
    module = _load_demo()
    assert module.normalize_steps(value) == expected


def test_demo_version_rows_use_runtime_metadata() -> None:
    module = _load_demo()
    assert [
        ["inkpaper", inkpaper.__version__],
        ["gradio", gr.__version__],
    ] == module.VERSION_ROWS


def test_demo_includes_a_read_only_code_surface() -> None:
    demo = _load_demo().demo
    code_blocks = [
        block for block in demo.blocks.values() if isinstance(block, gr.Code)
    ]
    assert len(code_blocks) == 1
    assert code_blocks[0].interactive is False
