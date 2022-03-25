import abc
from dataclasses import dataclass
from typing import List

from crawler.climbing_crawler.db_sandstein.grade import DiffType, GradeSystem


@dataclass
class GradeMatch:
    diff_type: DiffType
    gs: GradeSystem
    grade_str: str


class GradeParser(abc.ABC):
    @abc.abstractmethod
    def parse(self, content: str) -> List[GradeMatch]:
        """Parse grade from content string."""
