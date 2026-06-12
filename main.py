from dotenv import load_dotenv
from agents.search_agent import run_search_agent
from agents.research_agent import run_research_agent
from agents.report_agent import run_report_agent

load_dotenv()

topic = "quantum computing breakthroughs 2025"

# Step 1 - Search
run_search_agent(topic)

# Step 2 - Extract insights
insights = run_research_agent(topic)

# Step 3 - Write report
report = run_report_agent(topic, insights)

print(report)