def launch_gradio_ui(port=7860):
    import gradio as gr
    with gr.Blocks() as demo:
        gr.Markdown("# Plataforma de votaciones interactivas")
        # Sección Encuestas
        gr.Markdown("## Encuestas activas")
        # ...widgets de encuestas...
        # Sección Chatbot
        gr.Markdown("## Chatbot")
        # ...widgets de chatbot...
        # Sección Tokens
        gr.Markdown("## Galería de Tokens NFT")
        # ...widgets de tokens...
    demo.launch(server_port=port)