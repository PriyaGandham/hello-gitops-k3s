from semantic_kernel.agents import ChatCompletionAgent, AgentGroupChat
from semantic_kernel.agents.strategies import (
    KernelFunctionSelectionStrategy,
    KernelFunctionTerminationStrategy,
)
from semantic_kernel.kernel import Kernel
from semantic_kernel.contents import AuthorRole, ChatMessageContent
from semantic_kernel.functions import KernelFunctionFromPrompt

from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

from criteria_plugin import CriteriaPlugin
from semantic_kernel.contents import ChatHistoryTruncationReducer

import re
from semantic_kernel.functions import kernel_function
import asyncio


def create_kernel_with_chat_completion() -> Kernel:
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            api_key="",
            endpoint="",
            deployment_name="gpt-4o",
            service_id = "gpt-4-service"
        )
    )
    return kernel


PLANNER_NAME = "PROJECT_PLANNER"
PLANNER_INSTRUCTIONS = """\
You are a senior project planner known for strategic thinking and efficient software selection.

Goal: Turn a project description into an actionable project proposal.

Tools:
- get_project_dimensions – Returns key project planning parameters to be considered.
- get_complexity_details – Returns criteria for classifying project complexity.
- ask_question – Use to clarify software preferences, unclear requirements, drawbacks or ambiguities.

Guidelines:
- Always ask questions via ask_question and wait for the answer before continuing.
- Use get_project_dimensions and get_complexity_details as needed to inform your planning.
- For softwares and services you are restricted to the pool of Azure ecosystem.
- The following should preferably be the high level project phases :\
Discovery, Analysis & Design, Development & Implementation, MVP testing.

Your final output must include:
- A concise strategy and methodology.
- A list of platforms and software required for execution.
- Inputs from the questions asked

Be clear, actionable, and well-organized.\
"""

@kernel_function(name = "ask_question", description= "Ask the question.")
def ask_question(question: str) -> str:
    return input(f"🧠 Planner needs clarification: {question}\nUSER INPUT :>")

kernel_writer = create_kernel_with_chat_completion()
kernel_writer.add_function("ask_user", ask_question)
kernel_writer.add_plugin(plugin_name = "criteria_pugin", plugin = CriteriaPlugin(
    file_path = "./service_catalogue/complexity_criterias.xlsx"
))

agent_writer = ChatCompletionAgent(
    kernel=kernel_writer,
    name=PLANNER_NAME,
    instructions=PLANNER_INSTRUCTIONS,
    function_choice_behavior=FunctionChoiceBehavior.Auto(maximum_auto_invoke_attempts = 20)
)

AUDITOR_NAME = "PROJECT_AUDITOR"
AUDITOR_INSTRUCTIONS = f"""\
You are a meticulous project auditor who specializes in finding gaps, inefficiencies or inconsistencies in project proposals.
Your role is to review proposals and determine whether they are ready to move into execution. To do this, you need to:

- Identify ambiguities or unclear assumptions in the approach.
- Flag missing or unnecessary softwares and suggest clarification.
- Check for the feasibility of softwares being selected.

If the plan is complete and solid, you clearly state that it is approved from your side.
If not, offer precise, concise, constructive feedback.

Your responses are authoritative, focused, and never repetitive.\
"""

agent_reviewer = ChatCompletionAgent(
    kernel=create_kernel_with_chat_completion(),
    name=AUDITOR_NAME,
    instructions=AUDITOR_INSTRUCTIONS,
)

termination_function = KernelFunctionFromPrompt(
    function_name="termination",
    prompt=f"""\
Determine if the review process is complete.

Guidelines:
- The process is complete when the {AUDITOR_NAME} approves the project proposal made by the {PLANNER_NAME}.
- Look for phrases that give a clear indication that the {AUDITOR_NAME} is satisfied.
- If the {AUDITOR_NAME} has given approval in their most recent response, respond with the term 'ACCEPTED'.
- Otherwise, respond with the term 'REJECTED'.

RESPONSE:
{{{{$history}}}}
"""
)

selection_function = KernelFunctionFromPrompt(
    function_name="selection",
    prompt=f"""\
Determine which participant takes the next turn in a conversation based on the most recent participant.

Choose only from these participants:
- {PLANNER_NAME}
- {AUDITOR_NAME}

Always follow these rules when selecting the next participant, each conversation should be at least 4 turns:
- After user input, it is {PLANNER_NAME}'s turn.
- After {PLANNER_NAME} replies, it is {AUDITOR_NAME}'s turn.
- After {AUDITOR_NAME} provides feedback, it is {PLANNER_NAME}'s turn.

RESPONSE:
{{{{$history}}}}
"""
)

def _result_parser_selection(result):
    result = str(result.value[0])
    if(result is not None):
        match = re.findall(r'\b[A-Z]+(?:_[A-Z]+)*\b', result)[0]
        return match
    else:
        return PLANNER_NAME
    
def _result_parser_termination(result):
    result = str(result.value[0])
    if(result is not None and 'accepted' in result.lower()):
        return True
    return False

history_reducer = ChatHistoryTruncationReducer(target_count=2)

chat = AgentGroupChat(
    agents=[agent_writer, agent_reviewer],
    termination_strategy=KernelFunctionTerminationStrategy(
        agents=[agent_reviewer],
        function=termination_function,
        kernel=create_kernel_with_chat_completion(),
        result_parser=_result_parser_termination,
        history_variable_name="history",
        history_reducer=history_reducer,
        maximum_iterations=10,
    ),
    selection_strategy=KernelFunctionSelectionStrategy(
        function=selection_function,
        kernel=create_kernel_with_chat_completion(),
        result_parser=_result_parser_selection,
        agent_variable_name="agents",
        history_variable_name="history",
        history_reducer=history_reducer,
    ),
)

async def run_orchestration():
    project_template = f"""\
    Project Name:
    Finance KPI RCA Chatbot POC.

    Project Description:
    Request to build a chatbot POC which will assist in performing the RCA for various finance KPIs.

    Agents:
    RCA Reasoning Agent, Finance Insights Summarizer.\
    """

    await chat.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=project_template))

    async for content in chat.invoke():
        print(f"### Agent - {content.name or '*'}: \n'{content.content}'")

    print(f"# IS COMPLETE: {chat.is_complete}")

if __name__ == "__main__":
    asyncio.run(run_orchestration())

