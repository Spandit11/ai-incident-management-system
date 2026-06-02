import json
from pathlib import Path

import streamlit as st

st.set_page_config(

    page_title="Observability Dashboard",

    page_icon="📊",

    layout="wide"
)

# ------------------------
# File Path
# ------------------------

FILE_PATH = (

    Path(__file__)

    .resolve()

    .parents[2]

    / "data"

    / "execution_history.json"
)

# ------------------------
# Sidebar
# ------------------------

with st.sidebar:

    st.title(
        "📊 Dashboard"
    )

    st.markdown("---")

    st.write(
        "Execution Analytics"
    )

    st.write(
        "Workflow Visibility"
    )

    st.write(
        "Incident History"
    )

# ------------------------
# Load Data
# ------------------------

st.title(
    "Observability Dashboard"
)

st.caption(
    "Workflow analytics and execution insights"
)

try:

    with open(
        FILE_PATH,
        "r"
    ) as file:

        history = json.load(file)

except Exception:

    history = []

# ------------------------
# Calculations
# ------------------------

total_runs = len(history)

avg_time = 0

if total_runs > 0:

    avg_time = round(

        sum(

            x["execution_time"]

            for x in history

        ) / total_runs,

        2
    )

memory_count = sum(

    1

    for x in history

    if x["memory_status"]
)

critical_count = sum(

    1

    for x in history

    if x["severity"] == "Critical"
)

high_count = sum(

    1

    for x in history

    if x["severity"] == "High"
)

# ------------------------
# KPI Cards
# ------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Runs",
    total_runs
)

col2.metric(
    "Avg Time",
    f"{avg_time}s"
)

col3.metric(
    "Stored",
    memory_count
)

col4.metric(
    "Critical",
    critical_count
)

col5.metric(
    "High",
    high_count
)

st.markdown("---")

# ------------------------
# Tabs
# ------------------------

tab1, tab2, tab3 = st.tabs(

    [

        "Execution History",

        "Workflow",

        "Insights"
    ]
)

# ------------------------
# History
# ------------------------

with tab1:

    if history:

        st.dataframe(

            history,

            use_container_width=True
        )

    else:

        st.warning(
            "No execution history available."
        )

# ------------------------
# Workflow
# ------------------------

with tab2:

    st.success(
        """
        ✅ Supervisor Agent

        ✅ Log Analysis Agent
        
        ✅ Retrieval Layer
        
        ✅ RCA Agent
        
        ✅ Memory Persistence
        
        ✅ LangGraph Workflow
        """
    )

# ------------------------
# Insights
# ------------------------

with tab3:

    st.write(
        f"Total Memory Updates: "
        f"{memory_count}"
    )

    st.write(
        f"Average Workflow Time: "
        f"{avg_time}s"
    )

    if total_runs:

        st.write(

            "Latest Severity:",

            history[-1][
                "severity"
            ]
        )