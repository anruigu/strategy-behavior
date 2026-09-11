"""Canonical, JSON-native dataset records. Unknown measurements use null."""
from dataclasses import asdict, dataclass, field
import math

from prediction.io_utils import digest
from . import VERSION


@dataclass(frozen=True)
class Parameter:
    default: float
    values: tuple
    description: str

    def validate(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError(f"Nonfinite or nonnumeric parameter: {value!r}")
        if value not in self.values:
            raise ValueError(f"{value} outside declared parameter grid {self.values}")


@dataclass(frozen=True)
class GameFamily:
    family_id: str
    title: str
    mechanism: str | None
    mechanism_kind: str
    role: str
    actions: dict
    rules: str
    parameters: dict
    witness: tuple = ()
    information: str = "public"

    def record(self):
        return asdict(self)


@dataclass(frozen=True)
class Game:
    family_id: str
    parameters: dict
    construction_seed: int
    control: bool = False
    schema_version: str = VERSION

    @property
    def game_id(self):
        return "game-" + digest(asdict(self))[:24]

    def record(self):
        return {"game_id": self.game_id, **asdict(self)}


@dataclass(frozen=True)
class Player:
    model_id: str
    model_family: str
    provider: str
    provider_model: str
    model_generation: str | None = None
    model_size: str | None = None
    reasoning_setting: str | None = "low"
    temperature: float | None = .7
    sampling_seed: int | None = None
    implementation: str = "llm"


@dataclass(frozen=True)
class Role:
    seat_id: int
    strategic_role: str
    internal_actor: int = 0


@dataclass(frozen=True)
class Episode:
    game_id: str
    player_id: str
    trial: int
    environment_seed: int
    seat_order: tuple
    prompt_condition: str = "normal"
    opponent_policy: str = "ordinary"
    opponent_implementation: str = "scripted"

    def __post_init__(self):
        if self.prompt_condition not in ("normal", "active_exploration"):
            raise ValueError("Unknown prompt condition")
        if self.opponent_policy not in ("ordinary", "defensive"):
            raise ValueError("Unknown opponent policy")
        if self.opponent_implementation != "scripted":
            raise ValueError("Only scripted opponents are implemented in v1")
        if sorted(self.seat_order) != [0, 1, 2]:
            raise ValueError("Seats must be a permutation of three actors")

    @property
    def episode_id(self):
        return "ep-" + digest(asdict(self))[:24]

    def record(self):
        return {"episode_id": self.episode_id, **asdict(self), "seat_order": list(self.seat_order)}


@dataclass
class Trajectory:
    episode_id: str
    provenance: str
    status: str = "incomplete"
    steps: list = field(default_factory=list)
    behavior: dict | None = None
    exploit: dict | None = None
    outcome: dict | None = None
