"""Kitchen-sink demo of the Inkpaper theme.

Run from the repo root:

    uv run python demo/app.py

Every Gradio component family appears at least once so a single visual
sweep verifies the whole theme.
"""

import time

import gradio as gr

import inkpaper


def greet(name: str, intensity: int) -> str:
    return "Hello " + ", ".join(["there"] * max(intensity, 1)) + f", {name}."


def slow_count(steps: float, progress=gr.Progress()) -> str:
    total = int(steps)
    for step in progress.tqdm(range(total)):
        time.sleep(0.4)
    return f"Counted to {total}."


def echo(message: str, history: list) -> str:
    return f"You said: {message}"


with gr.Blocks(title="Inkpaper demo") as demo:
    gr.Markdown(
        "# Inkpaper\n"
        "A Gradio theme matching [ronedgecomb.site](https://ronedgecomb.site). "
        "Ink surfaces, paper text, slate accents."
    )

    with gr.Tab("Inputs"):
        with gr.Row():
            name = gr.Textbox(label="Name", placeholder="Type a name")
            intensity = gr.Slider(1, 10, step=1, label="Intensity")
        with gr.Row():
            gr.Dropdown(["alpha", "beta", "gamma"], label="Dropdown")
            gr.Radio(["one", "two", "three"], label="Radio")
            gr.CheckboxGroup(["red herring", "real option"], label="Checkboxes")
        gr.Number(label="Number", value=42)
        greeting = gr.Textbox(label="Greeting", interactive=False)
        with gr.Row():
            greet_btn = gr.Button("Greet", variant="primary")
            clear_btn = gr.Button("Clear", variant="secondary")
        greet_btn.click(greet, inputs=[name, intensity], outputs=greeting)
        clear_btn.click(lambda: "", outputs=greeting)

    with gr.Tab("Long job"):
        steps = gr.Number(label="Steps", value=8)
        outcome = gr.Textbox(label="Outcome", interactive=False)
        with gr.Row():
            start = gr.Button("Start", variant="primary")
            stop = gr.Button("Stop", variant="stop")
        job = start.click(slow_count, inputs=steps, outputs=outcome)
        stop.click(None, cancels=[job])

    with gr.Tab("Chat"):
        gr.ChatInterface(echo)

    with gr.Tab("Data"):
        gr.Dataframe(
            value=[["inkpaper", "0.1.0"], ["gradio", "6.x"]],
            headers=["package", "version"],
            label="Versions",
        )

    with gr.Tab("Prose"):
        with gr.Accordion("About this theme", open=True):
            gr.Markdown(
                "Body text is 16px mono on ink. Metadata sits at 14px, "
                "labels at 12px. Links like "
                "[this one](https://ronedgecomb.site) rest paper and "
                "ease to slate on hover — slate always means interactive."
            )

if __name__ == "__main__":
    inkpaper.launch(demo)
