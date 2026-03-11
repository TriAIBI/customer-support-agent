from agents import (
    Agent,
    output_guardrail,
    Runner,
    RunContextWrapper,
    GuardrailFunctionOutput,
)
from models import ComplaintOutputGuardRailOutput, UserAccountContext


complaint_output_guardrail_agent = Agent(
    name="Complaint Support Guardrail",
    instructions="""
    Analyze the response for customer's questions or complaints to check if it inappropriately contains:
    
    - Menu information (recipes, ingredients, chef or servers's information, price)
    - Order information (cooking time, status)
    - Reservation information (availability, reservation details)
    
    Complaint agents should ONLY provide alternative solution for the complaints.
    Return true for any field that contains inappropriate content for a compaint support response.
    """,
    output_type=ComplaintOutputGuardRailOutput,
)


@output_guardrail
async def complaint_output_guardrail(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent,
    output: str,
):
    result = await Runner.run(
        complaint_output_guardrail_agent,
        output,
        context=wrapper.context,
    )

    validation = result.final_output

    triggered = (
        validation.contains_off_topic
        or validation.contains_complaint_data
    )

    return GuardrailFunctionOutput(
        output_info=validation,
        tripwire_triggered=triggered,
    )