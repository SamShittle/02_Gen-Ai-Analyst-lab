#  SINGLE SETTINGS SOURCE (ENV, THTESHOLD)

"""Single source of truth for configuration. DRY: nothing else reads env vars."""
import os

LLM_PROVIDER   = os.getenv("LLM_PROVIDER", "openai")       # openai | anthropic | ollama
LLM_MODEL      = os.getenv("LLM_MODEL", "gpt-4o-mini")
TOP_K          = int(os.getenv("TOP_K", "3"))
MIN_SCORE      = float(os.getenv("MIN_SCORE", "0.20"))      # below this → refuse
FAQ_PATH       = os.getenv("FAQ_PATH", "data/faqs.json")
BUSINESS_NAME  = "Ìtàn Foods"
SUPPORT_CONTACT = "WhatsApp/call +234-XXX-XXX-XXXX or email support@itanfoods.example"