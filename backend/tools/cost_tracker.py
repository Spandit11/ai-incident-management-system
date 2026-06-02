"""
Token and cost estimation.
"""
from backend.config.settings import (

    INPUT_TOKEN_PRICE,

    OUTPUT_TOKEN_PRICE
)

GPT41_MINI_INPUT = INPUT_TOKEN_PRICE
GPT41_MINI_OUTPUT = OUTPUT_TOKEN_PRICE


def calculate_cost(

    prompt_tokens,

    completion_tokens
):

    input_cost = (

        prompt_tokens

        * GPT41_MINI_INPUT
    )

    output_cost = (

        completion_tokens

        * GPT41_MINI_OUTPUT
    )

    total = round(

        input_cost + output_cost,

        6
    )

    return total