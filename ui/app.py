import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import streamlit as st
from agents.search_agent import run_search_agent
from agents.research_agent import run_research_agent
from agents.chart_agent import run_chart_agent
from agents.report_agent import stream_report
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Research Agent",
    page_icon="",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #1a1a1a; }
    .block-container { max-width: 750px; padding: 0 1rem; margin: 0 auto; }
    .top-bar { text-align: center; padding: 3rem 0 1rem 0; }
    .top-bar h1 { font-size: 1.8rem; font-weight: 600; color: #ececec; margin: 0; }
    .top-bar p { color: #6b6b6b; font-size: 0.9rem; margin-top: 0.4rem; }
    .stTextInput input {
        background-color: #2f2f2f !important;
        border: 1px solid #3f3f3f !important;
        border-radius: 12px !important;
        color: #ececec !important;
        font-size: 1rem !important;
        padding: 1rem 1.2rem !important;
    }
    .stTextInput input:focus { border-color: #6b6b6b !important; box-shadow: none !important; }
    .stTextInput input::placeholder { color: #6b6b6b !important; }
    div.stButton > button {
        background-color: #2f2f2f;
        color: #ececec;
        border: 1px solid #3f3f3f;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-size: 0.9rem;
        font-weight: 500;
        width: 100%;
        transition: all 0.2s;
    }
    div.stButton > button:hover { background-color: #3f3f3f; border-color: #6b6b6b; }
    .step-indicator { display: flex; align-items: center; gap: 0.6rem; padding: 0.6rem 0; color: #6b6b6b; font-size: 0.85rem; }
    .step-indicator.done { color: #ececec; }
    .step-dot { width: 6px; height: 6px; border-radius: 50%; background-color: #3f3f3f; flex-shrink: 0; }
    .step-dot.done { background-color: #10a37f; }
    .query-pill {
        display: inline-block; background: #2f2f2f; border: 1px solid #3f3f3f;
        color: #ababab; padding: 0.25rem 0.75rem; border-radius: 20px;
        font-size: 0.78rem; margin: 0.2rem 0.2rem 0 0;
    }
    .divider { border: none; border-top: 1px solid #2f2f2f; margin: 1.5rem 0; }
    .report-body { color: #ececec; font-size: 0.95rem; line-height: 1.8; }
    .report-body h1 { font-size: 1.4rem; font-weight: 600; color: #ececec; margin-top: 0; margin-bottom: 1rem; }
    .report-body h2 { font-size: 1rem; font-weight: 600; color: #ababab; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 1.8rem; margin-bottom: 0.6rem; }
    .report-body p { color: #d0d0d0; margin-bottom: 0.8rem; }
    .report-body li { color: #d0d0d0; margin-bottom: 0.4rem; }
    .stats-row { display: flex; gap: 1rem; margin: 1rem 0; }
    .stat-item { flex: 1; background: #2f2f2f; border-radius: 10px; padding: 0.8rem 1rem; text-align: center; }
    .stat-num { font-size: 1.4rem; font-weight: 600; color: #ececec; }
    .stat-lbl { font-size: 0.75rem; color: #6b6b6b; margin-top: 0.2rem; }
    .quote-block { border-left: 3px solid #10a37f; padding: 0.8rem 1.2rem; margin-bottom: 0.8rem; background: #2f2f2f; border-radius: 0 8px 8px 0; }
    .quote-text { color: #ececec; font-size: 0.9rem; font-style: italic; }
    .quote-source { color: #6b6b6b; font-size: 0.78rem; margin-top: 0.4rem; }
    .related-topic {
        display: inline-block; background: #2f2f2f; border: 1px solid #3f3f3f;
        color: #ababab; padding: 0.4rem 0.9rem; border-radius: 20px;
        font-size: 0.82rem; margin: 0.3rem 0.3rem 0 0; cursor: pointer;
    }
    .related-topic:hover { background: #3f3f3f; color: #ececec; }
    .history-item { padding: 0.5rem 0.8rem; border-radius: 8px; color: #ababab; font-size: 0.85rem; }
    .history-item:hover { background: #2f2f2f; color: #ececec; }
    .source-item { padding: 0.6rem 0; border-bottom: 1px solid #2f2f2f; }
    .source-item a { color: #ababab; text-decoration: none; font-size: 0.85rem; }
    .source-item a:hover { color: #ececec; }
    .source-url { color: #4b4b4b; font-size: 0.75rem; margin-top: 0.1rem; }
    .chat-message-user {
        background: #2f2f2f; border-radius: 12px 12px 2px 12px;
        padding: 0.8rem 1rem; margin-bottom: 0.8rem;
        color: #ececec; font-size: 0.9rem; text-align: right;
    }
    .chat-message-ai {
        background: #1e2a1e; border: 1px solid #2d4a2d;
        border-radius: 12px 12px 12px 2px; padding: 0.8rem 1rem;
        margin-bottom: 0.8rem; color: #d0d0d0; font-size: 0.9rem;
    }
    div.stDownloadButton > button {
        background-color: #2f2f2f; color: #ababab;
        border: 1px solid #3f3f3f; border-radius: 10px; font-size: 0.85rem; width: 100%;
    }
    .stSpinner > div { border-top-color: #10a37f !important; }
</style>
""", unsafe_allow_html=True)

# Session state
if "history" not in st.session_state:
    st.session_state.history = []
if "report" not in st.session_state:
    st.session_state.report = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "report_data" not in st.session_state:
    st.session_state.report_data = None

# Sidebar
with st.sidebar:
    st.markdown('<div style="color:#6b6b6b;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:1rem;">Recent Reports</div>', unsafe_allow_html=True)
    if not st.session_state.history:
        st.markdown('<div style="color:#4b4b4b;font-size:0.82rem;">No reports yet</div>', unsafe_allow_html=True)
    else:
        for item in reversed(st.session_state.history[-5:]):
            st.markdown(f'<div class="history-item">{item}</div>', unsafe_allow_html=True)

# Top bar
st.markdown("""
<div class="top-bar">
    <h1>Research Agent</h1>
    <p>Enter a topic. Get a fully sourced research report.</p>
</div>
""", unsafe_allow_html=True)

# Input
topic = st.text_input("", placeholder="What do you want to research?", label_visibility="collapsed")
generate = st.button("Generate Report")

if generate and topic:
    if topic not in st.session_state.history:
        st.session_state.history.append(topic)
    st.session_state.chat_history = []
    st.session_state.report = None
    st.session_state.report_data = None

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    step1 = st.empty()
    step2 = st.empty()
    step3 = st.empty()

    step1.markdown('<div class="step-indicator"><div class="step-dot"></div>Searching the web...</div>', unsafe_allow_html=True)
    with st.spinner(""):
        all_results, queries = run_search_agent(topic)
    step1.markdown('<div class="step-indicator done"><div class="step-dot done"></div>Web search complete</div>', unsafe_allow_html=True)

    queries_html = "".join([f'<span class="query-pill">{q}</span>' for q in queries])
    st.markdown(f'<div style="padding-left:1.2rem;margin-bottom:0.5rem;">{queries_html}</div>', unsafe_allow_html=True)

    step2.markdown('<div class="step-indicator"><div class="step-dot"></div>Analyzing sources...</div>', unsafe_allow_html=True)
    with st.spinner(""):
        insights, sources = run_research_agent(topic)
    step2.markdown('<div class="step-indicator done"><div class="step-dot done"></div>Analysis complete</div>', unsafe_allow_html=True)

    step3.markdown('<div class="step-indicator"><div class="step-dot"></div>Writing report...</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div style="color:#6b6b6b;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.8rem;">Full Report</div>', unsafe_allow_html=True)

    report_placeholder = st.empty()
    report = ""
    for chunk in stream_report(topic, insights):
        report += chunk
        report_placeholder.markdown(
            f'<div class="report-body">{report}</div>',
            unsafe_allow_html=True
        )

    step3.markdown('<div class="step-indicator done"><div class="step-dot done"></div>Report ready</div>', unsafe_allow_html=True)

    st.session_state.report = report
    st.session_state.report_data = {
        "topic": topic,
        "queries": queries,
        "all_results": all_results,
        "sources": sources,
        "insights": insights
    }

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown(f"""
<div class="stats-row">
    <div class="stat-item"><div class="stat-num">{len(queries)}</div><div class="stat-lbl">Queries</div></div>
    <div class="stat-item"><div class="stat-num">{len(all_results)}</div><div class="stat-lbl">Sources</div></div>
    <div class="stat-item"><div class="stat-num">{len(report.split())}</div><div class="stat-lbl">Words</div></div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    fig = run_chart_agent(report)
    if fig:
        st.markdown('<div style="color:#6b6b6b;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;">Key Statistics</div>', unsafe_allow_html=True)
        st.pyplot(fig)
        st.markdown('<hr class="divider">', unsafe_allow_html=True)

    quotes = re.findall(r'QUOTE:\s*(.*?)\s*\|\s*SOURCE:\s*(.*?)(?:\n|$)', report)
    if quotes:
        st.markdown('<div style="color:#6b6b6b;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.8rem;">Key Quotes</div>', unsafe_allow_html=True)
        for quote, source in quotes:
            st.markdown(f"""
<div class="quote-block">
    <div class="quote-text">"{quote.strip()}"</div>
    <div class="quote-source">— {source.strip()}</div>
</div>
""", unsafe_allow_html=True)
        st.markdown('<hr class="divider">', unsafe_allow_html=True)

    related_llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
    related_prompt = ChatPromptTemplate.from_messages([
        ("system", "Generate exactly 5 related research topics for the given topic. Return only the topics, one per line, nothing else."),
        ("human", "Related topics for: {topic}")
    ])
    related_chain = related_prompt | related_llm
    related_response = related_chain.invoke({"topic": topic})
    related_topics = [t.strip() for t in related_response.content.strip().split("\n") if t.strip()][:5]
    related_html = "".join([f'<span class="related-topic">{t}</span>' for t in related_topics])
    st.markdown('<div style="color:#6b6b6b;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.8rem;">Explore Related Topics</div>', unsafe_allow_html=True)
    st.markdown(f'<div>{related_html}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div style="color:#6b6b6b;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;">Sources</div>', unsafe_allow_html=True)
    for source in sources:
        st.markdown(f"""
<div class="source-item">
    <a href="{source['url']}" target="_blank">{source['title']}</a>
    <div class="source-url">{source['url']}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.download_button(
        label="Download Report",
        data=report,
        file_name=f"{topic}_report.txt",
        mime="text/plain"
    )

elif st.session_state.report:
    data = st.session_state.report_data
    report = st.session_state.report

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div style="color:#6b6b6b;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.8rem;">Full Report</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="report-body">{report}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown(f"""
<div class="stats-row">
    <div class="stat-item"><div class="stat-num">{len(data["queries"])}</div><div class="stat-lbl">Queries</div></div>
    <div class="stat-item"><div class="stat-num">{len(data["all_results"])}</div><div class="stat-lbl">Sources</div></div>
    <div class="stat-item"><div class="stat-num">{len(report.split())}</div><div class="stat-lbl">Words</div></div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    quotes = re.findall(r'QUOTE:\s*(.*?)\s*\|\s*SOURCE:\s*(.*?)(?:\n|$)', report)
    if quotes:
        st.markdown('<div style="color:#6b6b6b;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.8rem;">Key Quotes</div>', unsafe_allow_html=True)
        for quote, source in quotes:
            st.markdown(f"""
<div class="quote-block">
    <div class="quote-text">"{quote.strip()}"</div>
    <div class="quote-source">— {source.strip()}</div>
</div>
""", unsafe_allow_html=True)
        st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div style="color:#6b6b6b;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;">Sources</div>', unsafe_allow_html=True)
    for source in data["sources"]:
        st.markdown(f"""
<div class="source-item">
    <a href="{source['url']}" target="_blank">{source['title']}</a>
    <div class="source-url">{source['url']}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.download_button(
        label="Download Report",
        data=report,
        file_name=f"{data['topic']}_report.txt",
        mime="text/plain"
    )

# Follow up chat - always visible after report is generated
if st.session_state.report:
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div style="color:#6b6b6b;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.8rem;">Ask a Follow-up Question</div>', unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message-ai">{msg["content"]}</div>', unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):
        question = st.text_input("", placeholder="Ask anything about this report...", label_visibility="collapsed")
        ask = st.form_submit_button("Ask")

    if ask and question:
        st.session_state.chat_history.append({"role": "user", "content": question})

        chat_llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a research assistant. Answer questions based on the research report provided.
            Be concise, accurate, and helpful. Only use information from the report."""),
            ("human", """Report:
{report}

Question: {question}""")
        ])
        chat_chain = chat_prompt | chat_llm
        chat_response = chat_chain.invoke({
            "report": st.session_state.report,
            "question": question
        })

        st.session_state.chat_history.append({"role": "ai", "content": chat_response.content})
        st.rerun()