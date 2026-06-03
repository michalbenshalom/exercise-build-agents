import os
import subprocess
from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


llm = ChatOllama(
    model="qwen3",
    temperature=0
)

@tool
def get_git_blame(file_path: str, line_number: int) -> str:
    """
    Get the author and commit date of a specific line in a file.
    """

    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' not found."

    try:
        cmd = ["git","blame", "-L", f"{line_number},{line_number}", "--porcelain", file_path]
        result = subprocess.run( cmd, capture_output=True, text=True, check=True)

        author = "Unknown"
        commit_time = "Unknown"

        for line in result.stdout.splitlines():

            if line.startswith("author "):
                author = line.replace("author ", "").strip()

            elif line.startswith("author-time "):
                commit_time = line.replace(
                    "author-time ",
                    ""
                ).strip()

        return (
            f"Author: {author}\n"
            f"Commit Time: {commit_time}"
        )

    except subprocess.CalledProcessError as ex:
        return f"Git error: {ex.stderr}"

    except Exception as ex:
        return f"Unexpected error: {str(ex)}"


# ==========================
# Tools
# ==========================

tools = [get_git_blame]

llm_with_tools = llm.bind_tools(tools)

tool_node = ToolNode(tools)


# ==========================
# Assistant Node
# ==========================

def assistant(state: MessagesState):

    team_context = ""
    if os.path.exists("team_context.txt"):
        with open("team_context.txt", "r", encoding="utf-8") as f:
            team_context = f.read()
    else:
        team_context = "לא נמצא מידע נוסף על הצוות."
    system_message = """
    אתה ארכיאולוג קוד.

    כאשר המשתמש שואל על קובץ או שורה,
    עליך להשתמש ב-tool get_git_blame.

    לאחר קבלת תוצאת ה-tool,
    הסבר למשתמש מי כתב את הקוד
    ומתי הוא נכתב.
    """

    messages = state["messages"]
    response = llm_with_tools.invoke(
        [
            ("system", system_message),
            *messages
        ]
    )

    return {
        "messages": [response]
    }

builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", tool_node)
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant",tools_condition)
builder.add_edge("tools", "assistant")
graph = builder.compile()


def run_agent(user_prompt: str):

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=user_prompt)
            ]
        }
    )

    print("\n===================")
    print("FINAL RESPONSE")
    print("===================\n")

    print(result["messages"][-1].content)


# ==========================
# Main
# ==========================

if __name__ == "__main__":
    print("Running agent with prompt: בדוק את שורה 5 בקובץ app.py")
    run_agent("בדוק את שורה 5 בקובץ app.py")