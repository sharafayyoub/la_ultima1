import gradio as gr
from src.services.ChatbotService import ChatbotService
from src.repositories.NFTRepository import NFTRepository

chatbot_service = ChatbotService()
nft_repo = NFTRepository()

def chatbot_response_function(message, history, username="anon"):
    # history: list of [user, bot] messages (Gradio format)
    response = chatbot_service.ask(username, message)
    return response

def tokens_gallery(username):
    tokens = nft_repo.get_by_owner(username)
    if not tokens:
        return "No tienes tokens NFT."
    # Mostrar como tabla de metadatos
    headers = ["Token ID", "Encuesta", "Opción", "Fecha"]
    rows = [
        [t["token_id"], t["poll_id"], t["option"], t["issued_at"]]
        for t in tokens
    ]
    import pandas as pd
    df = pd.DataFrame(rows, columns=headers)
    return df

def launch_gradio_ui(port=7860):
    with gr.Blocks() as demo:
        gr.Markdown("# Plataforma de votaciones interactivas")
        # ...otros componentes...
        gr.Markdown("## Galería de Tokens NFT")
        username_input = gr.Textbox(label="Usuario", value="anon")
        tokens_btn = gr.Button("Ver mis tokens")
        tokens_output = gr.Dataframe()
        tokens_btn.click(
            fn=lambda username: tokens_gallery(username),
            inputs=username_input,
            outputs=tokens_output
        )
        gr.Markdown("## Chatbot")
        gr.ChatInterface(
            fn=chatbot_response_function,
            title="Chatbot del Stream",
            chatbot=gr.Chatbot()
        )
    demo.launch(server_port=port)