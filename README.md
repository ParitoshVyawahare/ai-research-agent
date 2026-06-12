# AI Research Agent

An autonomous, multi-agent research assistant that takes any topic, searches the live web, extracts the most relevant insights, and generates a structured, fully sourced research report — in seconds.

Built with a multi-agent pipeline, retrieval-augmented generation (RAG), live web search, and a streaming chat interface.

**Live demo:** https://ai-research-agent-lgpvcdycriqswyebxiw9yx.streamlit.app

---

## Demo

<img width="1460" height="873" alt="image" src="https://github.com/user-attachments/assets/09aea782-2cc3-4c78-aea5-00a4c8bafc1f" />


---

## What it does

Give it a topic like *"quantum computing breakthroughs 2025"* and the system will:

1. Generate several intelligent search queries from a single topic
2. Search the live web across all of those queries
3. Store the results in a vector database for semantic retrieval
4. Extract the most important insights from everything it found
5. Write a structured, professional research report
6. Surface key statistics as a chart, pull out notable quotes, and suggest related topics
7. Let you ask follow-up questions about the report in a chat interface

All of it streams to the screen in real time, the way a modern AI assistant responds.

---

## How it works

The project is built as a pipeline of focused agents, where each agent does one job and passes its output to the next. This separation of concerns keeps the system easy to debug, extend, and reason about.

```text
User topic
    │
    ▼
search_agent      generates smart queries, searches the web, stores results
    │
    ▼
research_agent    retrieves the most relevant content, extracts key insights
    │
    ▼
report_agent      writes a structured, streaming research report
    │
    ▼
chart_agent       extracts statistics and renders a chart
    │
    ▼
Streamlit UI      report + chart + quotes + related topics + follow-up chat
```

---

## Features

- **Multi-agent pipeline** — four cooperating agents, each with a single responsibility
- **Intelligent query generation** — the agent decides how to search, rather than searching the raw topic once
- **Retrieval-Augmented Generation (RAG)** — results are embedded and retrieved by semantic meaning, not keyword matching
- **Streaming output** — the report types out token by token in real time
- **Automatic charts** — statistics are extracted from the report and plotted
- **Key quotes** — notable expert opinions are pulled out and highlighted
- **Related topics** — the agent suggests further avenues to explore
- **Follow-up chat** — ask questions about the generated report and get grounded answers
- **Report history** — recent reports are kept in the sidebar
- **Downloadable reports** — export any report as a text file

---

## Tech Stack

| Layer | Technology |
|---------|---------|
| Language | Python |
| LLM Inference | Groq (Llama 3.3 70B) |
| Web Search | Tavily API |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Orchestration | LangChain |
| Charts | Matplotlib |
| Interface & Deployment | Streamlit / Streamlit Community Cloud |


