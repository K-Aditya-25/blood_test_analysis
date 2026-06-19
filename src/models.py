from dataclasses import dataclass, field


@dataclass
class Test:
    __test__ = False
    key: str
    name: str
    section: str
    value: float | None
    value_text: str
    unit: str
    ref_low: float | None
    ref_high: float | None
    ref_text: str
    status: str = "normal"
    note: str = ""

    @property
    def in_range(self) -> bool:
        return self.status == "normal"


@dataclass
class Patient:
    name: str
    age: int
    gender: str
    lab_no: str
    collected: str
    reported: str
    tests: list[Test] = field(default_factory=list)
    summary: dict = field(default_factory=dict)

    def by_section(self, section: str) -> list[Test]:
        return [t for t in self.tests if t.section == section]


@dataclass
class Section:
    key: str
    title: str
    icon: str
    story: str
    chart_type: str
    order: int
