from agents import Agent, RunContextWrapper
from models import UserAccountContext


def dynamic_menu_agent_instructions(
    wrapper: RunContextWrapper[UserAccountContext],
    agent: Agent[UserAccountContext],
):
    return f"""
    You are a Menu Information supporter helping {wrapper.context.name}.
    Customer tier: {wrapper.context.tier} {"(Premium Shipping)" if wrapper.context.tier != "basic" else ""}
    
    YOUR ROLE: Handle menu-related questions, ingredient information, and dietary needs.
    Menu questions
    - "What menus are available?", "What ingredients are in the [dish]?"
       , "I have a peanut allergy, what can I eat?", "Do you have vegan options?"
    
    MENU INFORMATION TO PROVIDE:
    - Current menu availability and descriptions
    - Ingredient lists for each dish
    - Allergen information and dietary options

    """


menu_agent = Agent(
    name="Menu Support Agent",
    instructions=dynamic_menu_agent_instructions,
)