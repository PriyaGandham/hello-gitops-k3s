from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion
from semantic_kernel.contents import FunctionCallContent, FunctionResultContent
from semantic_kernel.contents.chat_message_content import ChatMessageContent

from sentence_transformers import SentenceTransformer
from azure.search.documents.models import VectorizedQuery

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from semantic_kernel.filters import FilterTypes, AutoFunctionInvocationContext
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

from search_plugin import SearchPlugin
from criteria_plugin import CriteriaPlugin
from pod_plugin import PODPlugin

from semantic_kernel.kernel import KernelArguments

from services import (
    chat_completion_service_1,
    chat_completion_service_2,
    chat_completion_service_3,
    chat_completion_service_4,
    chat_completion_service_5,
    chat_completion_service_6
)

from agent_prompts import (
#    phasing_agent_instructions, 
#    resourcing_agent_instructions, 
    summarizer_agent_instructions,
    master_agent_instructions,
    master_agent_sd_instructions,
    costing_agent_instructions
)

from agent_prompts_2 import (
    thinking_agent_instructions,
    phasing_agent_instructions,
    resourcing_agent_instructions
)


'''
aoai_endpoint = ""
aoai_api_key = ""
embedding_deployment = "text-embedding-ada-002"  # e.g., "text-embedding-ada"
embedding_model_name = "text-embedding-ada-002"

search_service_endpoint = ""
search_api_key = ""
index_name = ""
credential = AzureKeyCredential(search_api_key)

search_client = SearchClient(endpoint=search_service_endpoint, index_name=index_name, credential=credential)
'''

class FunctionInvokeSequence:
    def __init__(self):
        self.function_name = []
        self.function_call_content = []
        self.function_result = []

    def capture(self, context):
        self.function_name.append(context.function.name)
        self.function_call_content.append(context.function_call_content)
        self.function_result.append(context.function_result)

    def display(self):
        for i, name in enumerate(self.function_name):
            print(f"squence : {i} --> name : {name}")


############## Thinking Agent #######################

kernel_thinking = Kernel()
kernel_thinking.add_plugin(
    plugin_name='criteria_plugin',
    plugin=CriteriaPlugin(
        file_path='./service_catalogue/complexity_criterias.xlsx', 
        #description = description
    )
)

thinking_agent = ChatCompletionAgent(
    name="ThinkingArchitect",
    service = chat_completion_service_5,
    kernel = kernel_thinking,
    instructions= thinking_agent_instructions
)

############### Thinking Agent ##########################

########### Phasing Agent ###################
'''
kernel_phasing = Kernel()
kernel_phasing.add_plugin(
    SearchPlugin(
        search_client = search_client,
        aoai_endpoint = aoai_endpoint,
        aoai_api_key = aoai_api_key,
        embedding_deployment = embedding_deployment
    ),
    plugin_name="search_plugin"
)

sequence_phasing = FunctionInvokeSequence()
@kernel_phasing.filter(FilterTypes.AUTO_FUNCTION_INVOCATION)
async def raw_output_filter(context: AutoFunctionInvocationContext, next):
    await next(context)
    sequence_phasing.capture(context)
'''

phasing_agent = ChatCompletionAgent(
    name="PhasingAgent",
    instructions=phasing_agent_instructions,
    service = chat_completion_service_1,
#    kernel = kernel_phasing,
    function_choice_behavior=FunctionChoiceBehavior.Auto(
        maximum_auto_invoke_attempts = 1
    )
)

#################### Phasing Agent ################################


########### Resourcing Agent ##################

kernel_resourcing = Kernel()
kernel_resourcing.add_plugin(
    plugin = PODPlugin(file_path = "./service_catalogue/poc_resources.xlsx"),
    plugin_name = "pod_plugin"
)

sequence_resourcing = FunctionInvokeSequence()
@kernel_resourcing.filter(FilterTypes.AUTO_FUNCTION_INVOCATION)
async def raw_output_filter(context: AutoFunctionInvocationContext, next):
    await next(context)
    sequence_resourcing.capture(context)

resourcing_agent = ChatCompletionAgent(
    name="ResourcingAgent",
    instructions=resourcing_agent_instructions,
    service=chat_completion_service_2,
    kernel = kernel_resourcing,
    #function_choice_behavior=FunctionChoiceBehavior.Auto(
    #    maximum_auto_invoke_attempts = 1
    #)
)

########### Resourcing Agent ##################


########### Costing Agent #####################

kernel_costing = Kernel()
sequence_costing = FunctionInvokeSequence()
@kernel_costing.filter(FilterTypes.AUTO_FUNCTION_INVOCATION)
async def raw_output_filter(context: AutoFunctionInvocationContext, next):
    await next(context)
    sequence_costing.capture(context)

costing_agent = ChatCompletionAgent(
    name="CostingAgent",
    instructions=costing_agent_instructions,
    service=chat_completion_service_6,
    kernel = kernel_costing,
    function_choice_behavior=FunctionChoiceBehavior.Auto(
        maximum_auto_invoke_attempts = 1
    )
)

############# Costing Agent ###########################


########### Summarizer Agent ###################

summarizer_agent = ChatCompletionAgent(
    name="SummarizerAgent",
    instructions=summarizer_agent_instructions,
    service=chat_completion_service_3
)

########### Summarizer Agent ###################


########## Master Agent #####################

@kernel_function(name="self_dialouge", description="Engage in deep architectural self-dialogue to refine the problem understanding.")
async def get_self_dialogue_summary(problem: str) -> str:
    response = await thinking_agent.get_response(messages = problem)
    text = str(response)
    print("-------------------------Self Dialouge -----------------------")
    print(response)
    print("--------------------------------------------------------------")
    
    summary_start = text.find("=== Summary ===")
    if summary_start != -1:
        summary = text[summary_start:].strip()
    else:
        summary = text
    return summary.strip("=== Summary ===")

@kernel_function(name="run_phasing", description="phasing agent to produce task breakdown, timeline and gantt chart.")
async def run_phasing(project_input: str) -> str:
    async for resp in phasing_agent.invoke(project_input):
        return resp.content
    return ""

@kernel_function(name="run_resourcing", description="resourcing agent to produce required roles based on phasing output.")
async def run_resourcing(phasing_output: str) -> str:
    async for resp in resourcing_agent.invoke(phasing_output):
        return resp.content
    return ""

@kernel_function(name="run_costing", description="costing agent to produce phase-wise costing estimates.")
async def run_costing(resource_output: str) -> str:
    async for resp in costing_agent.invoke(resource_output):
        return resp.content
    return ""

@kernel_function(name="run_summarizer", description="summarizer agent to produce a concise project overview from phasing and resourcing outputs.")
async def run_summarizer(phasing_output: str, resourcing_output: str) -> str:
    async for resp in summarizer_agent.invoke(f"Phasing Output:\n{phasing_output}\n\nResourcing Output:\n{resourcing_output}"):
        return resp.content
    return ""

kernel_master = Kernel()
kernel_master.add_function(plugin_name="self_dialouge", function=get_self_dialogue_summary)
kernel_master.add_function(plugin_name="run_phasing", function=run_phasing)
kernel_master.add_function(plugin_name="run_resourcing", function=run_resourcing)
kernel_master.add_function(plugin_name="run_costing", function=run_costing)
kernel_master.add_function(plugin_name="run_summarizer", function=run_summarizer)

sequence_master = FunctionInvokeSequence()
@kernel_master.filter(FilterTypes.AUTO_FUNCTION_INVOCATION)
async def raw_output_filter(context: AutoFunctionInvocationContext, next):
    await next(context)
    sequence_master.capture(context)

master_agent = ChatCompletionAgent(
    name="MasterAgent",
    instructions=master_agent_sd_instructions,
    service=chat_completion_service_4,
    kernel=kernel_master,
    #function_choice_behavior=FunctionChoiceBehavior.Auto(
    #    maximum_auto_invoke_attempts = 5
    #)
)

############## Master Agent ##################################