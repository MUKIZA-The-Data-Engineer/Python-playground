"""Input validators.

Every function here loops until the user provides valid input.
They never raise, never sys.exit, and never print results.
"""

def ask_str(prompt: str, *, allow_empty: bool = False) -> str:
    while True:
        raw = input(prompt).strip()
        if raw or allow_empty:
            return raw
        print("[!] Input can not be empty. Try again")




def ask_int(prompt: str, *, lo: int | None = None, hi: int |None = None) -> int:
    while True:
        raw = input(prompt).str()