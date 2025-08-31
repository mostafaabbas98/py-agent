import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
from prompt import system_prompt

MAX_AI = 20

def main():
    load_dotenv()

    args = sys.argv[1:]
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    
    verbose_flag = "--verbose" in args
    # Remove flags from args before building the prompt
    args = [arg for arg in args if not arg.startswith("--")]
    user_prompt = " ".join(args)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    try:
        call_number = 0
        while call_number < MAX_AI:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages, 
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
            )

            if len(response.candidates) > 0:
                for candidate in response.candidates:
                    messages.append(types.Content(role= candidate.content.role, parts=candidate.content.parts))

            if verbose_flag:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if response.function_calls:
                for fun_call in response.function_calls:
                    res = call_function(fun_call, verbose=verbose_flag)
                    if len(res.parts) > 0 :
                        messages.append(types.Content(role= "user", parts=res.parts))
                    if not res.parts[0].function_response.response:
                        raise Exception("error!!!")
                    if verbose_flag:
                        print(f"-> {res.parts[0].function_response.response}")
            else:
                print(f"Final response:\n{response.text}")
                break
            
            call_number += 1
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
