import json
from pathlib import Path

from fastapi import APIRouter, Depends
from gliner2 import GLiNER2

from app.dependencies import get_model
from app.models import Data
from app.redaction import redact

router = APIRouter(tags=["data"])

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "mock.json"


@router.get("/data")
def get_data(model: GLiNER2 = Depends(get_model)) -> list[Data]:
    items = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    for item in items:
        item["question"] = redact(item["question"], model)
    return [Data.model_validate(item) for item in items]