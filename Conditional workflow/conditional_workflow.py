# imports
import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from langchain_docling import DoclingLoader
from langchain_text_splitters import TokenTextSplitter
from langchain_huggingface import  HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()

# embedding model
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# RAG
def build_retriever(PDF_PATH : str):
    loader = DoclingLoader(PDF_PATH)
    document = loader.load()

    splitter = TokenTextSplitter(
        chunk_size = 512,
        chunk_overlap = 50
    )

    chunks = splitter.split_documents(document)

    vectorstore = FAISS.from_documents(chunks,embeddings)

    return vectorstore.as_retriever(search_kwargs = {"k" : 4})

academic_retriever = build_retriever("academics_handbook.pdf")
fee_retriever = build_retriever("fee_structure.pdf")

llm = ChatGroq(model = "openai/gpt-oss-120b", temperature=0.4)

# State
class State(TypedDict):
    programme : str
    messages : Annotated[list,add_messages]
    query_type : str
    retrieved_context : str

# Node generation
def classifier_node(state : State) -> dict:
    """Look at the user message and decide which path to take."""

    last_message = state["messages"][-1].content

    prompt = (
        "Classify the following student query into exactly one category: "
        "'academic', 'fee', or 'general'.\n\n"
        "Use 'academic' for questions about attendance, exams, grading, credits, "
        "promotion, course structure, summer training, or degree requirements.\n"
        "Use 'fee' for questions about tuition, payment, refund, late charges, "
        "scholarships, or any money-related topic.\n"
        "Use 'general' for greetings, casual talk, or anything not related to "
        "the college rules or fee.\n\n"
        f"Query: {last_message}\n\n"
        "Return only one word: academic, fee, or general."
    )

    response = llm.invoke(prompt)
    category = response.content.strip().lower()

    if "academic" in category:
        category = "academic_rag_node"
    elif "fee" in category:
        category = "fee_rag_node"
    else :
        category = "general_node"

    return {"query_type" : category}

def academic_rag_node(state: State) -> dict:
    """Retrieves relevant chunks from the academics handbook."""
    query = state["messages"][-1].content
    docs = academic_retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    return {"retrieved_context": context}

def fee_rag_node(state: State) -> dict:
    """Retrieves relevant chunks from the fee structure PDF."""
    query = state["messages"][-1].content
    docs = fee_retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in docs])
    return {"retrieved_context": context}

def general_node(state: State) -> dict:
    """Answers directly using the LLM's own knowledge, no retrieval needed."""
    return {"retrieved_context": "NO_RETRIEVAL_NEEDED"}

def response_node(state: State) -> dict:
    """Generates the final answer, personalized using the student's programme."""
    query = state["messages"][-1].content
    programme = state.get("programme", "Unknown")
    context = state["retrieved_context"]

    if context == "NO_RETRIEVAL_NEEDED":
        prompt = (
            f"You are a friendly college assistant talking to a {programme} student. "
            f"Answer this question using your own general knowledge:\n\n{query}"
        )
    else:
        prompt = (
            f"You are a college assistant helping a {programme} student. "
            f"Use the following context from the official college documents to answer "
            f"the question accurately. If the context mentions specific figures for "
            f"different programmes, highlight the one relevant to {programme} if possible.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n\n"
            f"Give a clear, friendly, and precise answer."
        )

    response = llm.invoke(prompt)
    return {"messages": [("ai", response.content.strip())]}

# Router function

def route_query(state : State) :
    if state["query_type"] == "academic" :
        return "academic_rag_node"
    elif state["query_type"] == "fee" :
        return "fee_rag_node"
    else :
        return "general_node"

# Building the graph

graph = StateGraph(State)

graph.add_node("classifier_node",classifier_node)
graph.add_node("academic_rag_node",academic_rag_node)
graph.add_node("fee_rag_node",fee_rag_node)
graph.add_node("general_node",general_node)
graph.add_node("response_node",response_node)

graph.add_edge(START,"classifier_node")

graph.add_conditional_edges("classifier_node",route_query)

graph.add_edge("academic_rag_node","response_node")
graph.add_edge("fee_rag_node","response_node")
graph.add_edge("general_node","response_node")

graph.add_edge("response_node",END)

#step 6 - Run the code 
app = graph.compile()