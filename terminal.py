import sys
import os
from typing import List

if sys.platform == "win32":
    import msvcrt

    _special_keys = {
        "\x00": {  # special key prefix
            "H": "UP",
            "P": "DOWN",
            "K": "LEFT",
            "M": "RIGHT",
            "G": "HOME",
            "O": "END",
            "R": "INSERT",
            "S": "DELETE",
        },
        "\xe0": {  # alternative special key prefix
            "H": "UP",
            "P": "DOWN",
            "K": "LEFT",
            "M": "RIGHT",
            "G": "HOME",
            "O": "END",
            "R": "INSERT",
            "S": "DELETE",
        },
    }

    _ctrl_keys = {
        "\x1b": "ESC",
        "\r": "ENTER",
        "\t": "TAB",
        "\x08": "BACKSPACE",
        "\x03": "CTRL+C",
        "\x1a": "CTRL+Z",
    }

    def get_key():
        first = msvcrt.getwch()
        if first in _ctrl_keys:
            return _ctrl_keys[first]
        elif first in _special_keys:
            second = msvcrt.getwch()
            return _special_keys[first].get(second, f"SPECIAL_{ord(second):02X}")
        else:
            return first

    def clear_terminal():
        if (
            os.getenv("ANSICON")
            or "WT_SESSION" in os.environ
            or os.getenv("TERM_PROGRAM") == "vscode"
        ):
            print("\033[2J\033[H", end="", flush=True)
        else:
            os.system("cls")

else:
    import tty
    import termios

    _esc_sequences = {
        "[A": "UP",
        "[B": "DOWN",
        "[C": "RIGHT",
        "[D": "LEFT",
        "[H": "HOME",
        "[F": "END",
        "[2~": "INSERT",
        "[3~": "DELETE",
        "[5~": "PAGE_UP",
        "[6~": "PAGE_DOWN",
    }

    _ctrl_keys = {
        "\x1b": "ESC",
        "\r": "ENTER",
        "\n": "ENTER",
        "\t": "TAB",
        "\x7f": "BACKSPACE",
        "\x03": "CTRL+C",
        "\x1a": "CTRL+Z",
    }

    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch1 = sys.stdin.read(1)
            if ch1 in _ctrl_keys:
                return _ctrl_keys[ch1]
            if ch1 == "\x1b":  # start of escape sequence
                seq = ch1 + sys.stdin.read(1)
                if seq[1] == "[":
                    # Read remaining chars to match known sequences
                    seq_rest = ""
                    while True:
                        c = sys.stdin.read(1)
                        if c.isalpha() or c == "~":
                            seq_rest += c
                            break
                        else:
                            seq_rest += c
                    seq_full = seq + seq_rest
                    # Strip initial \x1b and look up sequence
                    key_name = _esc_sequences.get(seq_full[1:], None)
                    if key_name:
                        return key_name
                    else:
                        return f"ESC_SEQ_{seq_full[1:]}"
                else:
                    # Some other escape sequence or alt-key maybe
                    return "ESC"
            else:
                return ch1
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def clear_terminal():
        print("\033[2J\033[H", end="", flush=True)


def wait_on(keys_to_wait: List[str], case_sensitive: bool = False) -> str:
    options = set(keys_to_wait)

    while True:
        key = get_key()
        upper = key.upper()
        lower = key.lower()

        if not case_sensitive and (upper in options or lower in options):
            return lower
        elif case_sensitive and key in options:
            return key
