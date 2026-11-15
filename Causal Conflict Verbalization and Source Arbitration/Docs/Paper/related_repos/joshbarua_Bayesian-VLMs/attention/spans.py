"""Partition positions visible to the answer readout into source spans."""

from __future__ import annotations

from dataclasses import dataclass


SPAN_NAMES = ("image", "passage", "question", "other")


@dataclass
class Spans:
    """A disjoint partition of positions ``[0, readout]``."""

    readout: int
    image: list[int]
    passage: list[int]
    question: list[int]
    other: list[int]
    question_located: bool = False

    def as_dict(self) -> dict[str, list[int]]:
        return {
            "image": self.image,
            "passage": self.passage,
            "question": self.question,
            "other": self.other,
        }

    def check(self) -> None:
        seen: set[int] = set()
        for name, positions in self.as_dict().items():
            current = set(positions)
            if len(current) != len(positions):
                raise ValueError(f"span {name!r} has duplicate positions")
            overlap = seen & current
            if overlap:
                raise ValueError(
                    f"span {name!r} overlaps an earlier span at {sorted(overlap)[:5]}"
                )
            seen |= current
        expected = set(range(self.readout + 1))
        if seen != expected:
            raise ValueError(
                f"spans do not partition [0, {self.readout}]: "
                f"missing={sorted(expected - seen)[:5]} "
                f"extra={sorted(seen - expected)[:5]}"
            )

    def sizes(self) -> dict[str, int]:
        return {name: len(value) for name, value in self.as_dict().items()}


def build_spans(adapter, model_input, question: str) -> Spans:
    """Locate image, passage, and question positions; assign the rest to other."""

    readout = int(model_input.answer_pos)
    expanded_ids = model_input.inputs["input_ids"][0].tolist()
    visible = set(range(readout + 1))
    image = sorted(pos for pos in model_input.vision_positions if pos in visible)
    passage = sorted(pos for pos in model_input.text_positions if pos in visible)
    if set(image) & set(passage):
        raise ValueError("image and passage positions overlap")
    remaining = visible - set(image) - set(passage)

    anchor = passage if passage else image
    restrict_after = max(anchor) + 1 if anchor else 0
    question_positions: list[int] = []
    try:
        found = adapter.find_passage_by_subsequence(
            expanded_ids, question, restrict_after=restrict_after
        )
        question_positions = sorted(int(pos) for pos in found if pos in remaining)
    except Exception:
        pass

    question_set = set(question_positions)
    spans = Spans(
        readout=readout,
        image=image,
        passage=passage,
        question=question_positions,
        other=sorted(remaining - question_set),
        question_located=bool(question_positions),
    )
    spans.check()
    return spans
