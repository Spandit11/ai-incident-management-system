def safe_workflow_run(

    workflow_function,

    log_content
):

    try:

        return {

            "success": True,

            "data":

            workflow_function(
                log_content
            )
        }

    except Exception as ex:

        return {

            "success": False,

            "message":

            str(ex)
        }