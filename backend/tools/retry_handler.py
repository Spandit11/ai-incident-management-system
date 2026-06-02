import time


def execute_with_retry(

    function,

    *args,

    retries=3,

    delay=2,

    **kwargs
):

    last_error = None

    for attempt in range(

        retries
    ):

        try:

            return function(

                *args,

                **kwargs
            )

        except Exception as ex:

            last_error = ex

            time.sleep(

                delay * (

                    attempt + 1
                )
            )

    raise last_error