import asyncio
import json
from agents import Agent, Runner, OpenAIChatCompletionsModel
from tools import calculate
from openai import AsyncOpenAI
import os

def get_agent(model_name: str, api_key: str, base_url: str):
    """
    Creates an Agent instance with a custom model and provider.
    """
    # Configure the client for the specific provider (OpenAI, Groq, etc.)
    custom_client = AsyncOpenAI(
        base_url=base_url,
        api_key=api_key
    )

    custom_model = OpenAIChatCompletionsModel(
        model=model_name,
        openai_client=custom_client
    )

    return Agent(
        name="Math & Logic Assistant",
        model=custom_model,
        instructions="""
        You are a helpful AI assistant. 
        1. If the user input involves a math calculation, you MUST use the 'calculate' tool.
        2. For all other queries, respond normally.
        3. You MUST ALWAYS return your final response as a valid JSON object.
        
        The JSON structure MUST be:
        {
          "input": "the user's original message",
          "tool_used": "name of the tool used (e.g., 'calculate') or 'none'",
          "result": "your final answer or the tool's result",
          "status": "success" or "error"
        }
        
        Do not include any text outside of the JSON object.
        """,
        tools=[calculate]
    )

async def process_query(user_input: str, model_name: str, api_key: str, base_url: str):
    """
    Runs the agent and returns the structured JSON output.
    """
    try:
        agent = get_agent(model_name, api_key, base_url)
        
        # Runner.run is async and handles the tool-calling loop automatically.
        result = await Runner.run(agent, user_input)
        
        # The agent is instructed to return JSON in final_output
        output_text = result.final_output
        
        # Clean up output in case the model added markdown backticks
        if "```json" in output_text:
            output_text = output_text.split("```json")[1].split("```")[0].strip()
        elif "```" in output_text:
            output_text = output_text.split("```")[1].split("```")[0].strip()
            
        try:
            return json.loads(output_text)
        except json.JSONDecodeError:
            return {
                "input": user_input,
                "tool_used": "none",
                "result": output_text,
                "status": "success" # Treat as success if it's just raw text
            }
            
    except Exception as e:
        return {
            "input": user_input,
            "tool_used": "error",
            "result": f"An error occurred: {str(e)}",
            "status": "error"
        }
