"""Train and compare EstateIQ's candidate valuation models."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.model_utils import METADATA_PATH, train_and_save_model

if __name__ == "__main__":
    train_and_save_model()
    print(METADATA_PATH.read_text(encoding="utf-8"))
