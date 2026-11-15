"""Save and load InstanceRecord lists as JSONL."""
import json
from pathlib import Path
from data.schema import InstanceRecord


def save_instances_jsonl(records: list[InstanceRecord], path: Path | str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(r.model_dump_json() + "\n")


def load_instances_jsonl(path: Path | str) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records
