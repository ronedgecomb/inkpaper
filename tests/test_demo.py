"""The kitchen-sink demo keeps every showcase control genuinely live."""

import importlib.util
from pathlib import Path

import gradio as gr

APP_PATH = Path(__file__).resolve().parent.parent / "demo" / "app.py"


def _load_demo() -> gr.Blocks:
    spec = importlib.util.spec_from_file_location("demo_app", APP_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.demo


def test_showcase_inputs_are_interactive() -> None:
    demo = _load_demo()
    by_label = {getattr(block, "label", None): block for block in demo.blocks.values()}
    for label in ("Dropdown", "Radio", "Checkboxes", "Number"):
        assert by_label[label].interactive is True, label


def test_checkbox_choices_are_neutral() -> None:
    demo = _load_demo()
    checks = next(
        block
        for block in demo.blocks.values()
        if isinstance(block, gr.CheckboxGroup)
        and getattr(block, "label", None) == "Checkboxes"
    )
    values = [value for _, value in checks.choices]
    assert values == ["option a", "option b"]
