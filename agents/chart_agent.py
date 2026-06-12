import os
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import json

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a data extraction assistant.
    Your job is to extract statistics and numbers from research reports.
    Return ONLY a valid JSON array, nothing else, no explanation, no markdown.
    Format:
    [
        {{"label": "short label", "value": 123, "unit": "% or x or years etc"}},
        {{"label": "short label", "value": 456, "unit": "unit"}}
    ]
    Extract maximum 6 stats. Only include stats with clear numeric values.
    If no stats found return an empty array: []"""),
    ("human", "Extract statistics from this report:\n{report}")
])


def run_chart_agent(report: str):
    print("Chart agent extracting stats...")

    chain = prompt | llm
    response = chain.invoke({"report": report})

    try:
        raw = response.content.strip()
        raw = re.sub(r'^```json|^```|```$', '', raw, flags=re.MULTILINE).strip()
        stats = json.loads(raw)

        if not stats or len(stats) == 0:
            print("No stats found")
            return None

        labels = [s["label"] for s in stats]
        values = [float(s["value"]) for s in stats]
        units = [s.get("unit", "") for s in stats]

        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#2f2f2f')

        bars = ax.barh(labels, values, color='#10a37f', height=0.5)

        for bar, value, unit in zip(bars, values, units):
            ax.text(
                bar.get_width() + max(values) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{value} {unit}",
                va='center',
                color='#ececec',
                fontsize=9
            )

        ax.set_xlabel("Value", color='#6b6b6b', fontsize=9)
        ax.tick_params(colors='#ababab', labelsize=9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#3f3f3f')
        ax.spines['left'].set_color('#3f3f3f')
        ax.xaxis.label.set_color('#6b6b6b')

        plt.tight_layout()
        return fig

    except Exception as e:
        print(f"Chart agent error: {e}")
        return None