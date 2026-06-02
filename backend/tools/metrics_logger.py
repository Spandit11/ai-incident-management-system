"""
Stores workflow execution history.
"""

import json
from datetime import datetime

FILE_PATH = "data/execution_history.json"


def log_execution(
    category,
    severity,
    execution_time,
    memory_status
):
    """
    Save workflow metrics.
    """

    try:

        with open(
            FILE_PATH,
            "r"
        ) as file:

            history = json.load(file)

    except Exception:

        history = []

    history.append(
        {
            "timestamp": str(
                datetime.now()
            ),
            "category": category,
            "severity": severity,
            "execution_time": execution_time,
            "memory_status": memory_status
        }
    )

    with open(
        FILE_PATH,
        "w"
    ) as file:

        json.dump(
            history,
            file,
            indent=2
        )