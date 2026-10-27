# Problem Definition Report

**Project Title:** AI-Powered FAQ Assistant for Itan Foods Meal-Kit Delivery
**Date:** October 2026
**Prepared by:** Samuel Adesemowo
**Status:** Draft for Review
**Note on figures:** Numeric figures in this draft are marked `[insert measured value]` where real organizational data is required. No figures in this document are measured results — they are placeholders to be filled from internal support records before final submission.

---

## 1. Business Problem

Itan Foods delivers weekly meal kits across Abeokuta, Sagamu, Ijebu-Ode and the Lagos-Ogun corridor. As order volume grows, the same twelve categories of customer questions — delivery zones, delivery days, delivery costs, subscription pause/skip, subscription cancellation, refunds, payment methods, vegetarian/vegan options, allergens, packaging, address changes, and how to reach human support — are asked repeatedly, often outside business hours (Mon–Sat, 8am–6pm).

Today this volume is handled manually by the human support team. The consequences:

- **Slow first responses.** Customers asking routine questions wait for a human to reply, even when the answer already exists in internal FAQ notes. Current first-response time: `[insert measured value]`.
- **Repetitive load on agents.** The support team answers the same twelve categories repeatedly, with limited time left for genuinely novel or urgent issues.
- **Inconsistency.** Different agents phrase the same policy (e.g., refund window, delivery fee) slightly differently, creating customer confusion.
- **After-hours gap.** Questions arriving outside 8am–6pm Mon–Sat receive no reply until the next business day, even when the answer is fully documented.
- **Risk of policy drift in manual responses.** Without a single canonical FAQ source, agents may relay outdated fee structures or policies.

In short, Itan Foods does not need a larger support team — it needs a **fast, grounded, always-available first-line answer** for the questions it has already answered a hundred times, with a clear path to human support for anything outside that scope.

## 2. Target Users

**Meal-kit customers (primary):** Need immediate, accurate answers to routine questions about delivery, billing, refunds, and dietary options — especially outside business hours. Currently they must wait for a human reply.

**Itan Foods support team (secondary):** Need the repetitive FAQ volume removed from their queue so they can focus on damaged-item reports, complaints, and edge cases that genuinely require human judgment.

**Operations / content team (tertiary):** Need a single canonical source of FAQ answers (the `faq` list) so that policies, fees, and zones are stated consistently everywhere.

## 3. Proposed AI Solution

A **retrieval-augmented generation (RAG) FAQ assistant** for Itan Foods, delivered as a simple web chat UI (Gradio). The system has three layers:

1. **Curated FAQ knowledge base.** Twelve canonical entries, each with a stable ID (F01–F12), a customer-style question, and the approved answer. This is the single source of truth. It is stored in the application as a structured list and is trivially extendable.

2. **Keyword + similarity retrieval.** On each user message, the system scores all FAQ entries by token overlap plus `SequenceMatcher` ratio against the question text, and selects the top matches above a threshold. If nothing clears the threshold, no FAQ context is passed to the LLM.

3. **Grounded LLM response.** The retrieved FAQ entries are injected into a strict system prompt: *"Answer ONLY using the context below. If the context does not contain the answer, reply: 'I don't have that information — please contact human support.' Do not invent policy, prices, or delivery details."* The LLM is Groq `openai/gpt-oss-20b` at temperature 0.3, max 500 tokens.

**Guardrails already implemented:**
- **Strict grounding instruction** in the system prompt (no invented fees, zones, or policies).
- **Explicit fallback** to human support when no FAQ entry matches the query.
- **Input validation** — empty and over-length inputs rejected before reaching the LLM.
- **Graceful error handling** for missing API key and any API exception.

**Out of scope for this iteration (candidate future work):** multi-turn memory, embeddings-based retrieval, Zendesk/ServiceNow integration, PII redaction, audit logging, self-service deflection beyond FAQ scope.

## 4. Expected Benefits

Expected benefits are framed as hypotheses to validate, not measured results:

- **Faster first response for FAQ-scope questions.** Customers receive a grounded answer within seconds instead of waiting for a human — including outside business hours (Mon–Sat, 8am–6pm).
- **Reduced repetitive load on human agents.** FAQ-scope questions deflect away from the human queue; agents focus on damaged items, complaints, and non-standard cases.
- **Consistency.** Every answer to an FAQ-scope question is drawn from the same canonical entry (F01–F12), eliminating phrasing and policy drift between agents.
- **Honest fallback.** Out-of-scope questions are routed to human support with a clear message — no hallucinated fees, zones, or policies.
- **Low integration cost.** The system is standalone (Gradio UI + Groq API); no ticketing platform migration required for the first iteration.
- **Extensibility.** Adding a new FAQ entry is a single-line change to the `faq` list; no model retraining required.

Quantified targets (to be measured during pilot): `[insert target — e.g., % of FAQ-scope questions answered without human escalation]`, `[insert target — e.g., median first-response time for FAQ-scope questions]`.

## 5. Potential Challenges

**Accuracy and hallucination risk.** Even with a strict system prompt, the LLM may paraphrase or over-generalize a retrieved FAQ answer. *Mitigation:* strict grounding instruction, low temperature (0.3), 500-token cap, and — for any FAQ entry that must be quoted verbatim (e.g., fees, refund windows) — review a sample of live responses before launch.

**FAQ coverage gaps.** The current FAQ contains 12 entries. A customer asking about anything outside those 12 (e.g., international shipping, ingredient sourcing) will hit the fallback. *Mitigation:* monitor fallback frequency and add high-frequency missing questions to the FAQ on a rolling basis.

**Retrieval quality.** Keyword overlap + `SequenceMatcher` is a deliberately simple retriever. It can miss paraphrased questions (e.g., "how do I stop my boxes?" vs. "how do I cancel my subscription?") and can occasionally over-match a short ambiguous query. *Mitigation:* tune the threshold; move to embeddings-based retrieval in a future iteration.

**Customer trust in an AI assistant.** Some customers may distrust a bot or prefer a human. *Mitigation:* the fallback message explicitly offers human support (WhatsApp / phone / email per F12); the assistant is presented as first-line, not as a replacement.

**Privacy and key management.** Customer messages pass through the Groq API. API keys must never be hardcoded or committed. *Mitigation:* keys stored in `.env`, `.env` in `.gitignore`, and key rotation on any accidental exposure.

**Cost and rate limits.** Groq inference has per-request and per-minute limits. *Mitigation:* `max_tokens=500`, modest input-length cap (2000 chars), and monitoring of daily usage during pilot.

**Model drift / provider changes.** Model IDs and provider APIs evolve. *Mitigation:* model ID and provider isolated to config cells; periodic smoke-test of the pipeline.

## Recommendation

Proceed with a **2-week internal pilot** on the twelve FAQ entries, evaluated on:
1. **Grounded-answer rate** — % of FAQ-scope questions answered correctly from the canonical entry.
2. **Fallback correctness** — % of out-of-scope questions that receive the human-support fallback (no fabricated answers).
3. **Response time** — median seconds from message to reply.

Success criteria and threshold values `[insert after pilot]`. Any FAQ entries that fail grounded-answer review should be revised or removed before public launch.

---

*End of Report*