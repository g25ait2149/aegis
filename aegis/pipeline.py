"""
Aegis pipeline orchestrator (cascade).

L0 (normalize / spotlight) -> L1 FastLayer (RJD + semantic + signature) -> optional
L2 guard, invoked **only on uncertain prompts** (selective cascade) so the expensive
LLM guard is rarely called. Returns allow / escalate / block. L3/L4 plug in later.
"""
from .normalize.normalize import normalize, spotlight
from .prefilter.fast_layer import FastLayer


class Aegis:
    def __init__(self, detector=None, guard=None, block_at=0.80, allow_below=0.20, escalate_to_guard=True):
        self.detector = detector          # L1 fast layer
        self.guard = guard                 # L2 guard (TunedGuard / GuardEnsemble / OpenGuard)
        self.block_at, self.allow_below = block_at, allow_below
        self.escalate_to_guard = escalate_to_guard

    def fit(self, X, y):
        self.detector = (self.detector or FastLayer()).fit(X, y)
        return self

    def attach_guard(self, guard):
        self.guard = guard
        return self

    def scan(self, text, untrusted=None):
        ctx = spotlight(untrusted) if untrusted else ""             # L0 provenance
        payload = (text + "\n" + ctx) if ctx else text

        fast = float(self.detector.proba([payload])[0])             # L1 fast layer
        score, used_guard = fast, False
        # L2 — only escalate the uncertain band to the guard (cheap coverage, deep scrutiny where needed)
        if self.guard is not None and self.escalate_to_guard and self.allow_below <= fast < self.block_at:
            g = float(self.guard.proba([payload])[0])
            score, used_guard = max(fast, g), True

        decision = ("block" if score >= self.block_at else
                    "allow" if score < self.allow_below else "escalate")
        out = {"score": score, "fast_score": fast, "used_guard": used_guard,
               "decision": decision, "normalized": normalize(payload)}
        if hasattr(self.detector, "explain"):
            out["signals"] = self.detector.explain(payload)
        return out
