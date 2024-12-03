from typing import Iterator
import re

mul_statement = re.compile(r"mul\((\d{1,3}+),(\d{1,3}+)\)")

def extract_products(input_data: str) -> Iterator[int]:
    matches = re.findall(mul_statement, input_data)
    number_pairs = (map(int, pair) for pair in matches)
    products = (x * y for x, y in number_pairs)
    return products
