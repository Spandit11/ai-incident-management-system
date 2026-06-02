import re


def validate_log_content(

    log_content: str
):

    # -------------------
    # Small Content Check
    # -------------------

    if len(

        log_content.strip()

    ) < 20:

        return (

            False,

            "Log content too small"
        )

    # -------------------
    # Alpha Numeric Check
    # -------------------

    if not re.search(

        r"[A-Za-z0-9]",

        log_content
    ):

        return (

            False,

            "Invalid log content"
        )

    # -------------------
    # Log Keyword Check
    # -------------------

    log_keywords = [

        "ERROR",

        "WARN",

        "INFO",

        "Exception",

        "Traceback"
    ]

    keyword_found = any(

        keyword.lower()

        in

        log_content.lower()

        for keyword in log_keywords
    )

    if not keyword_found:

        return (

            False,

            "Not recognizable log content"
        )

    # -------------------
    # Special Character %
    # -------------------

    special_chars = len(

        re.findall(

            r"[^A-Za-z0-9\s]",

            log_content
        )
    )

    ratio = special_chars / max(

        len(log_content),

        1
    )

    if ratio > 0.70:

        return (

            False,

            "Too many special characters"
        )

    # -------------------
    # Malicious Patterns
    # -------------------

    suspicious_patterns = [

        "<script",

        "eval(",

        "exec(",

        "powershell",

        "cmd.exe",

        "rm -rf",

        "wget",

        "curl ",

        "base64",

        "subprocess",

        "import os",

        "drop table"
    ]

    for pattern in suspicious_patterns:

        if pattern.lower() in log_content.lower():

            return (

                False,

                "Suspicious content detected"
            )

    return (

        True,

        "Valid"
    )