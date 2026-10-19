from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

from src.my_agent.core.confing import Settings
from src.my_agent.services.agent.create_llm import create_llm


def get_system_prompt():
    return "Ты ии помощник для написания кода. Всегда отвечай кратко"


class AgentModule:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.model = create_llm(
            provider=self.settings.cur_llm_provider,
            api_key=self.settings.cur_llm_api_key,
            base_url=self.settings.cur_llm_base_url,
            model=self.settings.cur_llm_model,
            temperature=self.settings.cur_llm_temperature,
        )
        self.history: list[BaseMessage] = [
            SystemMessage(content=get_system_prompt()),
        ]

    def _update_history(self, item: BaseMessage):
        self.history.append(item)
        self.history = [self.history[0]] + self.history[1:][-10:]

    async def get_answer(self, query: str):
        self._update_history(HumanMessage(content=query))
        response = await self.model.ainvoke(self.history)
        self._update_history(response)

        return self.history[-1].content

