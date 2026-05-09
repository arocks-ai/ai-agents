"""Programmatic entry point for the Daily Briefing Agent.

This script demonstrates how to execute the agent using the Google ADK Runner 
API rather than the `adk web` or `adk run` CLI tools.

1. InMemorySessionService: Manages conversation history in volatile memory (RAM).
2. runner.run_async(): An asynchronous generator yielding tool calls and results.
3. event.content.parts[0].text: Extracted response text from the final response event.
"""


import asyncio
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# Import the agent you built
from agent import root_agent
async def ask_agent(query: str) -> str:
   
    # 1. InMemorySessionService stores conversation history in RAM.
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="daily_briefing",
        session_service=session_service,
    )
    # Create a session for this user
    session = await session_service.create_session(
        app_name="daily_briefing",
        user_id="user_1",
    )
        
    # Create content from user query
    content = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )
    

    # 2.Stream events from the agent until the final response arrives
    async for event in runner.run_async(
        user_id="user_1",
        session_id=session.id,
        new_message=content,
    ):
        if event.is_final_response():
            # 3. Extract text from final response
            return event.content.parts[0].text
    return "No response received."

if __name__ == "__main__":
    result = asyncio.run(ask_agent("Weather in Tokyo and tech news?"))
    print(result)