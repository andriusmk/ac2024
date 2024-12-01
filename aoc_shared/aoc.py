from typing import Callable, Any

def main(process: Callable[[str], Any]) -> None:
    with open("input") as file:
        content = file.read()
    print(process(content.strip()))
