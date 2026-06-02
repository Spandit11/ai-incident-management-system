"""
Workflow state schema.
"""

from typing import TypedDict


class IncidentState(TypedDict):

    log_content: str

    analysis: dict

    similar_incidents: list

    rca: dict

    analysis_usage: dict

    rca_usage: dict

    next_step: str

    workflow_path: list
    
    retrieval_confidence: list