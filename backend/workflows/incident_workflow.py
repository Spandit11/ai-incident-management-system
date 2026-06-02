"""
LangGraph incident workflow.
"""

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from backend.workflows.state import (
    IncidentState
)

from backend.workflows.nodes import (

    log_analysis_node,

    retrieval_node,

    rca_node
)

from backend.workflows.supervisor_node import (

    supervisor_node
)

workflow = StateGraph(
    IncidentState
)

workflow.add_node(
    "supervisor",
    supervisor_node
)

workflow.add_node(
    "log_analysis",
    log_analysis_node
)

workflow.add_node(
    "retrieval",
    retrieval_node
)

workflow.add_node(
    "rca",
    rca_node
)

workflow.add_edge(
    START,
    "supervisor"
)

# Supervisor routing
workflow.add_conditional_edges(

    "supervisor",

    lambda state:
        state["next_step"],

    {

        "analysis":
            "log_analysis",

        "analysis_only":
            "log_analysis",

        "end":
            END
    }
)

# Analysis routing
workflow.add_conditional_edges(

    "log_analysis",

    lambda state:

        state[
            "next_step"
        ],

    {

        "analysis":
            "retrieval",

        "analysis_only":
            END
    }
)

workflow.add_edge(

    "retrieval",

    "rca"
)

workflow.add_edge(

    "rca",

    END
)

incident_graph = workflow.compile()