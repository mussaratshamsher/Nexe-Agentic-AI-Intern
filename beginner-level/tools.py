from agents import function_tool
import re

@function_tool
def calculate(expression: str) -> str:
    """
    Safely evaluate a basic math expression string (+, -, *, /).
    
    Args:
        expression: A string containing a math expression like '2 + 2' or '(10 * 5) / 2'.
        
    Returns:
        The result as a string or an error message.
    """
    # Remove any whitespace
    clean_expression = expression.replace(" ", "")
    
    # Basic security: only allow digits, operators, and parentheses
    if not re.match(r'^[0-9+\-*/().]+$', clean_expression):
        return "Error: Invalid characters. Only numbers and +, -, *, /, () are allowed."

    try:
        # Use eval with no globals or builtins for a layer of safety
        # result = eval(clean_expression, {"__builtins__": None}, {})
        # Note: In a production app, use a proper parser like 'simpleeval' or 'numexpr'.
        # For this beginner-level SDK demo, we use eval carefully.
        result = eval(clean_expression, {"__builtins__": None}, {})
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except Exception as e:
        return f"Error: Invalid expression ({str(e)})"
