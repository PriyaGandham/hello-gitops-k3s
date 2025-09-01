import os
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion

# Read values from environment variables
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

chat_completion_service_1 = AzureChatCompletion(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name="gpt-4o",
    service_id="gpt-4-service"
)

chat_completion_service_2 = AzureChatCompletion(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name="gpt-4o",
    service_id="gpt-4-service"
)


chat_completion_service_1 = AzureChatCompletion(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name="gpt-4o",
    service_id = "gpt-4-service"
)

chat_completion_service_2 = AzureChatCompletion(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name="gpt-4o",
    service_id = "gpt-4-service"
)

chat_completion_service_3 = AzureChatCompletion(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name="gpt-4o",
    service_id = "gpt-4-service"
)

chat_completion_service_4 = AzureChatCompletion(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name="gpt-4o",
    service_id = "gpt-4-service"
)

chat_completion_service_5 = AzureChatCompletion(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name="gpt-4o",
    service_id = "gpt-4-service"
)

chat_completion_service_6 = AzureChatCompletion(
    api_key=api_key,
    endpoint=endpoint,
    deployment_name="gpt-4o",
    service_id = "gpt-4-service"
)


# import os
# from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion

# # Read values from environment variables
# api_key = os.getenv("AZURE_OPENAI_API_KEY")
# endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

# chat_completion_service_1 = AzureChatCompletion(
#     api_key=api_key,
#     endpoint=endpoint,
#     deployment_name="gpt-4o",
#     service_id="gpt-4-service"
# )

# chat_completion_service_2 = AzureChatCompletion(
#     api_key=api_key,
#     endpoint=endpoint,
#     deployment_name="gpt-4o",
#     service_id="gpt-4-service"
# )


# chat_completion_service_1 = AzureChatCompletion(
#     api_key=api_key,
#     endpoint=endpoint,
#     deployment_name="gpt-4o",
#     service_id = "gpt-4-service"
# )

# chat_completion_service_2 = AzureChatCompletion(
#     api_key=api_key,
#     endpoint=endpoint,
#     deployment_name="gpt-4o",
#     service_id = "gpt-4-service"
# )

# chat_completion_service_3 = AzureChatCompletion(
#     api_key=api_key,
#     endpoint=endpoint,
#     deployment_name="gpt-4o",
#     service_id = "gpt-4-service"
# )

# chat_completion_service_4 = AzureChatCompletion(
#     api_key=api_key,
#     endpoint=endpoint,
#     deployment_name="gpt-4o",
#     service_id = "gpt-4-service"
# )

# chat_completion_service_5 = AzureChatCompletion(
#     api_key=api_key,
#     endpoint=endpoint,
#     deployment_name="gpt-4o",
#     service_id = "gpt-4-service"
# )

# chat_completion_service_6 = AzureChatCompletion(
#     api_key=api_key,
#     endpoint=endpoint,
#     deployment_name="gpt-4o",
#     service_id = "gpt-4-service"
# )

