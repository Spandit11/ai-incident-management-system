"""
Main FastAPI application entry point.
"""

import time

from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from langsmith import traceable

from backend.workflows.incident_workflow import (
    incident_graph
)

from backend.tools.metrics_logger import (
    log_execution
)

from backend.tools.cost_tracker import (
    calculate_cost
)

from backend.tools.agent_tools import (
    memory_tool
)

from backend.guardrails.input_validator import (

    validate_log_content
)

from backend.guardrails.workflow_guard import (

    safe_workflow_run
)

from backend.config.settings import (

    CORS_ORIGINS,

    MAX_LOG_SIZE
)

# --------------------------------
# App Initialization
# --------------------------------

app = FastAPI(

    title="AI Incident Management"
)

app.add_middleware(

    CORSMiddleware,

    allow_origins=CORS_ORIGINS,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

# --------------------------------
# Workflow Execution
# --------------------------------

@traceable(
    name="Incident Workflow Execution"
)
def run_workflow(
    log_content: str
):

    return incident_graph.invoke(

        {

            "log_content":

            log_content
        }
    )

# --------------------------------
# Health Endpoint
# --------------------------------

@app.get("/")
def health_check():

    return {

        "status":

        "Backend Running Successfully"
    }

# --------------------------------
# Analyze Endpoint
# --------------------------------

@app.post("/analyze")
async def analyze_incident(

    file: UploadFile = File(...)
):

    start_time = time.time()

    content = await file.read()

    log_content = content.decode(

        "utf-8",

        errors="ignore"
    )

    # -----------------------
    # Validation
    # -----------------------

    is_valid, message = validate_log_content(

        log_content
    )

    if not is_valid:

        return {

            "error":

            message
        }

    # -----------------------
    # Token Optimization
    # -----------------------

    if len(

        log_content

    ) > MAX_LOG_SIZE:

        first_part = log_content[:2000]

        last_part = log_content[-2000:]

        log_content = (

            first_part

            +

            "\n...\n[TRUNCATED]\n...\n"

            +

            last_part
        )

    # -----------------------
    # Workflow
    # -----------------------

    workflow_response = safe_workflow_run(

        run_workflow,

        log_content
    )

    if not workflow_response["success"]:

        return {

            "error":

            workflow_response[
                "message"
            ]
        }

    workflow_result = workflow_response["data"]

    # -----------------------
    # Safe Defaults
    # -----------------------

    analysis_result = workflow_result.get(

        "analysis",

        {

            "category":

            "Unknown",

            "severity":

            "Unknown",

            "summary":

            "No analysis generated"
        }
    )

    analysis_usage = workflow_result.get(

        "analysis_usage",

        {

            "prompt_tokens": 0,

            "completion_tokens": 0
        }
    )

    rca_usage = workflow_result.get(

        "rca_usage",

        {

            "prompt_tokens": 0,

            "completion_tokens": 0
        }
    )

    rca_result = workflow_result.get(

        "rca",

        {

            "rootCause":

            "Not Generated",

            "recommendedActions":

            [],

            "confidence":

            "N/A"
        }
    )

    similar_incidents = workflow_result.get(

        "similar_incidents",

        []
    )

    # -----------------------
    # Memory
    # -----------------------

    memory_result = {

        "stored": False
    }

    if "rca" in workflow_result:

        try:

            memory_result = memory_tool(

                summary=

                analysis_result[
                    "summary"
                ],

                root_cause=

                rca_result[
                    "rootCause"
                ],

                actions=

                rca_result[
                    "recommendedActions"
                ]
            )

        except Exception:

            memory_result = {

                "stored": False,

                "reason":

                "Memory unavailable"
            }

    execution_time = round(

        time.time() - start_time,

        2
    )

    # -----------------------
    # Logging
    # -----------------------

    log_execution(

        category=

        analysis_result[
            "category"
        ],

        severity=

        analysis_result[
            "severity"
        ],

        execution_time=

        execution_time,

        memory_status=

        memory_result[
            "stored"
        ]
    )

    # -----------------------
    # Cost
    # -----------------------

    total_prompt = (

        analysis_usage[
            "prompt_tokens"
        ]

        +

        rca_usage[
            "prompt_tokens"
        ]
    )

    total_completion = (

        analysis_usage[
            "completion_tokens"
        ]

        +

        rca_usage[
            "completion_tokens"
        ]
    )

    estimated_cost = calculate_cost(

        total_prompt,

        total_completion
    )

    return {

        "analysis":

            analysis_result,

        "similar_incidents":

            similar_incidents,

        "rca":

            rca_result,

        "execution_time":

            execution_time,

        "memory":

            memory_result,

        "prompt_tokens":

            total_prompt,

        "completion_tokens":

            total_completion,

        "estimated_cost":

            estimated_cost,

        "retrieval_confidence":

            workflow_result.get(

                "retrieval_confidence",

                []
            ),

        "workflow_path":

            workflow_result.get(

                "workflow_path",

                []
            )
    }