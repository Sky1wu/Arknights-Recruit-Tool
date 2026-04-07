from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Operator:
    name: str
    level: int
    tags: frozenset[str]


@dataclass(frozen=True)
class CombinationResult:
    tags: tuple[str, ...]
    operators: tuple[Operator, ...]


@dataclass(frozen=True)
class RecruitAnalysis:
    rare_combinations: dict[str, tuple[CombinationResult, ...]]
    normal_combinations: tuple[CombinationResult, ...]


@dataclass(frozen=True)
class RecruitResult:
    status: int
    recognized_tags: tuple[str, ...] = ()
    rare_combinations: dict[str, tuple[CombinationResult, ...]] = field(default_factory=dict)
    normal_combinations: tuple[CombinationResult, ...] = ()
    message: str = ""
