# models/agent_creator.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI



from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

from tools.weather_tool import get_weather_data
from models.disease_predictor import analyze_plant_image
# Note: Yield prediction tool is omitted for simplicity but can be added similarly.

def create_agri_agent():
    """
    Creates and returns the main Agri-Agent executor.
    """
    load_dotenv()

    # 1. Define the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

    # 2. Define the tools the agent can use
    tools = [get_weather_data, analyze_plant_image]

    # 3. Create the prompt template
    # This prompt is crucial. It tells the agent how to behave.
    prompt_template = """
    You are Agri-Agent, a helpful AI assistant for farmers.
    Answer the user's questions as best as possible.
    You have access to the following tools:

    {tools}

    To use a tool, use the following format:
    
    Thought: Do I need to use a tool? Yes
    Action: The action to take, should be one of [{tool_names}]
    Action Input: The input to the action
    Observation: The result of the action

    When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:
    
    Thought: Do I need to use a tool? No
    Final Answer: [your response here]

    Begin!

    Previous conversation history:
    {chat_history}

    New input: {input}
    {agent_scratchpad}
    """
    prompt = PromptTemplate.from_template(prompt_template)
    
    # 4. Create the agent
    agent = create_react_agent(llm, tools, prompt)

    # 5. Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,  # Set to True to see the agent's thought process
        handle_parsing_errors=True,
        max_iterations=5,
    )
    
    return agent_executor