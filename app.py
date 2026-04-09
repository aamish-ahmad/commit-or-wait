from fastapi import FastAPI
from typing import Optional, Dict, Any
import sys
import os
import gradio as gr

# Connect to your actual project logic
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from rubicon_openenv.environment import FraudEnvironment

# Initialize API and Environment
api = FastAPI()
env = FraudEnvironment()

# ==========================================
# 1. FASTAPI ENDPOINTS (What the Bot sees)
# ==========================================
@api.post("/reset")
async def reset_env(payload: Optional[Dict[str, Any]] = None):
    task = payload.get("task", "easy") if payload else "easy"
    return env.reset(task)

@api.post("/step")
async def step_env(payload: Optional[Dict[str, Any]] = None):
    action = "investigate"
    if payload and "action" in payload:
        action = payload["action"].get("action_type", "investigate") if isinstance(payload["action"], dict) else payload["action"]
    return env.step(action)

@api.get("/health")
async def health():
    return {"status": "healthy"}

# ==========================================
# 2. GRADIO UI (What you see)
# ==========================================
def run_step_ui(action_choice):
    return str(env.step(action_choice))

def reset_ui(task_choice):
    return str(env.reset(task_choice))

def check_health():
    return "✅ System Healthy: Backend and Logic are connected."

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# ⚖️ Rubicon: Decision Timing Environment")
    
    with gr.Row():
        btn_health = gr.Button("🩺 Check System")
        # ADDED MEDIUM HERE
        task_dropdown = gr.Dropdown(["easy", "medium", "hard"], label="Task Difficulty", value="medium")
        btn_reset = gr.Button("🔄 Reset Env")
        
    with gr.Row():
        action_dropdown = gr.Dropdown(["investigate", "freeze_account", "approve_transaction"], label="Execute Action", value="investigate")
        btn_step = gr.Button("⚡ Execute Action", variant="primary")

    out_box = gr.Textbox(label="Rubicon Feedback & Scoring", lines=8)
        
    btn_health.click(check_health, outputs=out_box)
    btn_reset.click(reset_ui, inputs=task_dropdown, outputs=out_box)
    btn_step.click(run_step_ui, inputs=action_dropdown, outputs=out_box)

app = gr.mount_gradio_app(api, demo, path="/")