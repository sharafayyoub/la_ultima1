from src.repositories.NFTRepository import NFTRepository

class CLIController:
    def __init__(self):
        pass

    def run(self):
        print("Running CLI Controller")

nft_repo = NFTRepository()

def launch_cli():
    print("Bienvenido a la CLI de la plataforma de votaciones interactivas.")
    usuario_actual = None  # Simulación de sesión de usuario
    # Aquí iría el bucle principal de comandos
    while True:
        cmd = input(">> ")
        if cmd in ("salir", "exit", "quit"):
            print("Saliendo...")
            break
        if cmd.startswith("login"):
            parts = cmd.split()
            if len(parts) < 2:
                print("Uso: login <username>")
                continue
            usuario_actual = parts[1]
            print(f"Sesión iniciada como {usuario_actual}")
            continue
        if cmd.startswith("mis_tokens"):
            parts = cmd.split()
            username = usuario_actual if usuario_actual else (parts[1] if len(parts) > 1 else None)
            if not username:
                print("Uso: mis_tokens <username> (o haz login primero)")
                continue
            tokens = nft_repo.get_by_owner(username)
            if not tokens:
                print("No tienes tokens NFT.")
            else:
                for t in tokens:
                    print(f"TokenID: {t['token_id']} | Encuesta: {t['poll_id']} | Opción: {t['option']} | Fecha: {t['issued_at']}")
            continue
        if cmd.startswith("transferir_token"):
            parts = cmd.split()
            if len(parts) < 3:
                print("Uso: transferir_token <token_id> <nuevo_owner>")
                continue
            if not usuario_actual:
                print("Debes iniciar sesión con 'login <username>' para transferir tokens.")
                continue
            token_id, nuevo_owner = parts[1], parts[2]
            tokens = nft_repo.get_by_owner(usuario_actual)
            if not any(t["token_id"] == token_id for t in tokens):
                print("No eres el propietario de ese token o no existe.")
                continue
            nft_repo.transfer(token_id, nuevo_owner)
            print(f"Token {token_id} transferido a {nuevo_owner}.")
            continue
        # Procesar comandos aquí
        print(f"Comando recibido: {cmd}")