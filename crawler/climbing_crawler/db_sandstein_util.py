"""
Examples:
    Saxony:
        IV
        IV (VI)
        2/III
        2/Xa RP Xb
        IXb RP IXc
        IXa
        IXc (Xa) RP Xb
        VIIIa RP VIIIb
        V
        V !
        I (II) anstr.
    Pfalz:
        5+ A1 (6+)
        6- (5+, A0)
        4+,A0 (6)
    China:
        5.6
"""
from typing import List
from enum import Enum
import abc
import re
from dataclasses import dataclass

import roman


class DiffType(Enum):
    JUMP = "Jump"
    RP = "RP"
    AF = "Free/AF"
    A0 = "A0"
    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    A5 = "A5"


class GradeSystem(Enum):
    SAXON = "Saxon"
    SAXON_JUMP = "SaxonJump"
    UIAA = "UIAA"
    FRANCE = "France"
    TECHNICAL = "Technical"


@dataclass
class GradeMatch:
    diff_type: DiffType
    gs: GradeSystem
    grade_str: str


class GradeParser(abc.ABC):
    @abc.abstractmethod
    def parse(self, content: str) -> List[GradeMatch]:
        """Parse grade from content string."""


class UIAAGradeParser(GradeParser):
    def __init__(self):
        self._arabic = r"\d{1,2}[+-]?"
        self._support = r"A[0-6]?"
        self._roman = r"[VXI]+[+-]?"
        self.regexs = [
            # 1-, 3+ ... does not exist, should be 1,3
            r"^(?P<rp>[1,2,3])[+-]?$",
            # V+, X-, III
            rf"^(?P<rp_roman>{self._roman})$",
            # 8-, 10+, 7
            rf"^(?P<rp>{self._arabic})$",
            # II-V
            rf"^(?P<af_roman>{self._roman})-(?P<rp_roman>{self._roman})$",
            # II/V
            rf"^(?P<af_roman>{self._roman})/(?P<rp_roman>{self._roman})$",
            # 5+ A1 (6+)
            rf"^(?P<af>{self._arabic})(?P<support>{self._support})\((?P<rp>{self._arabic})\)$",  # noqa: E501
            # "5+ (5-A0)"
            rf"^(?P<rp>{self._arabic})\((?P<af>{self._arabic})(?P<support>{self._support})\)$",  # noqa: E501
            # "6+/A3"
            rf"^(?P<rp>{self._arabic})/(?P<support>{self._support})$",  # noqa: E501
            # 8+(6-/A1)
            rf"^(?P<rp>{self._arabic})\((?P<af>{self._arabic})/(?P<support>{self._support})\)$",  # noqa: E501
            # 3+ / 4+
            rf"^(?P<af>{self._arabic})/(?P<rp>{self._arabic})$",  # noqa: E501
            # 7+(original8)
            rf"^(?P<rp>{self._arabic})\(original{self._arabic}\)$",  # noqa: E501
            # 3, meist 2
            rf"^(?P<rp>{self._arabic}),meist{self._arabic}$",  # noqa: E501
        ]

    def parse(self, content: str) -> List[GradeMatch]:
        """UIAA Grade parsing."""

        for i, regex in enumerate(self.regexs):
            match = re.match(regex, content)

            if match:
                res = []
                if "rp_roman" in match.groupdict():
                    grade_str = self.roman_to_arabic(match.group("rp_roman"))
                    res.append(GradeMatch(DiffType.RP, GradeSystem.UIAA, grade_str))
                if "af_roman" in match.groupdict():
                    grade_str = self.roman_to_arabic(match.group("af_roman"))
                    res.append(GradeMatch(DiffType.AF, GradeSystem.UIAA, grade_str))
                if "rp" in match.groupdict():
                    res.append(
                        GradeMatch(DiffType.RP, GradeSystem.UIAA, match.group("rp"))
                    )
                if "support" in match.groupdict():
                    diff_type = DiffType[match.group("support")]
                    if "af" in match.groupdict():
                        grade_str = match.group("af")
                    else:
                        grade_str = "?"

                    res.append(GradeMatch(diff_type, GradeSystem.UIAA, grade_str))
                else:
                    if "af" in match.groupdict():
                        res.append(
                            GradeMatch(DiffType.AF, GradeSystem.UIAA, match.group("af"))
                        )
                return res

    def roman_to_arabic(self, roman_str):
        """Convert roman grade to arabic.

        Example: VII-   ==>   7-
        """
        sign = roman_str[-1]
        if sign == "+" or sign == "-":
            digits = roman_str[:-1]
            arabic_digits = roman.fromRoman(digits)
            return f"{arabic_digits}{sign}"
        return f"{roman.fromRoman(roman_str)}"


class FranceGradeParser(GradeParser):
    def parse(self, content: str):
        """France Grade parsing.

        Examples: 7a, 7a+
        """
        pattern = r"^\d[a,b,c]\+?$"
        match = re.match(pattern, content)
        if match:
            return [
                GradeMatch(DiffType.AF, GradeSystem.FRANCE, match.string),
            ]


class SaxonyGradeParser(GradeParser):
    """Grade parser for saxony grades."""

    def __init__(self):
        def jump():
            return r"(?P<jump>\d)"

        def roman(group_name):
            return rf"\**(?P<{group_name}>[XVI]+[abc]?)"

        self.regexs = [
            # II/1
            rf"{roman('rp')}\/{jump()}",
            # Sprung 3 od. VIIa
            rf"^Sprung{jump()}(od\.?{roman('rp')})?$",
            # 1/I
            rf"^{jump()}\/{roman('rp')}$",
            # 2/Xa RP Xb
            rf"^{jump()}\/{roman('af')}RP{roman('rp')}$",
            # Xa RP Xb
            rf"^{roman('af')}RP{roman('rp')}$",
            # IV (VI)
            rf"^{roman('ou')}\({roman('rp')}\)$",
            # VIIa
            rf"^{roman('rp')}$",
            # IXc (Xa) RP Xb
            rf"{roman('ou')}\({roman('af')}\)RP{roman('rp')}",
            # VIIc/RPVIIIa
            rf"^{roman('af')}/RP{roman('rp')}$",
            # VIIc/RPVIIIa
            rf"^{roman('af')}/{roman('rp')}$",
            # 7a
            r"(?P<rp_france>\d[a,b,c]\+?)",
            # VIIb-c
            r"(?P<af_r_base>[XVI]+)(?P<af_r0>[abc])-(?P<af_r1>[abc])",
            # V-VIIb
            r"(?P<af_r_explicit_0>[XVI]+[abc]?)-(?P<af_r_explicit_1>[XVI]+[abc]?)",
        ]

    def parse(self, content: str) -> List[GradeMatch]:
        """Parse saxony grade."""

        for regex in self.regexs:
            match = re.match(regex, content)

            if match:
                res = []
                if "jump" in match.groupdict() and match.group("jump"):
                    jump = GradeMatch(
                        DiffType.JUMP, GradeSystem.SAXON_JUMP, match.group("jump")
                    )
                    res.append(jump)
                if "af" in match.groupdict() and match.group("af"):
                    af = GradeMatch(DiffType.AF, GradeSystem.SAXON, match.group("af"))
                    res.append(af)
                if "rp" in match.groupdict() and match.group("rp"):
                    rp = GradeMatch(DiffType.RP, GradeSystem.SAXON, match.group("rp"))
                    res.append(rp)
                if "ou" in match.groupdict() and match.group("ou"):
                    ou = GradeMatch(DiffType.A0, GradeSystem.SAXON, match.group("ou"))
                    res.append(ou)
                if "rp_france" in match.groupdict() and match.group("rp_france"):
                    france = match.group("rp_france")
                    numeral = int(france[0])
                    letter = france[1]
                    roman_diff = f"{roman.toRoman(numeral)}{letter}"
                    res.append(GradeMatch(DiffType.RP, GradeSystem.SAXON, roman_diff))
                if "af_r_base" in match.groupdict():
                    base = match.group("af_r_base")
                    r0 = base + match.group("af_r0")
                    r1 = base + match.group("af_r1")
                    res.append(GradeMatch(DiffType.AF, GradeSystem.SAXON, r0))
                    res.append(GradeMatch(DiffType.RP, GradeSystem.SAXON, r1))
                if "af_r_explicit_0" in match.groupdict():
                    r0 = match.group("af_r_explicit_0")
                    r1 = match.group("af_r_explicit_1")
                    res.append(GradeMatch(DiffType.AF, GradeSystem.SAXON, r0))
                    res.append(GradeMatch(DiffType.RP, GradeSystem.SAXON, r1))

                return res


class GradeParser:
    exception_pattern = [
        r"Sprung\W*",
    ]

    def __init__(self):
        self.strategies = [
            UIAAGradeParser(),
            FranceGradeParser(),
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
        cleaned_content = (
            content.replace("!", "")
            .replace("?", "")
            .replace("anstr.", "")
            .replace(" ", "")
            .replace("\\/", "")
            .strip()
        )
        if len(content) == 0:
            return []
        for strategy in self.strategies:
            res = strategy.parse(cleaned_content)
            if res:
                return res

        raise ValueError(f"No strategy to parse diff [{cleaned_content}]")
