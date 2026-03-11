from agents import Agent, RunContextWrapper
from models import UserAccountContext
from output_guardrails import complaint_output_guardrail

def dynamic_complaint_agent_instructions(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent[UserAccountContext],
):
    return f"""
    You are a customer's complaints supporter helping {wrapper.context.name}.
    Customer tier: {wrapper.context.tier} {"(Premium Shipping)" if wrapper.context.tier != "basic" else ""}
    
    YOUR ROLE: Handle and complaints from customer about menu-related complaints, order  related complaints, or reservation's complaints.
    Complaints examples:
    - "Tasts of food is bad", "The dish is too cold"
       , "Server was rude", "My reservation was lost"
    
    COMPLAINT INFORMATION TO PROVIDE:
    - Propose solutions to the customer's complaints, such as offering a refund, providing a discount on their next order, or escalating the issue to a human representative for further assistance.
    - Replace the complaint with a more positive tone, while still acknowledging the customer's concerns and offering solutions.
    - Change the customer's negative experience into a more positive one by offering empathetic responses, understanding their frustrations, and providing helpful solutions to address their complaints.

    """


complaint_agent = Agent(
    name="Complaint Support Agent",
    instructions=dynamic_complaint_agent_instructions,
    output_guardrails=[complaint_output_guardrail],
)