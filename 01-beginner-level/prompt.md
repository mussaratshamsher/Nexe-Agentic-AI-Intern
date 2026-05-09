Build a complete beginner-level AI Agent web app using Python, Streamlit, and OpenAI Agents SDK.

Requirements:

1. The app must be a Streamlit application that can run locally and be deployed on Streamlit Cloud and uses free tier llm (free tier only).

2. Use OpenAI Agents SDK with clean folder structure to create an AI agent that supports:

   * Tool calling (function calling)
   * Structured JSON output
   * Basic decision-making (detect math queries vs normal queries)

3. Implement a calculator tool:

   * Accept a math expression as string input
   * Safely evaluate operations (+, -, *, /)
   * Handle errors (invalid input, division by zero)
   * Return result as string

4. Agent behavior:

   * If user input is a math query → call calculator tool
   * Otherwise → respond normally
   * Always return structured JSON like:
     {
     "input": "...",
     "tool_used": "...",
     "result": "...",
     "status": "success" or "error"
     }

5. Memory:

   * Store last 5 conversations using Streamlit session_state
   * Display chat history in UI

6. UI (Streamlit):

   * Simple chat interface
   * Input box + response display
   * Section to show JSON output
   * Section to show chat history

7. Error Handling:

   * Handle tool errors gracefully
   * Ensure app never crashes

8. Code structure:

   * Keep everything simple and beginner-friendly
   * Can be in a single file OR small modular files (agent.py, tools.py)

9. Deployment:

   * Must work on Streamlit Cloud (no paid APIs except OpenAI free tier)
   * Use environment variable for API key

10. Output:

* Provide complete working code
* Include requirements.txt
* Include instructions to run locally and deploy

Keep the UI minimal, clean, and functional. Focus on working logic, not design.
   

# command to run application
uv run streamlit run app.py  