import openai
import json
from dotenv import load_dotenv

# set OpenAI key
load_dotenv()

# Example dummy function hard coded to return the same stock prices
# In production, this could be an API call to a financial data service

def get_stock_price(ticker, market="NYSE"):
    """Get the current stock price for a given ticker symbol"""
    if "AAPL" in ticker.upper():
        return json.dumps({"ticker": ticker, "price": "150", "market": "NASDAQ"})
    elif "TSLA" in ticker.upper():
        return json.dumps({"ticker": ticker, "price": "900", "market": "NASDAQ"})
    else:
        return json.dumps({"ticker": ticker, "price": "Unknown", "market": market})

def run_conversation():
    # Step 1: send the conversation and available functions to the model
    messages = [{"role": "user", "content": "What's the stock price for AAPL, TSLA, and GOOG?"}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_stock_price",
                "description": "Get the current stock price for a given ticker symbol",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "The stock ticker symbol, e.g. AAPL for Apple Inc.",
                        },
                        "market": {"type": "string", "enum": ["NYSE", "NASDAQ"]},
                    },
                    "required": ["ticker"],
                },
            },
        }
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto", 
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        available_functions = {
            "get_stock_price": get_stock_price,
        } 
        messages.append(response_message) 
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            print("tool_call", tool_call)
            function_response = function_to_call(
                ticker=function_args.get("ticker"),
                market=function_args.get("market"),
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  
        second_response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        ) 
        return second_response
print(run_conversation())

print()
print("2nd run")
print()
print(run_conversation().choices[0].message.content)
