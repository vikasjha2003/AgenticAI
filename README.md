# AgenticAI

This repository is a small learning project focused on understanding different workflow patterns in LangGraph and agentic AI design.

I built these examples while exploring how LLM-based applications can be structured as graphs, with states, branching logic, tool use, human review, and retrieval. The goal was not to build a production-grade system, but to learn how different patterns work in practice.

## What this repo is about

This project contains a few small experiments that demonstrate common LangGraph patterns:

- Sequential workflow: a multi-step pipeline where one node passes output to the next
- Parallel workflow: multiple branches running at the same time and merging results into a single state
- Conditional workflow: routing queries based on intent and using different retrieval paths
- Human-in-the-loop workflow: pausing execution for user approval or feedback
- Iterative tool workflow: an LLM writing a draft, using tools when needed, then reviewing and retrying
- State patterns: simple examples showing different ways to manage state in LangGraph

These are intentionally beginner-friendly experiments, meant to make the ideas behind agentic systems easier to understand.

## Project examples

### 1. Sequential workflow
File: `sequential_workflow.py`

A simple three-stage pipeline:
- edit text
- convert it into a script
- translate it into Hinglish

This demonstrates how state can move from one step to another in a linear graph.

### 2. Parallel workflow
File: `parallel_workflow.py`

Three independent analysis branches run in parallel:
- toxicity
- copyright risk
- cultural sensitivity

The results are combined into a single state dictionary.

### 3. Conditional workflow + RAG
Folder: `Conditional workflow/`

This includes a college assistant example using:
- route classification
- academic vs fee query detection
- FAISS vector retrieval from PDF documents
- final answer generation using the retrieved context

This is a practical example of conditional routing and retrieval-augmented generation.

### 4. Human-in-the-loop workflow
File: `human_in_the_loop.py`

A LinkedIn post generator that pauses for manual review.

It:
- writes a draft
- asks for approval or feedback
- rewrites the post if needed
- stops after a fixed number of attempts

This shows how an agent can include human intervention in the loop.

### 5. Iterative tool workflow
File: `iterative_tools.py`

A more advanced writing workflow where the model can use a search tool, generate a draft, and then review/iterate based on feedback.

It demonstrates:
- tool calling
- draft extraction
- review and approval logic
- retry loops

### 6. State experiments
File: `state.py`

A small reference file covering different state representations in LangGraph and Python:
- TypedDict
- Pydantic model
- dataclass
- MessagesState

## Repository structure

```text
AgenticAI/
├── Conditional workflow/
│   ├── academics_handbook.pdf
│   ├── college_assistant.py
│   ├── conditional_workflow.py
│   └── fee_structure.pdf
├── human_in_the_loop.py
├── iterative_tools.py
├── parallel_workflow.py
├── requirements.txt
├── sequential_workflow.py
├── state.py
└── README.md
```

## Setup

1. Create a virtual environment
2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Add environment variables if required by the models or APIs you are using

For example, for Groq or Google/Gemini access, set your keys in a `.env` file:

```bash
GROQ_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

## Notes

This repo is more of a learning playground than a polished application. Most files are built to understand specific LangGraph concepts with minimal complexity.

A few examples here may require API keys and internet access depending on the model/tool used. The idea is to experiment, see how workflows behave, and gradually build a stronger mental model of agentic systems.

## Learning goal

The purpose of this project is simple:

- understand state-based workflows
- learn how graphs route execution
- understand tool use and retrieval
- experiment with human approval loops
- see how multi-step agent logic is constructed in practice

This repository is a personal step-by-step learning journey into LangGraph and agentic AI workflows.

## Future work

As this project grows, I may add more examples covering:
- memory and checkpoints
- multi-agent collaboration
- real-world tool integrations
- more advanced RAG setups
- better project structure and reusable utilities

For now, it's a practical scratchpad for learning.
