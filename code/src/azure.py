from typing import List, Dict

from openai import AsyncAzureOpenAI, AzureOpenAI


class AsyncAzureChatLLM:
    """
    Wrapper for an (Async) Azure Chat Model.
    """
    def __init__(
        self, 
        api_key: str, 
        azure_endpoint: str, 
        api_version: str, 
        ):
        """
        Initializes AsyncAzureOpenAI client.
        """
        self.client = AsyncAzureOpenAI(
            api_version=api_version,
            api_key=api_key,
            azure_endpoint=azure_endpoint,
        )

    @property
    def llm_type(self):
        return "AsyncAzureOpenAI"

    async def __call__(self, 
        messages: List[Dict[str, str]], 
        **kwargs,
    ):
        """
        Make an async API call.
        """
        return await self.client.chat.completions.create(
            messages=messages, 
            **kwargs)

class AzureChatLLM:
    """
    Wrapper for an (Async) Azure Chat Model.
    """
    def __init__(
        self, 
        api_key: str, 
        azure_endpoint: str, 
        api_version: str, 
        azure_deployment: str,
        ):
        """
        Initializes AzureOpenAI client.
        """
        self.client = AzureOpenAI(
            api_version=api_version,
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment,
        )

    @property
    def llm_type(self):
        return "AzureOpenAI"

    def __call__(self, 
        messages: List[Dict[str, str]], 
        **kwargs,
    ):
        """
        Make an async API call.
        """
        return self.client.chat.completions.create(
            messages=messages, 
            **kwargs)