import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

llm_streaming = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    streaming=True
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a professional research report writer.
    Write a deeply detailed, comprehensive research report.
    Always follow this exact structure:

    # Research Report: [Topic]

    ## Executive Summary
    [3-4 sentences giving a complete overview]

    ## Background
    [Context and history of the topic, why it matters]

    ## Key Findings
    [At least 5 detailed findings with explanation for each]

    ## Recent Developments
    [At least 4 specific recent developments with details]

    ## Key Statistics & Numbers
    [Extract every specific number, percentage, or statistic mentioned.
    Format each one as: STAT: [number] | CONTEXT: [what it means]
    This section is critical - extract as many stats as possible]

    ## Expert Opinions & Quotes
    [Any expert views, quotes, or opinions from the sources.
    Format each as: QUOTE: [quote or paraphrased view] | SOURCE: [who said it]]

    ## Implications & Future Outlook
    [What this means for the future, predictions, impact]

    ## Conclusion
    [3-4 sentence wrap up]

    Write in depth. Do not be brief. Every section should be thorough."""),
    ("human", """Write a full research report on: {topic}

Using these insights:
{insights}""")
])


def run_report_agent(topic: str, insights: str) -> str:
    print("Writing final report...")
    chain = prompt | llm
    response = chain.invoke({
        "topic": topic,
        "insights": insights
    })
    print("Report done!")
    return response.content


def stream_report(topic: str, insights: str):
    chain = prompt | llm_streaming
    for chunk in chain.stream({
        "topic": topic,
        "insights": insights
    }):
        yield chunk.content