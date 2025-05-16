import argparse

def main():
    parser = argparse.ArgumentParser(description="Plataforma de votaciones interactivas para streamers")
    parser.add_argument('--ui', action='store_true', help='Iniciar interfaz web Gradio')
    parser.add_argument('--port', type=int, default=7860, help='Puerto para Gradio UI')
    # Aquí se pueden agregar más parámetros de configuración (rutas, IA, estrategias, etc.)
    args = parser.parse_args()

    if args.ui:
        from src.ui.GradioUI import launch_gradio_ui
        launch_gradio_ui(port=args.port)
    else:
        from src.controllers.CLIController import launch_cli
        launch_cli()

if __name__ == "__main__":
    main()
# Para que salga en Gradio, ejecuta en la terminal:
# python main.py --ui
# Luego abre el enlace que aparece en la consola (por ejemplo, http://127.0.0.1:7860/) en tu navegador.
# Para ejecutar en modo CLI:
# python main.py
# Para ejecutar la interfaz Gradio:
# python main.py --ui
# Luego abre el enlace que aparece en la consola (por ejemplo, http://127.0.0.1:7860/) en tu navegador.
# Si quieres ejecutar usando un archivo llamado app.py en src:
# python src/app.py --ui
# Si tu punto de entrada es main.py en la raíz:
# python main.py --ui
# Ambos comandos lanzarán la interfaz Gradio si el archivo y la ruta existen y están configurados correctamente.

