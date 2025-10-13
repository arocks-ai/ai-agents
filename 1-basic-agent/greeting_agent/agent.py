from google.adk.agents import Agent
from google.adk.tools import google_search

def get_weather(city: str) -> dict:
    """"Retrive the current weather for a given city

    Returns:
        dictionary containing weather information
    """


    if city.lower() == 'new york':
        return {"status":"sucess", 
                "report": f"The weather in {city} is sunny with a high of 75°F."}

    else:
        return {"status":"error", 
                "error_message": f"The weather in {city} is not available."}


def get_current_time(city: str) -> dict:
    """Retrieve the current time for a given city

    Returns:
    dictionary containing current time information
    """
    
    import datetime
    from zoneinfo import ZoneInfo

    # get time zone info first
    if city.lower() == 'new york':
        tz_identifier = 'America/New_York'

    else:
        return {"status":"error", 
                "error_message": f"I don't have time zone information for {city} city."}
    
    tz = ZoneInfo(tz_identifier)
    current_time = datetime.datetime.now(tz)
    return {"status":"success",
            "report": f""" The current time in {city} is {current_time.strftime('%Y-%m-%d %H:%M:%S')}. """}


root_agent = Agent(
    name = "greeting_agent",
    model = "gemini-2.0-flash",
    description = "An agent that greets users and provides weather and time information.",
    instruction = "I can answer questions about the weather and current time in various cities.",
    # tools = [get_weather, get_current_time]
    tools = [get_weather, google_search, get_current_time]
    )