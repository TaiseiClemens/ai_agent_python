import os
import argparse
from prompts import system_prompt
from call_function import avaliable_functions, call_function
from constants import AGENT_ITERATION_LIMIT_COUNT
from google import genai
from google.genai import types
from dotenv import load_dotenv

from functions.get_files_info import get_files_info

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API key was not found.")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    is_finished = False
    iteration_count = 0
    while iteration_count < AGENT_ITERATION_LIMIT_COUNT and not is_finished:
        iteration_count += 1
        try:
            response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[avaliable_functions],
                        system_instruction=system_prompt
                    )
                )
            
            if not response.usage_metadata:
                raise RuntimeError("usage_metadata property is none. API request likely failed")
            
            if response.candidates and response.text:
                is_finished = True

            for candidate in response.candidates:
                messages.append(candidate.content)

               
            if args.verbose:
                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            #if not response.function_calls:
            if is_finished:
                print("Final response: ")
                print(response.text)

            function_responses = []

            function_calls = response.function_calls if response.function_calls else []
            for function_call in function_calls:
                #print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call)
                if not function_call_result.parts:
                    raise Exception("call_function should not return an empty .parts list.")
                function_response = function_call_result.parts[0].function_response
                if not function_response:
                    raise Exception("function_response should not be of None type")
                function_result = function_response.response
                if not function_result:
                    raise Exception("function_result should not be of None type")
                if args.verbose:
                    print(f"-> {function_result}")
                function_responses.append(function_call_result.parts[0])
            messages.append(types.Content(parts=function_responses, role="user"))
        except Exception as e:
            raise e

if __name__ == "__main__":
    main()

