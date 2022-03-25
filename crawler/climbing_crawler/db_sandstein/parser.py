import re
from typing import List

from crawler.climbing_crawler.db_sandstein.france_parser import FranceGradeParser
from crawler.climbing_crawler.db_sandstein.base_parser import GradeMatch
from crawler.climbing_crawler.db_sandstein.saxony_parser import SaxonyGradeParser
from crawler.climbing_crawler.db_sandstein.uiaa_parser import UIAAGradeParser
from crawler.climbing_crawler.db_sandstein.australia_parser import AustraliaGradeParser


class GradeParser:
    exception_pattern = [
        r"Sprung\W*",
    ]

    def __init__(self):
        self.strategies = [
            UIAAGradeParser(),
            FranceGradeParser(),
            AustraliaGradeParser(),
            SaxonyGradeParser(),
        ]

    @staticmethod
    def saxony():
        gp = GradeParser()
        gp.strategies = [
            SaxonyGradeParser(),
        ]
        return gp

    def is_temporary_exception(self, content: str):
        for ep in self.exception_pattern:
            match = re.match(rf"^{ep}$", content)
            if match:
                return True
        return False

    def parse(self, content: str) -> List[GradeMatch]:
        if self.is_temporary_exception(content):
            raise LookupError("Temporary Exception")
        content = remove_unnecesarry(content)
        content = correct_spelling(content)
        if len(content) == 0 or "?" in content:
            return []
        for strategy in self.strategies:
            res = strategy.parse(content)
            if res:
                return res

        raise ValueError(f"No strategy to parse diff [{content}]")


def remove_unnecesarry(content: str) -> str:
    content = (
        content.replace("!", "")
        .replace("?", "")
        .replace("anstr.", "")
        .replace(" ", "")
        .replace("\\/", "")
        .strip()
    )
    content = re.sub(r",meist\d{1,2}[+-]?", "", content)  # example: TODO
    content = re.sub(r"\(original\d{1,2}[+-]?\)", "", content)  # example: TODO
    return content


def correct_spelling(content: str) -> str:
    return content.replace("PP", "RP").replace("i", "I")
