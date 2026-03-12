from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv
import os

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import AIMessage

class Summarizer:
    def __init__(self):
        self.name = "Summarizer"
        load_dotenv()
        self.model = ChatOpenAI(
            name="gpt-5.2",
            api_key=os.environ["OPENAI_API_KEY"]
        )
        self.tools = self._get_tools()
        self.checkpointer = InMemorySaver()
        self.system_prompt = self._get_system_prompt()

        self.agent = create_agent(
            model=self.model,
            tools=self.tools,
            checkpointer=self.checkpointer,
            system_prompt=self.system_prompt
        )
        print(f"[DEBUG] {self.name} Agent Created Successfully")

    def invoke(self, input: str = "Summarize and store the provided notes.", threadid: str | None = None):
        print(f"[DEBUG] Invoking {self.name} Agent")
        if threadid == None:
            threadid = uuid4()
        response = self.agent.invoke(
            {"messages": [("user", input)]},
            config={"configurable": {"thread_id": threadid}}
        )
        message = self._get_ai_text(response)
        return message

    def _get_tools(self):
        from tools.db_tools import (
            list_pending_inputs_tool,
            get_input_tool,
            set_input_status_tool,
            create_note_tool,
            get_note_by_input_id_tool,
            update_note_tool,
        )
        from tools.audio_to_text_tools import (
            transcribe_audio
        )

        tools = [
            list_pending_inputs_tool,
            get_input_tool,
            set_input_status_tool,
            create_note_tool,
            get_note_by_input_id_tool,
            update_note_tool,
            transcribe_audio
            ]
        return tools
    
    def _get_system_prompt(self):
        SYSTEM_PROMPT = Path("souls/summarizer_soul.md").read_text(encoding="utf-8")

    def _get_ai_text(self, resp):

        msgs = resp.get("messages") if isinstance(resp, dict) else getattr(resp, "messages", None)

        if not msgs:
            return ""

        for m in reversed(msgs):
            if isinstance(m, AIMessage):
                return m.content or ""

        return ""