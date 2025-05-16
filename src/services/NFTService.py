from src.models.TokenNFT import TokenNFT
from src.repositories.NFTRepository import NFTRepository
from datetime import datetime

class NFTService:
    def __init__(self):
        self.nft_repo = NFTRepository()

    def mint_token(self, owner: str, poll_id: str, option: str):
        token = TokenNFT(owner=owner, poll_id=poll_id, option=option, issued_at=datetime.utcnow())
        self.nft_repo.save(token)
        return token.token_id

    def transfer_token(self, token_id: str, current_owner: str, new_owner: str) -> bool:
        tokens = self.nft_repo.get_by_owner(current_owner)
        if not any(t["token_id"] == token_id for t in tokens):
            return False  # No es el propietario
        self.nft_repo.transfer(token_id, new_owner)
        return True
