import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.call_function import call_function
from config import iteration_limit


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of files.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to get content from a file from, relative to the working directory. If not provided, will provide an error.",
            ),
        },
    ),
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="This function runs a python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the python file that will run , relative to the working directory. If not provided, will provide an error.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="The list of optional arguments that will be past into the python file.",
            ),
            
        },
        required=["file_path"],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="This function will write to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to where the file will be written to, relative to the working directory. If not provided, will provide an error.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="A string containing all that will be written into a file.",
            )
        }
    )
)




available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


if len(sys.argv) < 2:
    raise Exception("No prompt")
prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons. If asked about a calculator it is in the working directory.
"""
iteration = 0
while iteration < iteration_limit:
    try:
        iteration+=1
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig( tools=[available_functions],system_instruction=system_prompt),
        )
        if response.candidates:
            for candidate in response.candidates:
                function_call_content = candidate.content
                messages.append(function_call_content)


        



        prompt_token_counts = response.usage_metadata.prompt_token_count
        candidates_token_counts = response.usage_metadata.candidates_token_count


        if (not response.function_calls) and response.text:
            if "--verbose" in sys.argv:
                print(f"User prompt: {prompt}")
                print(f"Prompt tokens: {prompt_token_counts}")
                print(f"Response tokens: {candidates_token_counts}")
                print(f"Final response: {response.text}")
            else:
                print(response.text)
            break
        
       




        tool_responses = []


        if response.function_calls is not None:
            for x in response.function_calls:
                #print(f"Calling function: {x.name}({x.args})")
                if "--verbose" in sys.argv:
                    thing = call_function(x, True)
                    print(f"-> {thing.parts[0].function_response.response}")
                else:
                    thing = call_function(x)
                part = thing.parts[0]
                if part.function_response is None:
                    raise Exception("Norespnse")
                if part.function_response.response is None:
                    raise Exception("No response.response")
                
                tool_responses.append(part)
        if tool_responses:
            messages.append(types.Content(role="user", parts=tool_responses))
    
        
    except Exception as e:
        print(f"Error: {e}")




