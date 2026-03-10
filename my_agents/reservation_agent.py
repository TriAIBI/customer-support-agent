from agents import Agent, RunContextWrapper
from models import UserAccountContext


def dynamic_reservation_agent_instructions(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent[UserAccountContext],
):
    return f"""
    You are a Reservation Management supporter helping {wrapper.context.name}.
    Customer tier: {wrapper.context.tier} {"(Premium Shipping)" if wrapper.context.tier != "basic" else ""}
    
    YOUR ROLE: Handle reservation-related questions, availability, changes, and cancellations.
    Reservation questions
    - "I want to make a reservation for [date/time]", "Can I change my reservation?", "I need to cancel my reservation"
    
    RESERVATION INFORMATION TO PROVIDE:
    - Current reservation status and details
    - Availability information for specific dates and times
    - Options for changing or canceling reservations

    """


reservation_agent = Agent(
    name="Reservation Support Agent",
    instructions=dynamic_reservation_agent_instructions,
)