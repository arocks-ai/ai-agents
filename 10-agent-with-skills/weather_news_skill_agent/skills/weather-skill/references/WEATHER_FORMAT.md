# Extended Weather Formatting Guide

## For forecast requests (multi-day)
Present as a table:
| Day  | High | Low  | Condition     |
|------|------|------|---------------|
| Mon  | 28°C | 19°C | Partly cloudy |

## For severe weather
Always lead with a ⚠️ warning before the weather data and recommend
appropriate precautions (umbrella, avoiding travel, etc.).

## Units reference
- Default: Celsius (°C), wind in km/h, precipitation in mm
- If the user mentions "imperial", switch to: Fahrenheit (°F), mph, inches
- If the user is clearly from the US (mentions US cities), offer both units

```
This file is L3 - extended resources. Here's why it's in a separate file rather than in `SKILL.md` itself, and why that distinction matters enormously in production:
Every time the weather skill is triggered, the agent loads L2 (the `SKILL.md` body) into its context window. That happens on *every* weather query. But the extended formatting guide - multi-day forecast tables, severe weather protocols, unit conversion rules - is only relevant for a small fraction of queries. For a simple *"What's the weather in Paris?"* question, loading all of that detail is pure waste.
By putting it in `references/`, you're telling ADK: *"This information exists, but only load it if you actually need it."* The agent reads the reference filename and its header, decides whether the current task requires it, and loads the full content only then. This is what ADK's documentation calls *progressive disclosure* - specialist knowledge enters the context window just in time, not all at once.
At small scale this feels academic. At production scale - when your agent has dozens of skills, each with multiple reference files - it's the difference between an agent that fits comfortably in its context window and one that hits token limits on the third message.
The folder structure for your weather skill now looks like this:
```


```
skills/
└── weather_skill/
    ├── SKILL.md                        ✅ written
    └── references/
        └── WEATHER_FORMAT.md           ✅ written
```