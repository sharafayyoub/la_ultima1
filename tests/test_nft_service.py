import pytest
from src.services.NFTService import NFTService
from src.repositories.NFTRepository import NFTRepository

class DummyNFTRepository(NFTRepository):
    def __init__(self):
        self.tokens = []

    def save(self, token):
        self.tokens.append({
            "token_id": token.token_id,
            "owner": token.owner,
            "poll_id": token.poll_id,
            "option": token.option,
            "issued_at": token.issued_at.isoformat()
        })

    def get_by_owner(self, owner):
        return [t for t in self.tokens if t["owner"] == owner]

    def transfer(self, token_id, new_owner):
        for t in self.tokens:
            if t["token_id"] == token_id:
                t["owner"] = new_owner

@pytest.fixture
def nft_service(monkeypatch):
    service = NFTService()
    repo = DummyNFTRepository()
    service.nft_repo = repo
    return service

def test_mint_token_and_persist(nft_service):
    token_id = nft_service.mint_token("alice", "poll1", "OpciónA")
    tokens = nft_service.nft_repo.get_by_owner("alice")
    assert any(t["token_id"] == token_id for t in tokens)

def test_transferencia_valida(nft_service):
    token_id = nft_service.mint_token("alice", "poll1", "OpciónA")
    ok = nft_service.transfer_token(token_id, "alice", "bob")
    assert ok
    tokens_bob = nft_service.nft_repo.get_by_owner("bob")
    assert any(t["token_id"] == token_id for t in tokens_bob)

def test_transferencia_invalida(nft_service):
    token_id = nft_service.mint_token("alice", "poll1", "OpciónA")
    ok = nft_service.transfer_token(token_id, "bob", "carol")
    assert not ok
    tokens_carol = nft_service.nft_repo.get_by_owner("carol")
    assert not any(t["token_id"] == token_id for t in tokens_carol)
