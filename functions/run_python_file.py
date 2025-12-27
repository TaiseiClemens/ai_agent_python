import os
from google.genai import types
import subprocess

def run_python_file(working_directory, file_path, args=None):
    absolute_working_directory = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(os.path.join(absolute_working_directory, file_path))
    valid_working_directory = os.path.commonpath([absolute_working_directory, absolute_file_path]) == absolute_working_directory

    if not valid_working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory)'
    if not os.path.isfile(absolute_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if file_path[-3:] != '.py':
        return f'Error: "{file_path}" is not a Python file'

    try:
        command = ["python", absolute_file_path]
        if args:
            command.extend(args)
        output = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output_string = ""
        if output.returncode != 0:
            output_string += "Process exited with code {output.returncode}"
        if not output.stdout and not output.stderr:
            output_string += "No output produced"
        else:
            output_string += f"STDOUT:{output.stdout}"
            output_string += f"STDERR:{output.stderr}"
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to file you want to run, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="If the python file takes arguments you can provide them here",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
        required=["file_path"],
    ),
)

