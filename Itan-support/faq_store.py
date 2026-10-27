"""Single loader/validator for the FAQ knowledge base. DRY: one load path."""
import json
from functools import lru_cache
from config import FAQ_PATH


@lru_cache(maxsize=1)
def load_faqs() -> list[dict]:
    with open(FAQ_PATH, encoding="utf-8") as f:
        faqs = json.load(f)
    ids = [f["id"] for f in faqs]
    assert len(ids) == len(set(ids)), "Duplicate FAQ ids"
    for f in faqs:
        assert f.get("q") and f.get("a"), f"Malformed FAQ {f.get('id')}"
    return faqs


def get_faq(faq_id: str) -> dict | None:
    return next((f for f in load_faqs() if f["id"] == faq_id), None)