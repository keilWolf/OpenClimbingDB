import re
from typing import List

import roman
from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem
from crawler.climbing_crawler.db_sandstein.base_parser import GradeMatch, GradeParser

support_re = r"A[0-6]?"
roman_re = r"[VXI]+[+-]?"
# arabic_re = r"(1|2|3|4|[5-9][+-]?|1[0-2][+-]?)"
arabic_re = r"([1-9][+-]?|1[0-2][+-]?)"


def fix_sign_for_low_grades(grade_str: str):
    """Fix sign for low UIAA grades.

    Corresponding to the offical UIAA grades, there
    should be no sign for the grades 1 to 4. Signs
    starting at 5.
    """
    sign = None
    if "+" in grade_str:
        sign = "+"
    if "-" in grade_str:
        sign = "-"
    value = int(grade_str.split(sign)[0])
    if sign and value <= 4:
        return f"{value}"
    else:
        return grade_str


def roman_to_arabic(roman_str):
    """Convert roman grade to arabic.

    Example: VII-   ==>   7-
    """
    sign = roman_str[-1]
    if sign == "+" or sign == "-":
        digits = roman_str[:-1]
        arabic_digits = roman.fromRoman(digits)
        return f"{arabic_digits}{sign}"
    return f"{roman.fromRoman(roman_str)}"


class UIAAGradeParser(GradeParser):
    def __init__(self):
        # self._arabic = r"\b([1-9]|1[0-1])\b[+-]?"
        self._arabic = arabic_re
        self._support = r"A[0-6]?"
        self._roman = r"[VXI]+[+-]?"
        self.regexs = [
            # V+, X-, III
            rf"^(?P<rp_roman>{self._roman})$",
            # 8-, 10+, 7
            rf"^(?P<rp>{self._arabic})$",
            # II-V
            rf"^(?P<af_roman>{self._roman})-(?P<rp_roman>{self._roman})$",
            # II/V
            rf"^(?P<af_roman>{self._roman})/(?P<rp_roman>{self._roman})$",
            # 5+ A1
            rf"^(?P<af>{self._arabic})(?P<support>{self._support})$",
            # 5+ A1 (6+)
            rf"^(?P<af>{self._arabic})(?P<support>{self._support})\((?P<rp>{self._arabic})\)$",  # noqa: E501
            # "5+ (5-A0)"
            rf"^(?P<rp>{self._arabic})\((?P<af>{self._arabic})(?P<support>{self._support})\)$",  # noqa: E501
            # "6+/A3"
            rf"^(?P<af>{self._arabic})/(?P<support>{self._support})$",  # noqa: E501
            # 8+(6-/A1)
            rf"^(?P<rp>{self._arabic})\((?P<af>{self._arabic})/(?P<support>{self._support})\)$",  # noqa: E501
            # 3+ / 4+
            rf"^(?P<af>{self._arabic})/(?P<rp>{self._arabic})$",  # noqa: E501
            # 7+(original8)
            rf"^(?P<rp>{self._arabic})\(original{self._arabic}\)$",  # noqa: E501
            # 3, meist 2
            rf"^(?P<rp>{self._arabic}),meist{self._arabic}$",  # noqa: E501
            # 1-2
            rf"^(?P<af>{self._arabic})-(?P<rp>{self._arabic})$",  # noqa: E501
            # 5+ (6+)
            rf"^(?P<af>{self._arabic})\((?P<rp>{self._arabic})\)$",  # noqa: E501
            # 7 A0
            rf"^(?P<af>{self._arabic})\((?P<rp>{self._arabic})\)$",  # noqa: E501
        ]

    def parse(self, content: str) -> List[GradeMatch]:
        """UIAA Grade parsing."""

        for _, regex in enumerate(self.regexs):
            match = re.match(regex, content)

            if match:
                res = []
                if "rp_roman" in match.groupdict():
                    grade_str = roman_to_arabic(match.group("rp_roman"))
                    grade_str = fix_sign_for_low_grades(grade_str)
                    res.append(GradeMatch(DiffType.RP, GradeSystem.UIAA, grade_str))
                if "af_roman" in match.groupdict():
                    grade_str = roman_to_arabic(match.group("af_roman"))
                    grade_str = fix_sign_for_low_grades(grade_str)
                    res.append(GradeMatch(DiffType.AF, GradeSystem.UIAA, grade_str))
                if "rp" in match.groupdict():
                    grade_str = match.group("rp")
                    grade_str = fix_sign_for_low_grades(grade_str)
                    res.append(GradeMatch(DiffType.RP, GradeSystem.UIAA, grade_str))
                if "support" in match.groupdict():
                    diff_type = DiffType[match.group("support")]
                    grade_str = match.group("af")
                    grade_str = fix_sign_for_low_grades(grade_str)
                    res.append(GradeMatch(diff_type, GradeSystem.UIAA, grade_str))
                else:
                    if "af" in match.groupdict():
                        grade_str = match.group("af")
                        grade_str = fix_sign_for_low_grades(grade_str)
                        res.append(GradeMatch(DiffType.AF, GradeSystem.UIAA, grade_str))
                return res
