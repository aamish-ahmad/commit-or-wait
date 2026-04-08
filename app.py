import gradio as gr
import requests

BASE = "http://localhost:7860"

def check_health():
    try:
        res = requests.get(f"{BASE}/health")
        return res.json()
    except:
        return "Backend not reachable"

def run_step():
    try:
        res = requests.post(
            f"{BASE}/step",
            json={"action_type": "inspect_headers", "task": "easy"}
        )
        return res.json()
    except:
        return "Error running step"

with gr.Blocks() as demo:
    gr.Markdown("# ⚖️ Rubicon")
    gr.Markdown("Evaluate when an agent decides — not just what it decides.")

    btn1 = gr.Button("Check Health")
    out1 = gr.JSON()

    btn2 = gr.Button("Run Step")
    out2 = gr.JSON()

    btn1.click(check_health, outputs=out1)
    btn2.click(run_step, outputs=out2)

demo.launch()