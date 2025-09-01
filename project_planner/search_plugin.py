from azure.search.documents.models import VectorizedQuery
from azure.search.documents import SearchClient
from openai import AzureOpenAI
from semantic_kernel.functions import kernel_function
  
class SearchPlugin:
 
    def __init__(
        self,
        search_client: SearchClient,
        aoai_endpoint: str,
        aoai_api_key: str,
        embedding_deployment: str,
    ):
        self.search_client = search_client
        self.embedding_deployment = embedding_deployment
 
        # Initialize Azure OpenAI client
        self.aoai_client = AzureOpenAI(
            api_key=aoai_api_key,
            api_version="2024-12-01-preview",
            azure_endpoint=aoai_endpoint,
        )
 
    def _get_embedding(self, text: str) -> list:
        try:
            response = self.aoai_client.embeddings.create(
                input=[text],
                model=self.embedding_deployment
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"⚠️ Embedding error: {e}")
            return []
 
    @kernel_function(
        name="build_augmented_prompt",
        description="Build an augmented prompt using retrieval context.",
    )
    def build_augmented_prompt(self, query: str, retrieval_context: str) -> str:
        return (
            f"Retrieved Context:\n{retrieval_context}\n\n"
            f"User Query: {query}\n\n"
        )
 
    @kernel_function(
        name="retrieve_documents",
        description="Retrieve documents from the Azure Search index",
    )
    def get_retrieval_context(self, query: str) -> str:
        # Step 1: Encode the query using Azure OpenAI
        query_vector = self._get_embedding(query)
        if not query_vector:
            return "⚠️ Error generating embedding for the query."
 
        # Step 2: Run vector search
        results = self.search_client.search(
            search_text="",
            vector_queries=[
                VectorizedQuery(
                    vector=query_vector,
                    fields="contentVector",
                    k_nearest_neighbors=5
                )
            ],
            select=["content"]
        )

        # Step 3: Aggregate results
        context_chunks = [f"Document: {r['content']}" for r in results]
        return "\n\n".join(context_chunks) if context_chunks else "No results found"
 