# agent.py
import os
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

api_base = os.getenv("EYQ_INCUBATOR_ENDPOINT")
api_key = os.getenv("EYQ_INCUBATOR_KEY")

if not api_base or not api_key:
    raise ValueError("As variáveis de ambiente EYQ_INCUBATOR_ENDPOINT e EYQ_INCUBATOR_KEY devem ser definidas.")

file_path = r"C:\Users\PS961MX\OneDrive - EY\Documents\eyq_incubator_sample_data.txt"

with open(file=file_path, mode='r') as file:  
    text = file.read()  

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

text_chunks = text_splitter.split_text(text)

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=api_base,
    api_key=api_key,
    azure_deployment="text-embedding-3-large",
    api_version="2024-06-01"
)

vectorstore = InMemoryVectorStore.from_texts(
    texts=text_chunks,
    embedding=embeddings
)

retriever = vectorstore.as_retriever()

def get_response(query):
    retrieved_documents = retriever.invoke(query)  
    retrieved_texts = [doc.page_content for doc in retrieved_documents]  

    llm = AzureChatOpenAI(
        azure_endpoint=api_base,
        api_key=api_key,
        azure_deployment="gpt-4o",
        api_version="2024-06-01",
        temperature=0.7,
        max_tokens=800
    )

    if len(retrieved_texts) > 1:
        retrieved_info = retrieved_texts[1]
    else:
        retrieved_info = "Desculpe, não consegui encontrar informações suficientes."

    messages = [  
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="What is EYQ Incubator?"), 
        AIMessage(content=f"Here is some information I found:\n\n{retrieved_info}\n\nDo you need more details?"),
        HumanMessage(content=query),
    ]
      
    ai_msg = llm.invoke(messages)
    return ai_msg.content
