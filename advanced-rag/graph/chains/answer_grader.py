from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI


class GraderAnswer(BaseModel):
    binary_score: bool = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )


llm = ChatOpenAI(temperature=0)
structured_llm_grader = llm.with_structured_output(GraderAnswer)

system = """
    You are a grader assessing whether an answer addresse/ resolves a question \n
    Give a binary score 'yes' or 'no'. Yes means the answer resolves the question
"""

answer_prompt= ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "User question:\n\n {question} \n\n LLM generation: {generation}")
    ]

)

answer_grader: RunnableSequence = answer_prompt | structured_llm_grader