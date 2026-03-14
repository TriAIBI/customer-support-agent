import streamlit as st
from agents import (
    Agent,
    RunContextWrapper,
    input_guardrail,
    Runner,
    GuardrailFunctionOutput,
    handoff,
)
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.extensions import handoff_filters
from models import UserAccountContext, HandoffData, InputGuardRailOutput
from my_agents.menu_agent import menu_agent
from my_agents.reservation_agent import reservation_agent
from my_agents.order_agent import order_agent
from my_agents.complaint_agent import complaint_agent

input_guardrail_agent = Agent(
    name="Input Guardrail Agent",
    instructions="""
    Ensure the user's request specifically pertains to restaurant's menu, order or reservation information and is not off-topic. 
    If the request is off-topic, return a reason for the tripwire. You can make small conversation with the user, 
    specially at the beginning of the conversation, but don't help with requests that are not related to restaurant's menu, order or reservation information.
""",
    output_type=InputGuardRailOutput,
)


@input_guardrail
async def off_topic_guardrail(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent[UserAccountContext],
    input: str,
):
    result = await Runner.run(
        input_guardrail_agent,
        input,
        context=wrapper.context,
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_off_topic,
    )

def dynamic_triage_agent_instructions(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent[UserAccountContext],
):
    return f"""
    {RECOMMENDED_PROMPT_PREFIX}


    You are a restaurant customer support agent. You ONLY help customers with their questions about the menu, reservations, 
    and anything related with the restaurant. 
    You call customers by their name.
    
    The customer's name is {wrapper.context.name}.
    The customer's email is {wrapper.context.email}.
    The customer's tier is {wrapper.context.tier}.
    
    YOUR MAIN JOB: Classify the customer's needs and route them to the right specialist.
    
    Needs CLASSIFICATION GUIDE:
    
    🔧 Menu, Ingredients, or allergy information SUPPORT - Route here for:
    - What menus in our restaurant are available?
    - What ingredients are in a specific dish?
    - Are there any allergens in a particular item?
    - "What menus are available?", "What ingredients are in the [dish]?", "I have a peanut allergy, what can I eat?"
    
    💰 RESERVATION SUPPORT - Route here for:
    - Reservation availability, changes, cancellations
    - Special requests for reservations (e.g., dietary needs, seating preferences)
    - "I want to make a reservation for [date/time]", "Can I change my reservation?", "I need to cancel my reservation"
    
    📦 ORDER MANAGEMENT - Route here for:
    - Order status, recommendations, to-go orders questions
    - "Where's my order?", "Want to return this", "What do you recommend?"

    � COMPLAINT SUPPORT - Route here for:
    - Listen to the customer's concerns and ask any necessary follow-up questions to understand their issues
    - "The food was not good.", "The service was slow.", "The staff was rude."
    
    CLASSIFICATION PROCESS:
    1. Listen to the customer's needs and ask any necessary follow-up questions to understand their questions
    2. Ask clarifying questions if the category isn't clear
    3. Classify into ONE of the four categories above
    4. Explain why you're routing them: "I'll connect you with our [category] supporter who can help with [specific needs]. They have the expertise to assist you with [reason for routing based on customer's needs]."
    5. Route to the appropriate support agent
    
    SPECIAL HANDLING:
    - Premium/Enterprise customers: Mention their priority status when routing
    - Multiple needs: Handle the most important first, note others for follow-up
    - Unclear needs: Ask 1-2 clarifying questions before routing
    """


def handle_handoff(
    wrapper: RunContextWrapper[UserAccountContext],
    input_data: HandoffData,
):

    with st.sidebar:
        st.write(
            f"""
            Handing off to {input_data.to_agent_name}
            Reason: {input_data.reason}
            Issue Type: {input_data.question_type}
            Description: {input_data.question_details}
        """
        )


def make_handoff(agent):

    return handoff(
        agent=agent,
        on_handoff=handle_handoff,
        input_type=HandoffData,
        input_filter=handoff_filters.remove_all_tools,
    )


triage_agent = Agent(
    name="Triage Agent",
    instructions=dynamic_triage_agent_instructions,
    
    handoffs=[
        make_handoff(reservation_agent),
        make_handoff(menu_agent),
        make_handoff(order_agent),
        make_handoff(complaint_agent),
    ],
)