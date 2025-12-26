# 1. Create project and install dependencies
mkdir agentcore-tutorial && cd agentcore-tutorial
uv init --no-workspace && uv add bedrock-agentcore-starter-toolkit

# 2. Create a deployment folder and add the pyproject.toml file needed:
mkdir agent_deployment
uv init --bare ./agent_deployment && uv --directory ./agent_deployment add strands-agents bedrock-agentcore strands-agents-tools

# 3. Save the agent code above in to the agent_deployment folder as tutorial_agent.py

# 3. Configure and deploy
# Use all default answers for now:
uv run agentcore configure -e ./agent_deployment/tutorial_agent.py

uv run agentcore launch

# 4. Test your deployed agent
uv run agentcore invoke '{"prompt": "What is 25 * 4 + 10?"}'

uv run agentcore invoke '{"prompt": "Hello"}'