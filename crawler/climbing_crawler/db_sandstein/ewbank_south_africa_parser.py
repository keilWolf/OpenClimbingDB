from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem
from crawler.climbing_crawler.db_sandstein.base_parser import GradeMatch, GradeParser


class EwbankSouthAfricaGradeParser(GradeParser):
    def parse(self, content: str):
        """Australian Grade parsing.

        Examples: 11, 12, ... 38
        """
        try:
            if int(content) in range(11, 39):
                return [
                    GradeMatch(DiffType.RP, GradeSystem.EWBANK_SOUTH_AFRICA, content),
                ]
        except ValueError:
            return None
