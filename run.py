import logging
from pathlib import Path

import quakewatch as qw

log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_dir / "run.log", encoding="utf-8"),
    ],
)

if "127.0.0.1" in qw.BASE:          # practice copy of the API on this laptop
    import mock_usgs
    mock_usgs.start()

print(qw.run_pipeline())
