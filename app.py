# app.py
import streamlit as st
from PIL import Image
from models.agent_creator import create_agri_agent
import os
import uuid

# --- Page Configuration ---
st.set_page_config(
    page_title="Agri-Agent: Your Smart Farming Assistant",
    page_icon="🧑‍🌾",
    layout="wide"
)

# --- Ensure a temporary directory for images exists ---
if not os.path.exists('temp'):
    os.makedirs('temp')

# --- Title and Description ---
st.title("🧑‍🌾 Agri-Agent: The Next-Generation Farming Assistant")
st.markdown("Welcome! Ask me about farming, get weather forecasts, or upload a plant image for disease analysis.")

# --- Initialize the Agent and Chat History ---
if 'agent_executor' not in st.session_state:
    with st.spinner("🌱 Preparing the AI assistant..."):
        st.session_state.agent_executor = create_agri_agent()
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display existing chat messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Main Interaction Logic (View & Controller) ---
uploaded_file = st.file_uploader("Upload an image of a plant leaf for analysis:", type=["jpg", "jpeg", "png"])
prompt = st.chat_input("Ask me anything about your farm...")

# Prepare the input for the agent
agent_input = {"input": "", "chat_history": []}
absolute_file_path = None # Use a more descriptive name

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    file_extension = os.path.splitext(uploaded_file.name)[1]
    temp_file_path = os.path.join("temp", f"{uuid.uuid4()}{file_extension}")
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # *** THE KEY FIX: Convert the relative path to an absolute path ***
    absolute_file_path = os.path.abspath(temp_file_path)
    
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Plant Leaf', use_column_width=True)
    st.info("Image uploaded successfully! Please ask your question in the chat box below.")


if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Construct the final prompt for the agent
    final_prompt = prompt
    if absolute_file_path:
        # Update the prompt with the absolute path for clarity
        final_prompt += f" [CONTEXT: The user has uploaded an image. Its absolute file path is: '{absolute_file_path}']"
    
    agent_input["input"] = final_prompt
    agent_input["chat_history"] = st.session_state.messages

    # Get response from the agent
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            response = st.session_state.agent_executor.invoke(agent_input)
            response_text = response['output']
            st.markdown(response_text)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})