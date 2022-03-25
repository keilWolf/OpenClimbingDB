import re
from typing import List

import roman
from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem
from crawler.climbing_crawler.db_sandstein.base_parser import GradeMatch, GradeParser


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
            # VIIc/VIIIa
            rf"^{roman('af')}/{roman('rp')}$",
            # RPVIIIa
            rf"^RP{roman('rp')}$",
            # 7a
            r"(?P<rp_france>\d[a,b,c]\+?)",
            # VIIb-c
            r"(?P<af_r_base>[XVI]+)(?P<af_r0>[abc])-(?P<af_r1>[abc])",
            # V-VIIb
            r"(?P<af_r_explicit_0>[XVI]+[abc]?)-(?P<af_r_explicit_1>[XVI]+[abc]?)",
            # 3h ... special case from goettinger wald
            rf"^{jump()}h$",
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
