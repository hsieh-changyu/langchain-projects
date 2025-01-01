from typing import Any, Tuple
from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
    create_tool_calling_agent,
)
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()


def anslysis_python():
    print("Start Python Interpreter...")

    instructions = """You are an agent designed to write and execute python code to answer questions.
    You have access to a python REPL, which you can use to execute python code.
    If you get an error, debug your code and try again.
    Only use the output of your code to answer the question. 
    You might know the answer without running any code, but you should still run the code to get the answer.
    If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
    """
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instructions)

    tools = [PythonREPLTool()]
    agent = create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
        tools=tools,
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    agent_executor.invoke(
        input={
            "input": """
                    Please generate and save in current working directory for 10 QRcodes
                    that point to https://github.com/hsieh-changyu/langchang-projects, you have qrcode package installed already
                """
        }
    )


def analysis_csv():
    csv_agent = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
        path="book_levels.csv",
        verbose=True,
        allow_dangerous_code=True,
    )

    csv_agent.invoke(
        input={"input": "how many different language levels in book_level.csv"}
    )
    csv_agent.invoke(
        input={"input": "Please summary the number of books for each author"}
    )


def construct_python_agent() -> tuple[AgentExecutor, Any]:
    instructions = """You are an agent designed to write and execute python code to answer questions.
    You have access to a python REPL, which you can use to execute python code.
    If you get an error, debug your code and try again.
    Only use the output of your code to answer the question. 
    You might know the answer without running any code, but you should still run the code to get the answer.
    If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
    """
    tools = [PythonREPLTool()]
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instructions)

    agent = create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
        tools=tools,
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return (agent_executor, prompt)


def construct_csv_agent() -> AgentExecutor:
    csv_agent = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
        path="book_levels.csv",
        verbose=True,
        allow_dangerous_code=True,
    )
    return csv_agent


def main():

    python_agent_executor, prompt = construct_python_agent()

    def python_agent_executor_wrapper(original_prompt: str) -> dict[str, Any]:
        return python_agent_executor.invoke({"input": original_prompt})

    tools = [
        Tool(
            name="Python Agent",
            func=python_agent_executor_wrapper,
            description="""useful when you need to transform natural language to python and execute the python code,
                          returning the results of the code execution
                          DOES NOT ACCEPT CODE AS INPUT""",
        ),
        Tool(
            name="CSV Agent",
            func=construct_csv_agent().invoke,
            description="""useful when you need to answer question over ebook_levels.csv file,
                         takes an input the entire question and returns the answer after running pandas calculations""",
        ),
        Tool(
            name="Tavily Search Agent",
            func=TavilySearchResults().invoke,
            description="""Useful for fetching real-time information, such as current weather or other search queries.""",
        ),
    ]

    grand_agent = create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
        tools=tools,
    )
    grand_agent_executor = AgentExecutor(agent=grand_agent, tools=tools, verbose=True)

    # print(
    #     grand_agent_executor.invoke(
    #         {
    #             "input": "what is the current weather in Taipei right now? compare it with Shanghai, output should in in celsious",
    #         }
    #     )
    # )

    print(
        grand_agent_executor.invoke(
            {
                "input": "Find the number of books published for each author, and sort in the descending order?",
            }
        )
    )

    print(
        grand_agent_executor.invoke(
            {
                "input": "Generate and save in current working directory 10 qrcodes that point to `https://github.com/hsieh-changyu/langchain-projects`",
            }
        )
    )


if __name__ == "__main__":
    main()
    # analysis_csv()
