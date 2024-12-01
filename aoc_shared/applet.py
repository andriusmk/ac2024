from typing import Protocol, Iterable

class Applet(Protocol):
    def parse_input(self, stream: Iterable[str]) -> None:
        ...
    
    def calculate_result(self) -> int:
        ...

def process_file(applet: Applet, file_name: str) -> int:
    with open(file_name, encoding="utf-8") as file:
        applet.parse_input(file)
    return applet.calculate_result()
