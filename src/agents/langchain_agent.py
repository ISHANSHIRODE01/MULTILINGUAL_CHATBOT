from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

class MultilingualAgent:
    def __init__(self, openai_api_key: str):
        self.llm = OpenAI(openai_api_key=openai_api_key)
        self.memory = ConversationBufferMemory()
        self.tools = self._setup_tools()
        self.agent = initialize_agent(
            self.tools, 
            self.llm, 
            agent="conversational-react-description",
            memory=self.memory
        )
    
    def _setup_tools(self):
        return [
            Tool(
                name="Translate",
                func=self._translate_tool,
                description="Translate text between languages"
            ),
            Tool(
                name="Grammar Check",
                func=self._grammar_tool,
                description="Check grammar and provide corrections"
            )
        ]
    
    def _translate_tool(self, query: str) -> str:
        # Integration with translation service
        return f"Translated: {query}"
    
    def _grammar_tool(self, query: str) -> str:
        # Integration with grammar checking
        return f"Grammar feedback for: {query}"
    
    def chat(self, message: str) -> str:
        return self.agent.run(message)