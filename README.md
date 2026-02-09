# ai-agents using google ADK





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
https://www.kaggle.com/code/ashokai2/day-5a-agent2agent-communication
