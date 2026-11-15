"""Build the four condition instances from one base example."""
from data.schema import Condition, ConflictType, InstanceRecord


def build_instance_records(
    example_id: str,
    query: str,
    image_path: str,
    image_id: str,
    gold_answer: str,
    aligned_passage: str,
    contradicting_passage: str,
    text_answer_contradicting: str,
    wrong_image_path: str,
    wrong_image_id: str,
    conflict_type: ConflictType,
    source_dataset: str,
) -> list[InstanceRecord]:
    """
    Produce four InstanceRecords (one per condition) from a single base example.

    - Aligned:       correct image + aligned passage   (text_answer = gold)
    - Image-correct: correct image + contradicting passage (text_answer = wrong)
    - Text-correct:  wrong image   + aligned passage   (text_answer = gold)
    - Both-wrong:    wrong image   + contradicting passage (text_answer = wrong)
    """
    return [
        InstanceRecord(
            instance_id=f"{example_id}_aligned",
            example_id=example_id,
            condition=Condition.ALIGNED,
            conflict_type=conflict_type,
            source_dataset=source_dataset,
            query=query,
            gold_answer=gold_answer,
            image_path=image_path,
            image_id=image_id,
            text_passage=aligned_passage,
            text_answer=gold_answer,
        ),
        InstanceRecord(
            instance_id=f"{example_id}_image_correct",
            example_id=example_id,
            condition=Condition.IMAGE_CORRECT,
            conflict_type=conflict_type,
            source_dataset=source_dataset,
            query=query,
            gold_answer=gold_answer,
            image_path=image_path,
            image_id=image_id,
            text_passage=contradicting_passage,
            text_answer=text_answer_contradicting,
        ),
        InstanceRecord(
            instance_id=f"{example_id}_text_correct",
            example_id=example_id,
            condition=Condition.TEXT_CORRECT,
            conflict_type=conflict_type,
            source_dataset=source_dataset,
            query=query,
            gold_answer=gold_answer,
            image_path=wrong_image_path,
            image_id=wrong_image_id,
            text_passage=aligned_passage,
            text_answer=gold_answer,
        ),
        InstanceRecord(
            instance_id=f"{example_id}_both_wrong",
            example_id=example_id,
            condition=Condition.BOTH_WRONG,
            conflict_type=conflict_type,
            source_dataset=source_dataset,
            query=query,
            gold_answer=gold_answer,
            image_path=wrong_image_path,
            image_id=wrong_image_id,
            text_passage=contradicting_passage,
            text_answer=text_answer_contradicting,
        ),
    ]
