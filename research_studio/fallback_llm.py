import logging
from typing import AsyncGenerator

from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

logger = logging.getLogger(__name__)


class FallbackLlm(BaseLlm):
    """Tries the primary model. If it fails before replying, uses the fallback."""

    primary: BaseLlm
    fallback: BaseLlm

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        started = False
        try:
            req = llm_request.model_copy()
            req.model = self.primary.model
            async for resp in self.primary.generate_content_async(req, stream=stream):
                started = True
                yield resp
            return
        except Exception as e:
            if started:
                raise  # already sent partial output, so don't switch mid-answer
            logger.warning("Primary model failed (%s). Using fallback.", e)

        req = llm_request.model_copy()
        req.model = self.fallback.model
        async for resp in self.fallback.generate_content_async(req, stream=stream):
            yield resp