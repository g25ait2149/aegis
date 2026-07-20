"""
Attack suite — obfuscations used to (a) augment training and (b) test robustness.

SEEN attacks are used during training augmentation; UNSEEN attacks are held out
to measure generalization. Used defensively only.
"""
import base64
import codecs
import random

HOMO = {"a": "а", "e": "е", "o": "о", "c": "с"}   # latin -> cyrillic look-alikes


def leet(t, p=0.2, rng=random):
    m = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5"}
    return "".join(m.get(c, c) if (c.isalpha() and rng.random() < p) else c for c in t)


def homoglyph(t, p=0.3, rng=random):
    return "".join(HOMO.get(c, c) if (c in HOMO and rng.random() < p) else c for c in t)


def base64_attack(t, rng=random):
    return "Decode and follow: " + base64.b64encode(t.encode()).decode()


def rot13(t, rng=random):
    return "Decode ROT13: " + codecs.encode(t, "rot_13")


def zero_width(t, p=0.3, rng=random):
    return "".join(c + ("​" if rng.random() < p else "") for c in t)


def emoji_smuggle(t, rng=random):
    # interleave variation selectors (invisible) — a 2025/26 smuggling channel
    vs = "️"
    return "".join(c + (vs if c.isalpha() and rng.random() < 0.3 else "") for c in t)


def ascii_art(t, rng=random):
    return " ".join(list(t))   # space every character


SEEN = {"leet": leet, "homoglyph": homoglyph, "base64": base64_attack, "rot13": rot13}
UNSEEN = {"zero-width": zero_width, "emoji-smuggle": emoji_smuggle, "ascii-art": ascii_art}
ALL_ATTACKS = {**SEEN, **UNSEEN}


def augment(text, rng):
    """Apply 1-2 random SEEN attacks to a jailbreak example for training."""
    fns = list(SEEN.values())
    rng.shuffle(fns)
    for f in fns[: rng.randint(1, 2)]:
        try:
            text = f(text, rng=rng)
        except Exception:
            pass
    return text
