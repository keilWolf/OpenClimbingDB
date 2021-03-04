import re

import roman


def create_difficulties_dict(
    af, rp=None, oU=None, jump=None, is_danger=False, is_anstr=False
):
    return {
        "Jump": jump,
        "Free/AF": af,
        "Without Support": oU,
        "RP": rp,
        "danger": is_danger,
        "anstr": is_anstr,
    }


def parse_difficulties(content: str):
    """Split difficulties.

    Examples:
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
    """

    strategies = [parse_explicit_jump_diff, parse_redpoint_arabic, parse_general_diff]

    for strategy in strategies:
        res = strategy(content)
        if res:
            return res

    return {}


def parse_explicit_jump_diff(content: str):
    """Parse explicit jump difficulty.

    Examples:
        Sprung 2 od. II
    """
    pattern = r"Sprung (\d) od\. (.*)"

    match = re.match(pattern, content)

    if match:
        groups = match.groups()
        jump = groups[0]
        af = groups[1]
        return create_difficulties_dict(af, jump=jump)

    return {}


def parse_general_diff(content: str):
    """Parse general difficulties.

    Examples:
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
    """
    pattern = r"(\d)?\/?(\w*)( \((.*)\))?( RP (\w*))?( !)?( anstr\.)?"

    match = re.match(pattern, content)
    if match:
        groups = match.groups()
        jump = groups[0]
        af = groups[1]
        oU = groups[3]
        rp = groups[5]
        danger = True if groups[6] else False
        anstr = True if groups[7] else False
        return create_difficulties_dict(af, rp, oU, jump, danger, anstr)


def parse_redpoint_arabic(content: str):
    """Parse explicit jump difficulty.

    Examples:
        7a
    """
    pattern = r"^(\d{1,2})(\w)$"
    match = re.match(pattern, content)
    if match:
        groups = match.groups()
        numeral = int(groups[0])
        letter = groups[1]
        diff = f"{roman.toRoman(numeral)}{letter}"
        return create_difficulties_dict(diff, rp=diff)
