import gradio as gr

def status():
    return "Rubicon is running ✅"

demo = gr.Interface(
    fn=status,
    inputs=[],
    outputs="text",
    title="Rubicon",
    description="Decision timing evaluation environment"
)

if __name__ == "__main__":
    demo.launch()