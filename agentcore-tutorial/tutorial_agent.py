"""
Production-Ready AI Agent for Amazon Bedrock AgentCore
"""
from strands import Agent
from strands_tools import calculator
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

@app.entrypoint
def invoke(payload, context):
    """AgentCore Runtime entry point"""
    agent = Agent(
        model=MODEL_ID,
        system_prompt="You are a helpful assistant that can perform calculations. Use the calculate tool for any math problems.",
        tools=[calculator]
    )
    
    prompt = payload.get("prompt", "Hello!")
    result = agent(prompt)
    
    return {
        "response": result.message.get('content', [{}])[0].get('text', str(result))
    }

if __name__ == "__main__":
    app.run()