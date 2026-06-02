"""
Workflow nodes.
"""

from langsmith import traceable

from backend.agents.log_analysis_agent import (
    analyze_logs
)

from backend.agents.rca_agent import (
    generate_rca
)

from backend.tools.agent_tools import (
    retrieval_tool
)

from backend.tools.retry_handler import (
    execute_with_retry
)


@traceable(
    name="Log Analysis Agent"
)
def log_analysis_node(state):

    try:

        response = execute_with_retry(

            analyze_logs,

            state[
                "log_content"
            ]
        )

    except Exception:

        response = {

            "result": {

                "category":
                    "Unknown",

                "severity":
                    "Low",

                "summary":
                    "Analysis failed"
            },

            "usage": {

                "prompt_tokens": 0,

                "completion_tokens": 0
            }
        }

    path = state.get(

        "workflow_path",

        []
    )

    path.append(
        "analysis"
    )
    return {

        "analysis":

            response[
                "result"
            ],

        "analysis_usage":

            response[
                "usage"
            ],

        "next_step":

            "analysis",

        "workflow_path":

            path
    }
    return {

        "analysis":

            response[
                "result"
            ],

        "analysis_usage":

            response[
                "usage"
            ],

        "workflow_path":

            path
    }


@traceable(
    name="Retrieval Agent"
)
def retrieval_node(state):

    try:

        retrieval_result = execute_with_retry(

            retrieval_tool,

            state[
                "analysis"
            ]["summary"]
        )

    except Exception:

        retrieval_result = {

            "documents": [],

            "confidence": []
        }

    path = state.get(

        "workflow_path",

        []
    )

    path.append(
        "retrieval"
    )

    path.append(

        f"Retrieved:{len(retrieval_result['documents'])}"
    )

    return {

        "similar_incidents":

            retrieval_result[
                "documents"
            ],

        "retrieval_confidence":

            retrieval_result[
                "confidence"
            ],

        "workflow_path":

            path
    }


@traceable(
    name="RCA Agent"
)
def rca_node(state):

    try:

        response = execute_with_retry(

            generate_rca,

            incident_summary=

            state[
                "analysis"
            ]["summary"],

            similar_incidents=

            state[
                "similar_incidents"
            ]
        )

    except Exception:

        response = {

            "result": {

                "rootCause":
                    "Unable to generate RCA",

                "confidence":
                    "Low",

                "recommendedActions":
                    []
            },

            "usage": {

                "prompt_tokens": 0,

                "completion_tokens": 0
            }
        }

    path = state.get(

        "workflow_path",

        []
    )

    path.append(
        "rca"
    )

    return {

        "rca":

            response[
                "result"
            ],

        "rca_usage":

            response[
                "usage"
            ],

        "workflow_path":

            path
    }