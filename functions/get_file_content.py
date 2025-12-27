import os
from google.genai import types
from constants import MAX_CHARS

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    file_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, file_abs]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{working_directory}" as it is outside the permitted working directory'
    if not os.path.isfile(file_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(file_abs, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of a file up to 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to file you want to get the contents, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"]
    ),
)
