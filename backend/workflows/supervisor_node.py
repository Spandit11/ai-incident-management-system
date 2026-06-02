"""
Supervisor node.
"""

from langsmith import traceable


@traceable(
    name="Supervisor Agent"
)
def supervisor_node(state):

    workflow_path = [

        "supervisor"
    ]

    log_size = len(

        state[
            "log_content"
        ]
    )

    # Very small logs
    if log_size < 20:

        next_step = "end"

    # Small logs
    elif log_size < 200:

        next_step = "analysis_only"

    # Large logs
    else:

        next_step = "analysis"

    return {

        "next_step":
            next_step,

        "workflow_path":
            workflow_path
    }