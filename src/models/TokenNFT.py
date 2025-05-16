import uuid
from datetime import datetime

class TokenNFT:
    def __init__(self, owner: str, poll_id: str, option: str, issued_at: datetime = None, token_id: str = None):
        self.token_id = token_id or str(uuid.uuid4())
        self.owner = owner
        self.poll_id = poll_id
        self.option = option
        self.issued_at = issued_at or datetime.utcnow()
