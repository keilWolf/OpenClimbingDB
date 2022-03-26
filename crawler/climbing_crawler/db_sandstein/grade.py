from enum import Enum


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
    EWBANK_SOUTH_AFRICA = "Ewbank (South Africa)"
    USA = "USA"
