from semantic_kernel.contents import FunctionCallContent, FunctionResultContent
from semantic_kernel.contents.chat_message_content import ChatMessageContent

async def run_master_agent(master_agent, project_template, streamlit_instance):
    async def handle_intermediate_steps(message: ChatMessageContent) -> None:
        for item in message.items or []:
            if isinstance(item, FunctionCallContent):
                streamlit_instance.markdown(f"**FUNCTION_CALL**: {item.name} with arguments: {item.arguments}")
            elif isinstance(item, FunctionResultContent):
                streamlit_instance.markdown(f"**FUNCTION_RESULT**: {item.result} for function: {item.name}")
            else:
                streamlit_instance.markdown(f"**LLM**: {message.role}: {message.content}")
 
    async for response in master_agent.invoke(
        messages=project_template,
        on_intermediate_message=handle_intermediate_steps,
    ):
        streamlit_instance.markdown(f"**# {response.role}**: {response}")


def format_project_template(
    usecase_name, usecase_objectives, budget_constraints, expected_timeline, sensitivity_requirements, description
):
    template = f"""\
Name:
{usecase_name}
 
Objectives:
{usecase_objectives}
 
Budget Constraints:
* Total project budget: ${budget_constraints:,.2f}
 
Timeline (Interrelated with Resources):
* Project duration: {expected_timeline}
 
Sensitivity Requirements:
{sensitivity_requirements if sensitivity_requirements else 'None'}
 
Description:
{description if description else 'None'}
"""
    return template 