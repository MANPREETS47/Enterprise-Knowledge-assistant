from langchain_core.prompts import ChatPromptTemplate


rag_prompt = ChatPromptTemplate.from_messages(
	[
		("system",""" 
        You are an enterprise knowledge assistant. 
        Use ONLY the following context to answer the question. 
        If the answer is not in the context, say you don't know.
        <context>
        {context}
        </context>
        Answer clearly and cite sources if possible.
      """,
		),
		("human","""Question:{question}""",),
	]
)




