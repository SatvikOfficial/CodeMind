import hashlib
from typing import Any

import numpy as np
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pinecone import Pinecone
from transformers import AutoModel, AutoTokenizer
import torch

from app.config import get_settings

settings = get_settings()


tokenizer = AutoTokenizer.from_pretrained(settings.embedding_model)
encoder_model = AutoModel.from_pretrained(settings.embedding_model)


class AIEngine:
    def __init__(self) -> None:
        self.llm = None
        if settings.nvidia_api_key:
            self.llm = ChatOpenAI(
                api_key=settings.nvidia_api_key,
                base_url=settings.nvidia_base_url,
                model=settings.nvidia_model,
                temperature=0.1,
            )

        self.pinecone_index = None
        if settings.pinecone_api_key and settings.pinecone_host:
            pc = Pinecone(api_key=settings.pinecone_api_key)
            self.pinecone_index = pc.Index(host=settings.pinecone_host)

    def generate_embedding(self, code: str) -> np.ndarray:
        inputs = tokenizer(code, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = encoder_model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze(0)
        return embedding.cpu().numpy()

    def find_similar_code(self, embedding: np.ndarray) -> list[dict[str, Any]]:
        if not self.pinecone_index:
            return []

        response = self.pinecone_index.query(vector=embedding.tolist(), top_k=5, include_metadata=True)
        return response.get("matches", [])

    async def _run_prompt(self, prompt: str, fallback: list[str]) -> list[str]:
        if not self.llm:
            return fallback

        output = await self.llm.ainvoke(prompt)
        lines = [line.strip("- ") for line in output.content.splitlines() if line.strip()]
        return lines[:5] if lines else fallback

    async def analyze(self, code: str, language: str) -> dict[str, Any]:
        embedding = self.generate_embedding(code)
        similar = self.find_similar_code(embedding)

        digest = hashlib.sha1(code.encode()).hexdigest()[:8]
        similar_summary = ", ".join([m.get("id", "unknown") for m in similar]) or "none"

        suggestions_prompt = PromptTemplate.from_template(
            """
            You are a senior reviewer. Provide concise maintainability suggestions for this {language} code.
            Similar patterns: {similar}
            Code:
            {code}
            """
        ).format(language=language, code=code, similar=similar_summary)

        bugs_prompt = PromptTemplate.from_template(
            """
            Find likely bugs and security risks in this {language} snippet. Keep answers brief.
            Code:
            {code}
            """
        ).format(language=language, code=code)

        perf_prompt = PromptTemplate.from_template(
            """
            Suggest runtime and memory optimizations for this {language} snippet.
            Code:
            {code}
            """
        ).format(language=language, code=code)

        suggestions = await self._run_prompt(
            suggestions_prompt,
            [
                "Add explicit input validation and fail-fast error handling.",
                "Extract repeated logic into small pure functions for easier testing.",
            ],
        )
        bugs = await self._run_prompt(
            bugs_prompt,
            [
                "Potential unchecked null/undefined access in control paths.",
                "Missing authentication/authorization checks around sensitive operations.",
            ],
        )
        optimizations = await self._run_prompt(
            perf_prompt,
            [
                "Avoid repeated heavy computation by memoizing deterministic results.",
                "Batch IO-bound calls and parallelize independent async operations.",
            ],
        )

        documentation = (
            f"Code fingerprint `{digest}` in {language}.\n"
            "This snippet was analyzed for maintainability, security, and performance.\n"
            "Recommended next step: add focused tests for risky branches before refactors."
        )

        raw_score = 1.0 - min(0.8, len(bugs) * 0.2)
        score = max(0.05, round(raw_score, 2))

        return {
            "suggestions": suggestions,
            "bugs": bugs,
            "optimizations": optimizations,
            "documentation": documentation,
            "score": score,
            "embedding": embedding.tolist(),
        }
