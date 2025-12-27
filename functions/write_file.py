import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    file_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, file_abs]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(file_abs):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
        
    try:
        # Make necessary directories
        os.makedirs(os.path.dirname(file_abs), exist_ok=True)
        with open(file_abs, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file. If the file does not exist, or directory structure to file does not exist it will be automatically generated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to file you want to write to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                description="The content you want to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

