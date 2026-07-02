"""Aegis — layered (L0–L5) LLM jailbreak & prompt-injection defense.

Top-level convenience exports are lazy (PEP 562) so `import aegis` stays cheap:

    from aegis import Aegis, FastLayer, OutputModerator
"""
__version__ = "0.6.0"


def __getattr__(name):
    if name == "Aegis":
        from .pipeline import Aegis
        return Aegis
    if name == "FastLayer":
        from .prefilter.fast_layer import FastLayer
        return FastLayer
    if name == "OutputModerator":
        from .output import OutputModerator
        return OutputModerator
    raise AttributeError(f"module 'aegis' has no attribute {name!r}")


__all__ = ["Aegis", "FastLayer", "OutputModerator", "__version__"]
