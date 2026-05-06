# Beginner-Level AI Agent Web App

This is a simple Streamlit application that demonstrates an AI Agent built using the **OpenAI Agents SDK**.

## Features
- **Tool Calling:** Uses a custom `calculate` function to solve math expressions.
- **Decision Making:** Automatically detects if a query is math-related or general conversation.
- **Structured Output:** Always returns responses in a clean JSON format.
- **Memory:** Remembers the last 5 conversations in the session.
- **UI:** A clean Streamlit chat interface.

## Prerequisites
- Python 3.10 or higher
- An OpenAI API Key (Free tier / `gpt-4o-mini` supported)

## Local Setup

1. **Clone the repository** (or copy the files).
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   streamlit run app.py
   ```
4. **Enter your OpenAI API Key** in the sidebar when the app opens.

## Deployment (Streamlit Cloud)

1. Push this code to a GitHub repository.
2. Connect your GitHub account to [Streamlit Cloud](https://share.streamlit.io/).
3. Deploy a "New App" and select your repository.
4. **Important:** Add your OpenAI API Key in the app settings:
   - Go to **Settings** -> **Secrets**.
   - Add: `OPENAI_API_KEY = "your-api-key-here"`
5. The app will now work without needing to enter the key in the sidebar.

## Project Structure
- `app.py`: The main Streamlit user interface.
- `agent_logic.py`: Logic for initializing and running the OpenAI Agent.
- `tools.py`: Contains the `calculate` tool logic.
- `requirements.txt`: List of required Python packages.
