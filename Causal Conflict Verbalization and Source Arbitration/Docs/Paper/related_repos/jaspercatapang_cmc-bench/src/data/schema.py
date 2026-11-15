"""CMC-Bench data schema."""
import json
from dataclasses import dataclass, asdict
from enum import Enum


class ConflictType(str, Enum):
    FACTUAL = "factual"
    TEMPORAL = "temporal"
    ENTITY = "entity"
    GRANULARITY = "granularity"


class Condition(str, Enum):
    ALIGNED = "aligned"
    IMAGE_CORRECT = "image_correct"
    TEXT_CORRECT = "text_correct"
    BOTH_WRONG = "both_wrong"


def condition_is_conflict(c: Condition) -> bool:
    return c != Condition.ALIGNED


@dataclass
class InstanceRecord:
    instance_id: str
    example_id: str
    condition: Condition
    conflict_type: ConflictType
    source_dataset: str
    query: str
    gold_answer: str
    image_path: str
    image_id: str
    text_passage: str
    text_answer: str

    def model_dump(self) -> dict:
        d = asdict(self)
        d["condition"] = self.condition.value
        d["conflict_type"] = self.conflict_type.value
        return d

    def model_dump_json(self) -> str:
        return json.dumps(self.model_dump(), ensure_ascii=False)

    @classmethod
    def model_validate(cls, d: dict) -> "InstanceRecord":
        d = dict(d)
        d["condition"] = Condition(d["condition"])
        d["conflict_type"] = ConflictType(d["conflict_type"])
        return cls(**d)
