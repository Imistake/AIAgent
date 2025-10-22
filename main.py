import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.config import system_prompt
from call_function import available_functions, call_function

def parse_args(argv):
    verbose = "--verbose" in argv
    # collect non-flag args as the prompt parts
    args = [a for a in argv[1:] if not a.startswith("--")]
    return verbose, args

def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing. Check your .env and load_dotenv() location.")
    return genai.Client(api_key=api_key)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            ),
    )

    # Verbose token usage
    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)

            if not function_call_result.parts or not hasattr(function_call_result.parts[0], 'function_response'):
                raise Exception("Invalid function call result structure")
        
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response['result']}")

    else:
        print(response.text)

def main():
    load_dotenv()
    verbose, args = parse_args(sys.argv)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}")

    client = get_client()

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)

if __name__ == "__main__":
    main()