"""
Agent tools layer.
"""

from backend.rag.retrieval import (
    retrieve_similar_incidents
)

from backend.memory.incident_memory import (
    store_incident_if_unique
)
from backend.config.settings import (
    TOP_K_RESULTS
)

def retrieval_tool(

    incident_summary: str
):

    result = retrieve_similar_incidents(

        incident_summary
    )

    documents = result.get(

        "documents",

        [[]]
    )[0]

    distances = result.get(

        "distances",

        [[]]
    )[0]
    combined_results = list(

        zip(

            documents,

            distances
        )
    )

    combined_results.sort(

        key=lambda x:

        x[1]
    )

    TOP_K = TOP_K_RESULTS

    combined_results = combined_results[

        :TOP_K
    ]

    documents = [

        x[0]

        for x in combined_results
    ]

    distances = [

        x[1]

        for x in combined_results
    ]
    confidence = []

    for score in distances:

        similarity = round(

            max(

                0,

                (1 - score)

            ) * 100,

            2
        )

        confidence.append(

            similarity
        )

    return {

        "documents":

            documents,

        "confidence":

            confidence
    }

def memory_tool(

    summary,

    root_cause,

    actions
):
    """
    Memory Tool
    """

    return store_incident_if_unique(

        summary=summary,

        root_cause=root_cause,

        actions=actions
    )