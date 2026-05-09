import os
import pathlib

import httpx
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.skills import load_skill_from_dir, models
from google.adk.tools import skill_toolset

load_dotenv()

def get_weather(city: str) -> dict:
    """
    Fetches current weather for a given city using the wttr.in API.
    Args:
        city: The name of the city to fetch weather for.
    Returns:
        A dictionary containing weather data or an error message.
    """
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data["current_condition"][0]
        area = data["nearest_area"][0]
        return {
            "city": area["areaName"][0]["value"],
            "country": area["country"][0]["value"],
            "temp_c": current["temp_C"],
            "feels_like_c": current["FeelsLikeC"],
            "condition": current["weatherDesc"][0]["value"],
            "wind_kmph": current["windspeedKmph"],
            "humidity": current["humidity"],
        }
    except httpx.HTTPError as e:
        return {"error": f"Could not fetch weather: {str(e)}"}
    except KeyError:
        return {"error": f"Location '{city}' not found. Please check the city name."}
    



# Inline skills
def create_news_skill(api_key: str) -> models.Skill:
    """Creates the news summarizer skill with runtime API configuration."""

    return models.Skill(
        frontmatter=models.Frontmatter(
            name="news-summarizer",
            description=(
                "Fetches and summarizes the latest news headlines. "
                "Use this skill when the user asks about news, current events, "
                "headlines, what's happening, trending topics or sports results. "
                "Can filter by category: technology, business, sports, health, science."
            ),
        ),
        instructions=(
            "You are a news briefing specialist. Your job is to fetch and present "
            "the latest news in a clear, concise format.\n\n"
            "## Steps\n"
            "Step 1: Use the `get_news` function tool to fetch headlines.\n"
            "Step 2: Group headlines by topic if multiple categories were requested.\n"
            "Step 3: For each headline, provide:\n"
            "  - 📰 Headline title\n"
            "  - One sentence summary of what happened\n"
            "  - Source name\n\n"
            "## Rules\n"
            "- Present a maximum of 5 headlines unless the user asks for more.\n"
            "- Always mention when the news was published (e.g., '2 hours ago').\n"
            "- If no news is found for a category, say so clearly.\n"
            "- Never editorialize or add personal opinions to the news."
        ),
        resources=models.Resources(
            references={
                "CATEGORIES.md": (
                    "# Available News Categories\n"
                    "- technology: Tech, AI, software, hardware news\n"
                    "- business: Finance, markets, economy\n"
                    "- sports: All sports news including cricket, NFL, basketball, football, tennis\n"  # ← updated
                    "- health: Medical, wellness, public health\n"
                    "- science: Research, space, discoveries\n"
                    "- general: Top stories across all topics (default)\n"
                ),
            }
        ),
    )



def get_news(category: str = "general", page_size: int = 5) -> dict:
    """
    Fetches the latest news headlines from NewsAPI.
    Args:
        category: News category (technology, business, sports, health,
                  science, general). Defaults to 'general'.
        page_size: Number of headlines to return (1-20). Defaults to 5.
    Returns:
        A dictionary with a list of articles or an error message.
    """
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return {"error": "NEWS_API_KEY not configured"}
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": api_key,
            "category": category,
            "language": "en",
            "pageSize": page_size,
        }
        response = httpx.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = []
        for article in data.get("articles", []):
            published = article.get("publishedAt", "")
            articles.append({
                "title": article.get("title", "No title"),
                "description": article.get("description", "No description"),
                "source": article.get("source", {}).get("name", "Unknown"),
                "published_at": published,
                "url": article.get("url", ""),
            })
        return {
            "category": category,
            "total_results": data.get("totalResults", 0),
            "articles": articles,
        }
    except httpx.HTTPError as e:
        return {"error": f"News API request failed: {str(e)}"}
    

# ─────────────────────────────────────────────────────────────────────────────
# SKILL 1: Weather — File-Based
# load_skill_from_dir() reads the SKILL.md and references/ folder and builds
# a Skill object from them. Same result as models.Skill(...), different source.
# ─────────────────────────────────────────────────────────────────────────────
weather_skill = load_skill_from_dir(
    pathlib.Path(__file__).parent / "skills" / "weather-skill"   
)

# ─────────────────────────────────────────────────────────────────────────────
# SKILL 2: News — Inline
# Constructed at runtime by the factory function you wrote in Section 4.
# ─────────────────────────────────────────────────────────────────────────────
news_skill = create_news_skill(api_key=os.getenv("NEWS_API_KEY", ""))

# ─────────────────────────────────────────────────────────────────────────────
# SKILL TOOLSET
# SkillToolset bundles both skills into a single object the Agent can hold.
# Think of it as the agent's "skills menu" — the complete list of specialist
# knowledge modules available to it.
# ─────────────────────────────────────────────────────────────────────────────
my_toolset = skill_toolset.SkillToolset(
    skills=[weather_skill, news_skill]
)

# ─────────────────────────────────────────────────────────────────────────────
# THE AGENT
# This is the variable ADK looks for when you run `adk web` or `adk run`.
# It must be named `root_agent` at module level for the CLI to find it.
# ─────────────────────────────────────────────────────────────────────────────
root_agent = Agent(
    model="gemini-2.5-flash",
    name="weather_news_skill_agent",
    description=(
        "A helpful daily briefing assistant that provides weather updates "
        "and news summaries for any location and topic."
    ),
    instruction=(
        "You are a friendly daily briefing assistant. "
        "You help users stay informed by providing accurate weather information "
        "and the latest news headlines. "
        "When answering, always be concise and well-organized. "
        "Use your weather skill for weather queries and your news skill for news queries. "
        "If the user asks for both in a single question, answer both."
    ),
    tools=[
        my_toolset,    # the skills menu — tells the agent WHEN to use each skill
        get_weather,   # the actual executor — called by the weather skill
        get_news,      # the actual executor — called by the news skill
    ],
)    