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

### 1. Basic Agent
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
Learn how to use Pydantic models with `output_schema` to ensure consistent, structured responses from your agents.

### 5. Sessions and State
Understand how to maintain state and memory across multiple interactions using sessions.

### 6. Persistent Storage
Learn techniques for storing agent data persistently across sessions and application restarts.

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
