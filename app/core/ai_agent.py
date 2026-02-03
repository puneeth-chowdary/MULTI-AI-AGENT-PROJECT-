from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from app.config.settings import settings

def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):
    llm = ChatGroq(
        model=llm_id,
        api_key=settings.GROQ_API_KEY
    )

    tools = [TavilySearchResults(max_results=3)] if allow_search else []

    # ✅ CORRECT for your LangGraph version
    agent = create_react_agent(llm, tools)

    # ✅ System prompt injected via messages
    state = {
        "messages": [
            ("system", system_prompt),
            *[("user", q) for q in query]
        ]
    }

    response = agent.invoke(state)

    messages = response.get("messages", [])

    ai_messages = [
        message.content
        for message in messages
        if isinstance(message, AIMessage)
    ]

    return ai_messages[-1] if ai_messages else None
