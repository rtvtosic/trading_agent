import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from load_data import get_technical_analysis


load_dotenv()

# 1) определяем состояние (STATE)
class State(TypedDict):
    messages: Annotated[list, add_messages]


# 2) инициализация модели и инструментов
llm = ChatMistralAI(
    api_key=os.getenv("MISTRAL_API_KEY"),
    model='open-mistral-nemo-2407',
    temperature=0
)

tools = [get_technical_analysis]
llm_with_tools = llm.bind_tools(tools)


# 3) определение узлов
def chatbot(state: State):
    """узел, который вызывает LLM"""
    return {"messages": [llm_with_tools.invoke(state['messages'])]}

# узел, который сам вызывает инструменты
tool_node = ToolNode(tools)


# 4) логика переходов (conditional edges)
def should_continue(state: State):
    """Решает, нужно ли вызывать инстурмент 
    или можно закончить"""

    last_message = state['messages'][-1]

    if last_message.tool_calls:
        return "tools"
    
    return END


# 5) сборка графа
workflow = StateGraph(State)

# добавление узлов
workflow.add_node("agent", chatbot)
workflow.add_node("tools", tool_node)

# установка точки входа
workflow.set_entry_point("agent")


# === добавление связей ===
# из узла agent мы идем по ребру should_continue
workflow.add_conditional_edges(
    "agent",
    should_continue
)

# возвращаемся из tools в agent для анализа ответа
workflow.add_edge("tools", "agent")


# компиляция графа
app = workflow.compile()

with open("graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

if __name__ == "__main__":
    message = "Проведи аналитику актива BTC/USDT"
    inputs = {
        "messages": [
            ("user", message)
        ]
    }

    for output in app.stream(inputs):
        #print(output)
        for key, value in output.items():
            print(f"\n--- Node: {key} ---")
            if "messages" in value:
                print(value['messages'][-1].content)
