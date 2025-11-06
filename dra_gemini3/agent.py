from google.adk.agents import Agent
from .ado_tools import (
    ado_query_work_items,
    ado_get_pipeline_status,
    ado_get_test_results,
    # Import all other tool functions
)

import warnings
warnings.filterwarnings("ignore", message=".*EXPERIMENTAL.*", category=UserWarning)
#warnings.filterwarnings("ignore")

# # 1. Define the Agent's Goal and Instructions
# DEPLOYMENT_READINESS_INSTRUCTION = """
#     You are the **Release Readiness Auditor Agent** for Project Phoenix.
#     Your goal is to provide a clear, evidence-based Go/No-Go recommendation for the deployment.
#     **You MUST use the provided tools (ADOConnectorTool) to fetch all required data.**
#     **NEVER HALLUCINATE data or claims.** Every claim MUST be supported by a work item ID, pipeline ID, or URL returned by the tools.

#     **Decision Criteria:**
#     1.  **NO-GO** if any Critical/High Security Vulnerabilities are present.
#     2.  **NO-GO** if any P1/Critical Bugs flagged as 'release-blocker' are 'Active'.
#     3.  **NO-GO** if the latest CI/CD pipeline run failed on a critical stage (e.g., Integration Tests).
#     4.  **GO** only if all critical checks pass and the CAB signoff is approved.

#     **Output Format:** Your final response MUST be structured clearly in Markdown with the following sections:

#     ## 📢 Release Readiness Report: Project Phoenix
#     ---
#     **Readiness Score:** [Score 0-100, calculated based on the blocker severity]
#     **Decision:** [GO / NO-GO]
#     **Summary:** [Short paragraph justifying the decision, citing data from all tools used.]
#     ---
#     ### 🛑 Top Blockers and Evidence
#     * [Blocker Title] - **Evidence:** [ID/URL] - **Reason:** [Why it blocks release]
#     * ... (List up to 5 blockers)
#     ---
#     ### 🛠️ Recommended Actions
#     * [Action: Assign owner to fix Bug 101]
#     * [Action: Rerun CI-main pipeline]
#     * ... (Suggest concrete, actionable steps based on findings)
#     """

# 1. Define the Agent's Goal and Instructions
DEPLOYMENT_READINESS_INSTRUCTION = (
    "You are a sophisticated Deployment Readiness AI Agent. "
    "Your goal is to synthesize data from simulated Azure DevOps tools (work items, "
    "pipelines, security scans, etc.) to produce a clear 'Go/No-GO' decision for deployment. "
    "Use the provided tools to gather all required information. "
    "Based on the data, you must output a short readiness score (0-100), "
    "a Go/No-GO Decision, a readiness summary, the top 5 blockers with evidence links (IDs/URLs), "
    "recommended actions (e.g., 'create bug', 'assign owner', 'rerun pipeline'), "
    "and a suggested rollback plan if needed. "
    "Prioritize Critical/High vulnerabilities, blocked work items, and failed pipeline runs."
)

# 2. Instantiate the Agent
root_agent = Agent(
    name="Deployment_Readiness_Agent",
    model="gemini-2.5-flash",
    instruction=DEPLOYMENT_READINESS_INSTRUCTION,
    description="An agent that automates deployment readiness checks using ADO data.",
    tools=[
        ado_query_work_items,
        ado_get_pipeline_status,
        ado_get_test_results,
    ]
)

# 3. Define the main function to run the agent (for adk run)
async def main():
    # Example of a user query
    query = "Evaluate the deployment readiness for the 'Product-Search' project to Production environment. Check for any blocking P0 bugs, Critical/High vulnerabilities, and ensure the last build was successful."
    
    print(f"User Query: {query}\n")

    # Stream the agent's response
    async for event in root_agent.async_stream_query(query=query):
        if event.message:
            print(f"Agent Response: {event.message.text}")
        elif event.tool_call:
            print(f"Tool Call: {event.tool_call.function.name}({event.tool_call.function.arguments})")
        elif event.tool_result:
            # You might want to suppress printing large tool results for clarity
            print(f"Tool Result: Success (Data synthesized for model reasoning)")
        
    print("\n--- Agent Run Complete ---")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())