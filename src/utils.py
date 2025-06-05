from typing import Optional


def read_cli(msg: Optional[str]) -> str:
    return input(msg).rstrip()
