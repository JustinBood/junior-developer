from gliner2 import GLiNER2
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig, RecognizerResult

LABEL_TO_ENTITY = {
    "full_name": "[NAME]",
    "first_name": "[NAME]",
    "last_name": "[NAME]",
    "email": "[EMAIL]",
    "phone_number": "[PHONE]",
}
LABELS = list(LABEL_TO_ENTITY)

OPERATORS = {
    placeholder: OperatorConfig("replace", {"new_value": placeholder})
    for placeholder in LABEL_TO_ENTITY.values()
}

anonymizer = AnonymizerEngine()


def redact(text: str, model: GLiNER2) -> str:
    """Replace names, emails and phone numbers in text with placeholders."""
    found = model.extract_entities(
        text, LABELS, include_spans=True, include_confidence=True
    )

    results = []
    for label, matches in found["entities"].items():
        for match in matches:
            results.append(
                RecognizerResult(
                    entity_type=LABEL_TO_ENTITY[label],
                    start=match["start"],
                    end=match["end"],
                    score=match["confidence"],
                )
            )

    return anonymizer.anonymize(text, results, OPERATORS).text