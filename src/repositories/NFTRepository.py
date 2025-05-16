import json
import os
from src.models.TokenNFT import TokenNFT
from datetime import datetime

NFTS_FILE = "nfts.json"

class NFTRepository:
    def __init__(self, filepath=NFTS_FILE):
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump([], f)

    def save(self, token: TokenNFT):
        tokens = self.get_all()
        tokens.append({
            "token_id": token.token_id,
            "owner": token.owner,
            "poll_id": token.poll_id,
            "option": token.option,
            "issued_at": token.issued_at.isoformat()
        })
        with open(self.filepath, "w") as f:
            json.dump(tokens, f, indent=2)

    def get_all(self):
        with open(self.filepath, "r") as f:
            tokens = json.load(f)
        return tokens

    def get_by_owner(self, owner: str):
        return [t for t in self.get_all() if t["owner"] == owner]

    def transfer(self, token_id: str, new_owner: str):
        tokens = self.get_all()
        for t in tokens:
            if t["token_id"] == token_id:
                t["owner"] = new_owner
                break
        with open(self.filepath, "w") as f:
            json.dump(tokens, f, indent=2)
