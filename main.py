from retriever import get_retriever
from llm import get_llm
from prompt import rag_prompt
from format import format_docs
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_core.output_parsers import StrOutputParser


def Rag_chain():
    retriever = get_retriever()
    llm = get_llm()
    parser = StrOutputParser()

    parallel_runnable = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    rag_chain = parallel_runnable | rag_prompt | llm | parser
    return rag_chain

# if __name__ == "__main__":
#     rag = Rag_chain()
#     question = input("Enter your question: ")
#     answer = rag.invoke(question)
#     print(f"Q: {question}\nA: {answer}")