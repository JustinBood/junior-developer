import json
from pathlib import Path

from fastapi import APIRouter, Depends
from gliner2 import GLiNER2

from app.dependencies import get_model
from app.models import Data
from app.redaction import redact
from app.citations import link_citations

router = APIRouter(tags=["data"])

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "mock.json"


@router.get("/data")
def get_data(model: GLiNER2 = Depends(get_model)) -> list[Data]:
    items = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    data = [Data.model_validate(item) for item in items]
    for item in data:
        item.question = redact(item.question, model)
        item.content = link_citations(item.content, item.sources)
    return data