# backend/agents/agent_chain.py
import os, json
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA

from agents.health_chain import run_health_chain
from agents.finance_chain import run_finance_chain
from agents.llm_chat import FreeLLMWrapper
from memory.vector_memory import get_task_vector_memory, save_vector_memory
from utils.ipfs import store_task_on_ipfs, fetch_task_from_ipfs
from utils.blockchain import store_task, get_task_proof

def get_aidpa_agent():
    retriever = get_task_vector_memory()

    def get_task_content(task_id: str) -> str:
        try:
            proof = get_task_proof(task_id)
            if not proof:
                return "❌ No IPFS proof found."
            task_data = fetch_task_from_ipfs(proof)
            return json.dumps(task_data, indent=2)
        except Exception as e:
            return f"❌ Failed to fetch task content: {str(e)}"

    def store_task_to_chain(task_json_str: str) -> str:
        try:
            task_dict = json.loads(task_json_str)
            ipfs_hash = store_task_on_ipfs(task_dict)
            task_id = str(task_dict.get("id", "unknown"))
            store_task(task_id, ipfs_hash)
            save_vector_memory()
            return f"✅ Task stored with IPFS hash: {ipfs_hash}"
        except Exception as e:
            return f"❌ Failed to store task: {str(e)}"

    tools = [
        Tool(
            name="Health Recommendation Chain",
            func=run_health_chain,
            description="Use this tool to get JSON-based health recommendations for hydration, meals, and steps."
        ),
        Tool(
            name="Finance Advisor",
            func=run_finance_chain,
            description="Use this to get personalized financial insights."
        ),
        Tool(
            name="Store Task to Blockchain",
            func=store_task_to_chain,
            description="Use this to store a user task with ID and content on the blockchain via IPFS."
        ),
        Tool(
            name="Verify Task Hash",
            func=lambda task_id: get_task_proof(task_id),
            description="Use this to verify a task's IPFS hash from the blockchain using task ID."
        ),
        Tool(
            name="Get Task Content",
            func=get_task_content,
            description="Use this to fetch the full task details from IPFS using the task ID."
        ),
        Tool(
            name="Task Search",
            func=RetrievalQA.from_chain_type(llm=FreeLLMWrapper(), retriever=retriever).run,
            description="Use this to search for task-related info using semantic memory."
        ),
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are AIDPA, a helpful assistant for tasks, health, and finance. Use tools if needed."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    agent = create_tool_calling_agent(
        llm=FreeLLMWrapper(),
        tools=tools,
        prompt=prompt
    )

    return AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

# CLI
if __name__ == "__main__":
    agent = get_aidpa_agent()
    print("🤖 AIDPA Agent Ready")
    while True:
        try:
            msg = input("You: ")
            if msg.lower() in {"exit", "quit"}:
                break
            out = agent.invoke({"input": msg})
            print("AIDPA:", out["output"])
        except Exception as e:
            print("❌ Error:", str(e))