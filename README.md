# Agent Development Kit (ADK) Samples

This repository contains examples for learning Google's Agent Development Kit (ADK), a powerful framework for building LLM-powered agents.

## Getting Started

### Setup Environment

Create a virtual environment at the root project level

```bash
# Create virtual environment in the root directory
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# deactivate  # when done with the work
```
Once set up, this single environment will work for all examples in the repository.

### Agent directory structure

pay attention to the directory structure

```bash
1-basic-agent/
└── greeting_agent	# see agent.py on agent naming	
    ├── agent.py	# agent name should match with directory name
    ├── __init__.py	# import the agent.py file (from . import agent)
    └── README.md
```
Once set up, this single environment will work for all examples in the repository.

### How to run

Navigate to the directory which contains the agent.py file

```bash
cd 1-basic-agent/
adk web                 # open browser windows for user input
adk run greeting_agent  # troubleshoot from the cmd line 

```





### Setting Up API Keys

1. Create an account in Google Cloud https://cloud.google.com/?hl=en
2. Create a new project
3. Go to https://aistudio.google.com/apikey
4. Create an API key
5. Assign key to the project
6. Connect to a billing account

Each example folder contains a `.env.example` file. For each project you want to run:

1. Navigate to the example folder
2. Rename `.env.example` to `.env` 
3. Open the `.env` file and replace the placeholder with your API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

You'll need to repeat this for each example project you want to run.

## Examples Overview

Here's what you can learn from each example folder:

### 1. Agent using tools
- Basic agent with 2 custom tools (for checking weather and time).  
- Simplfied to work for one city only (new york)

#### Example Query
```
What is the weather in new york
```
```
What is the time in new york
```

### 4. Structured Outputs
Using Pydantic models with `output_schema` to ensure consistent, structured responses from the agents.

LlMAgnet() will have the following data. EmailContent is a custom class with required fields of Pydantic models.
```
    output_schema=EmailContent,
    output_key="email",
```
#### Example Query
```
Draft email requesting manager for 5 day PTO. 
```
```
I am working on this project for 4 years on cirtial tasks.  Draft email asking manager requesting promption. 
```

### 5. Sessions and State
Understand how to maintain state and memory across multiple interactions using sessions.


#### Create Runner: provide agent, app_name and session_service object
```python
    APP_NAME = "agents"  # Application Name
    USER_ID = "default"  # User
    SESSION = "default"  # Session
    MODEL_NAME = "gemini-2.5-flash-lite"

    # Step 1: Create the LLM Agent
    root_agent = Agent(
        model=Gemini(model=MODEL_NAME),
        name="basic_session",
        description="A text chatbot",  # Description of the agent's purpose
    )

    # Step 2: Set up Session Management
    # InMemorySessionService stores conversations in RAM (temporary)
    session_service = InMemorySessionService()

    # Step 3: Create the Runner
    runner = Runner(
        agent=root_agent,       # Agent name
        app_name=APP_NAME,      # Application name to identify your app in the session service
        session_service=session_service # Session service object to manage conversation history and state 
    )
```

#### Create a new session or retrieve an existing one
```python
    # Attempt to create a new session or retrieve an existing one
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
    except:
        session = await session_service.get_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
```


#### Same session used across the calls
```python
    await run_session(
        runner,
        "Hi, I am rock ! What is the capital of United States?",
        "short-term-memory",        # Session name "short-term-memory"
    )

    await run_session(
        runner,
        "Hello! What is my name ?",
        "short-term-memory",        # Session name = Should match with preivous session to retrieve conversation history
    )
```

#### How to run
Run directly using python instead of "adk web" so that we can simulate same or different sessions

```bash
    cd 5-session-state/basic_session/
    python agent.py 
```

#### Testing - Both the queries are of same session
#### session name = "short-term-memory"
```bash

    ### Session: short-term-memory
    User > Hi, I am rock ! What is the capital of United States?
    gemini-2.5-flash-lite >  Hello Rock! The capital of the United States is Washington, D.C.

    ### Session: short-term-memory
    User > Hello! What is my name ?
    gemini-2.5-flash-lite >  You told me your name is Rock.
```

#### Testing -  Both the queries are of different sessions.
#### session name = "short-term-memory" (1st query)   session name = "short-term-memory" (2nd query)
```bash
    ### Session: short-term-memory
    User > Hi, I am rock ! What is the capital of United States?
    gemini-2.5-flash-lite >  Hello Rock! The capital of the United States is Washington, D.C.

    ### Session: short-term-memory-ANOTHER
    User > Hello! What is my name ?
    gemini-2.5-flash-lite >  I do not have access to your personal information, including your name. Therefore, I cannot tell you what your name is.
```


### 6. Persistent Storage
Learn techniques for storing agent data persistently across sessions and application restarts.

```bash

  # Modify the source code like below
  db_url = "sqlite+aiosqlite:///sessions.db"  
  session_service = DatabaseSessionService(db_url=db_url)

  # Install aiosqlite package
  pip install aiosqlite

```

#### How to run
Run directly using python instead of "adk web" so that we can simulate same or different sessions

```bash
    cd 5-session-state/basic_session/
    python agent.py 
```

#### Testing - First Session
#### Query 1, Query 2
```bash

    ### Session: short-term-memory
    User > Hi, I am rock ! What is the capital of United States?
    gemini-2.5-flash-lite >  Hello Rock! The capital of the United States is Washington, D.C.

    ### Session: short-term-memory
    User > Hello! What is my name ?
    gemini-2.5-flash-lite >  You told me your name is Rock.
```

#### Testing - Second Session (Application closed and ran again)
#### Query 2  Only (Name retrived from the Database)
```bash
    ### Session: short-term-memory
    User > Hello! What is my name ?
    gemini-2.5-flash-lite >  Your name is Rock.
```

### 7. Multi-Agent
See how to orchestrate multiple specialized agents working together to solve complex tasks.

### 8. Stateful Multi-Agent
Build agents that maintain and update state throughout complex multi-turn conversations.

### 9. Callbacks
Implement event callbacks to monitor and respond to agent behaviors in real-time.

### 10. Sequential Agent
Create pipeline workflows where agents operate in a defined sequence to process information.

### 11. Parallel Agent
Leverage concurrent operations with parallel agents for improved efficiency and performance.

### 12. Loop Agent
Build sophisticated agents that can iteratively refine their outputs through feedback loops.

## Official Documentation

For more detailed information, check out the official ADK documentation:
- https://google.github.io/adk-docs/get-started/quickstart



## Remote Agent2Agent Communication [Link](./15-day5-agent2agent/README.md)

This demo Demonstrates

- **Product Catalog Agent (exposed via A2A)** - External vendor service that provides product information
- **Customer Support Agent (consumer)** - Internal agent that helps customers by querying product data


![Agent 2 Agent workflow](./15-day5-agent2agent/images/remote-flow.png)

How it works:
1. Customer asks a product question to your Customer Support Agent
2. Support Agent realizes it needs product information
3. Support Agent calls the Product Catalog Agent via A2A protocol
4. Product Catalog Agent (external vendor) returns product data
5. Support Agent formulates an answer and responds to the customer

Why this justifies A2A:
- Product Catalog is maintained by an external vendor (you can't modify their code)
- Different organizations with separate systems
- Formal contract needed between services
- Product Catalog could be in a different language/framework

---

#### Application build steps

- Create the Product Catalog Agent - Build the vendor's agent with product lookup (This is remote Agent)
- Expose via A2A - Make it accessible using to_a2a() (expose on port 8001)
- Start the Server - Run the agent as a background service (use uvicorn to spin off the webserver at port 8001)
- Create the Customer Support Agent - Build the consumer agent (This will be local to us)
- Test Communication - See A2A in action with real queries (Check for response, call >> Local Agent >> Remote agent)


---

Setup the remote environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```
---


#### Start the Product Catalog Agent Server

```bash
cd 15-day5-agent2agent
uvicorn remote_a2a.product_catalog.agent-expose:a2a_app --host localhost --port 8001    # show warnings also
python -W ignore::UserWarning -m uvicorn remote_a2a.product_catalog.agent-expose:a2a_app --host localhost --port 8001   # Ignore warnings

```
---


#### Start the Customer Agent

```bash
# Star the customer Agent and provide user query
python agent
python -W ignore::UserWarning -m agent   # Ignore warnings

```
---


#### References
- [ADK Structured Data Documentation](https://google.github.io/adk-docs/agents/llm-agents/#structuring-data-input_schema-output_schema-output_key)
- [Pydantic Documentation](https://docs.pydantic.dev/latest/) 
- [Kaggle 5 day AI Agent course with ADK](https://www.kaggle.com/code/ashokai2/day-5a-agent2agent-communication)
- [ADK Master Class YT - Beginner to Pro](https://www.youtube.com/watch?v=P4VFL9nIaIA&list=WL&index=16)
