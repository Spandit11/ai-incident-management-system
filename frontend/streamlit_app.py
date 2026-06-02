"""
Streamlit frontend for AI Incident Management.
"""
import sys
import os

sys.path.append(

    os.path.abspath(

        os.path.join(

            os.path.dirname(__file__),

            ".."
        )
    )
)
import requests
import streamlit as st
from backend.config.settings import (
    MAX_FILE_SIZE_MB,
    BACKEND_URL
)
st.set_page_config(
    page_title="AI Incident Management",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------------
# Sidebar
# -----------------------------------

with st.sidebar:

    st.title(
        "🤖 AI Incident Platform"
    )

    st.markdown("---")

    st.subheader(
        "Modules"
    )

    st.write(
        "📄 Incident Analyzer"
    )

    st.write(
        "📊 Dashboard"
    )

    st.markdown("---")

    st.subheader(
        "System Information"
    )

    st.caption(
        "Model: GPT-4.1-mini"
    )

    st.caption(
        "Embedding: text-embedding-3-small"
    )

    st.caption(
        "Workflow: LangGraph"
    )

    st.caption(
        "Memory: ChromaDB"
    )

    st.markdown("---")

    st.success(
        "LangSmith Enabled"
    )

# -----------------------------------
# Header
# -----------------------------------

st.title(
    "AI Incident Management Agent"
)

st.caption(
    "AI-powered log analysis, RAG retrieval and RCA generation"
)

uploaded_file = st.file_uploader(

    "Upload Incident Logs",

    type=[

        "log",

        "txt",

        "csv"
    ]
)

MAX_FILE_SIZE_MB = MAX_FILE_SIZE_MB

if uploaded_file:

    file_size_mb = round(

        uploaded_file.size /

        (1024 * 1024),

        2
    )

    if uploaded_file.size > (

        MAX_FILE_SIZE_MB *

        1024 *

        1024
    ):

        st.error(

            f"File exceeds {MAX_FILE_SIZE_MB} MB"
        )

        st.stop()

    st.success(

        f"Uploaded: {uploaded_file.name}"
    )

    analyze = st.button(

        "🚀 Analyze Incident",

        use_container_width=True
    )

    if analyze:

        progress = st.progress(0)

        status = st.empty()

        status.write(

            "Analyzing Logs..."
        )

        progress.progress(25)

        files = {

            "file": (

                uploaded_file.name,

                uploaded_file.getvalue(),

                uploaded_file.type
            )
        }

        response = requests.post(

            BACKEND_URL,

            files=files,

            timeout=120
        )

        progress.progress(60)

        status.write(

            "Generating RCA..."
        )

        if response.status_code != 200:

            st.error(

                f"Backend Error: {response.status_code}"
            )

            st.write(

                response.text
            )

            st.stop()

        result = response.json()

        if "error" in result:

            st.error(

                result[
                    "error"
                ]
            )

            st.stop()

        progress.progress(100)

        status.write(

            "Completed ✅"
        )

        # -----------------
        # Metrics
        # -----------------

        st.subheader(

            "Execution Metrics"
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(

            "Execution",

            f"{result['execution_time']} sec"
        )

        c2.metric(

            "Prompt Tokens",

            result.get(

                "prompt_tokens",

                0
            )
        )

        c3.metric(

            "Estimated Cost",

            result.get(

                "estimated_cost",

                0
            )
        )

        c4.metric(

            "File Size",

            f"{file_size_mb} MB"
        )

        st.subheader(

            "Workflow Progress"
        )

        workflow = " ✅ ".join(

            result.get(

                "workflow_path",

                []
            )
        )

        st.success(

            workflow
        )

        analysis = result.get(

            "analysis",

            {}
        )

        rca = result.get(

            "rca",

            {

                "rootCause":

                "Not Generated",

                "confidence":

                "N/A",

                "recommendedActions":

                []
            }
        )

        tab1, tab2, tab3 = st.tabs(

            [

                "Analysis",

                "RCA",

                "Observability"
            ]
        )

        # -----------------
        # Analysis
        # -----------------

        with tab1:

            st.subheader(

                "Category"
            )

            st.write(

                analysis.get(

                    "category",

                    "Unknown"
                )
            )

            st.subheader(

                "Severity"
            )

            st.write(

                analysis.get(

                    "severity",

                    "Unknown"
                )
            )

            st.subheader(

                "Summary"
            )

            st.write(

                analysis.get(

                    "summary",

                    "No summary"
                )
            )

            with st.expander(

                "Retrieved Incidents"
            ):

                incidents = result.get(

                    "similar_incidents",

                    []
                )

                confidence_scores = result.get(

                    "retrieval_confidence",

                    []
                )

                st.metric(

                    "Retrieved",

                    len(

                        incidents
                    )
                )

                if incidents:

                    for idx, incident in enumerate(

                        incidents
                    ):

                        similarity = "N/A"

                        if idx < len(

                            confidence_scores
                        ):

                            similarity = (

                                f"{confidence_scores[idx]}%"
                            )

                        st.markdown(

                            f"""
**Incident**

{incident}

Similarity:

{similarity}
"""
                        )

                else:

                    st.info(

                        "No incidents retrieved."
                    )

        # -----------------
        # RCA
        # -----------------

        with tab2:

            st.write(

                rca.get(

                    "rootCause",

                    "Not Generated"
                )
            )

            st.write(

                f"Confidence: {rca.get('confidence','N/A')}"
            )

            actions = rca.get(

                "recommendedActions",

                []
            )

            if actions:

                for action in actions:

                    st.write(

                        "•",

                        action
                    )

        # -----------------
        # Observability
        # -----------------

        with tab3:

            st.json(

                result.get(

                    "memory",

                    {}
                )
            )

            st.success(

                "Workflow completed"
            )

        st.markdown(

            "---"
        )

        st.caption(

            "AI Incident Management Platform | LangGraph + RAG + Multi-Agent Workflow"
        )