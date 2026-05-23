from typing_extensions import TypedDict, NotRequired


class Categories(TypedDict):
    name: str
    total_seconds: float
    percent: float
    digital: str
    decimal: str
    text: str
    hours: int
    minutes: int


class Project(TypedDict):
    name: str
    total_seconds: float
    percent: float
    digital: str
    decimal: str
    text: str
    hours: int
    minutes: int


class Languages(TypedDict):
    name: str
    total_seconds: float
    percent: float
    digital: str
    decimal: str
    text: str
    hours: int
    minutes: int
    seconds: int | None


class Editors(TypedDict):
    name: str
    total_seconds: float
    percent: float
    digital: str
    decimal: str
    text: str
    hours: int
    minutes: int
    seconds: int | None


class OperatingSystems(TypedDict):
    name: str
    total_seconds: float
    percent: float
    digital: str
    decimal: str
    text: str
    hours: int
    minutes: int


class Machines(TypedDict):
    name: str
    total_seconds: float
    percent: float
    digital: str
    decimal: str
    text: str
    hours: int
    minutes: int
    machine_name_id: str


class GrandTotal(TypedDict):
    decimal: str
    digital: str
    hours: int
    minutes: int
    text: str
    total_seconds: float


class AiAgentBreakdown(TypedDict):
    name: str
    lines: int
    cost: NotRequired[float]


class AiAgentSummary(TypedDict):
    name: str
    percent: float
    lines: int


class AiCodingSummary(TypedDict):
    ai_lines: int
    human_lines: int
    ai_percent: float
    human_percent: float
    dominant_label: str
    dominant_percent: float
    tokens_in: int
    tokens_out: int
    total_tokens: int
    agents: list[AiAgentSummary]


class Stats(TypedDict):
    human_readable_total: str
    human_readable_total_including_other_language: str
    daily_average: float
    daily_average_including_other_language: float
    human_readable_daily_average: str
    human_readable_daily_average_including_other_language: str
    categories: list[Categories] | None
    projects: list[Project] | None
    languages: list[Languages] | None
    editors: list[Editors] | None
    operating_systems: list[OperatingSystems] | None
    machines: list[Machines] | None
    user_id: str
    username: str
    is_up_to_date: bool
    ai_additions: NotRequired[int]
    ai_deletions: NotRequired[int]
    human_additions: NotRequired[int]
    human_deletions: NotRequired[int]
    ai_input_tokens: NotRequired[int]
    ai_output_tokens: NotRequired[int]
    ai_agent_line_changes: NotRequired[dict[str, int]]
    ai_agent_breakdown: NotRequired[list[AiAgentBreakdown]]
    ai_agent_costs: NotRequired[dict[str, float]]


class StatsBar(TypedDict):
    grand_total: GrandTotal
    categories: list[Categories] | None
    projects: list[Project] | None
    editors: list[Editors] | None
    languages: list[Languages] | None
    operating_systems: list[OperatingSystems] | None
