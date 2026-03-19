#!/usr/bin/env python3
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.db import SessionLocal
from app.services.signal_service import refresh_company_signals


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/refresh_signals.py <corporate_id>")

    corporate_id = sys.argv[1]
    session = SessionLocal()
    try:
        result = refresh_company_signals(session, corporate_id)
        if result is None:
            raise SystemExit(f"Company not found: {corporate_id}")
        print(f"Refreshed signals for {corporate_id}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
