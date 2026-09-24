# AgenticAI Experiments

This repository is a collection of small Python experiments for learning LangGraph and common agentic workflow patterns.

It is not a single application or production project. Instead, it contains multiple independent examples that explore different ways to structure LLM workflows in Python using LangGraph.

## What is in this repo?

Each file or folder is a focused example for a specific concept:

- Sequential workflow: a linear multi-step pipeline where the output of one node is passed to the next
- Parallel workflow: multiple branches running at the same time and then merged into one state
- Conditional workflow + RAG: routing based on the user query and using retrieval from PDF documents
- Human-in-the-loop workflow: pausing for approval or revision before continuing
- Iterative tool workflow: generating a draft, using tools, then reviewing and retrying
- State patterns: examples showing different ways to manage state in LangGraph

These scripts are intentionally simple and beginner-friendly. The goal is to understand how agentic systems are built, not to create a polished end-user product.

## Repository contents

### 1. Sequential workflow
File: `sequential_workflow.py`

A simple 3-step workflow:
- edit text
- convert it into a script
- translate it into Hinglish

This demonstrates how state moves through a linear graph.

### 2. Parallel workflow
File: `parallel_workflow.py`

This example runs multiple independent analysis branches in parallel:
- toxicity
- copyright risk
- cultural sensitivity

The results are merged into a single shared state.

### 3. Conditional workflow + retrieval
Folder: `Conditional workflow/`

This folder includes a small college assistant example using:
- query routing
- academic vs. fee-related classification
- FAISS-based retrieval from local PDF documents
- final answer generation using retrieved context

This is a practical example of conditional logic and RAG.

### 4. Human-in-the-loop workflow
File: `human_in_the_loop.py`

A LinkedIn post generator that pauses for manual review.

It:
- writes a draft
- asks for approval or feedback
- rewrites the post if needed
- stops after a fixed number of attempts

This demonstrates how user input can be included in an agent workflow.

### 5. Iterative tool workflow
File: `iterative_tools.py`

A writing workflow where the model can use tools, draft content, review the output, and iterate if needed.

It shows:
- tool calling
- draft extraction
- review and approval logic
- retry loops

### 6. State experiments
File: `state.py`

A small reference file covering common state representations in Python and LangGraph:
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
├── README.md
└── .gitignore
```

## Setup

1. Create a virtual environment
2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Add any required API keys in a `.env` file if the script uses an LLM provider such as Groq, Gemini, or OpenAI.

Example:

```bash
GROQ_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

## Notes

This repo is meant as a learning sandbox. Most files are intentionally minimal and meant to demonstrate a specific LangGraph concept rather than serve as production-ready applications.

A few examples may require API keys and internet access depending on the model or tool being used.

## Learning goal

The main purpose of this repository is to explore:

- state-based workflows
- graph routing and branching
- tool use in agent systems
- retrieval-augmented generation
- human review loops
- how multi-step LLM logic is structured in practice

This is a personal collection of LangGraph experiments and learning exercises.
