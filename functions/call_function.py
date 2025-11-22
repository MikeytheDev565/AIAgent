
from google.genai import types
from .get_files_info import get_files_info
from .get_files_info import  get_file_content
from .run_python import run_python_file
from .write_file_func import write_file

def call_function(function_call_part, verbose=False):
    
    working_directory = "./calculator"
    function_name = function_call_part.name
    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}")
    if function_name == "get_files_info":
        function_result = get_files_info(working_directory=working_directory, **function_call_part.args)
    elif function_name == "get_file_content":
        function_result = get_file_content(working_directory=working_directory, **function_call_part.args)
    elif function_name == "run_python_file":
        function_result = run_python_file(working_directory=working_directory, **function_call_part.args)
    elif function_name == "write_file":
        function_result = write_file(working_directory=working_directory, **function_call_part.args)
    
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)

