import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    try:
        names = os.listdir(target_dir)
        item_info = []
        for name in names:
            name_path = os.path.join(target_dir, name)
            file_size = os.path.getsize(name_path)
            is_dir = os.path.isdir(name_path)
            item_info.append(f"  - {name}: file_size={file_size}, is_dir={is_dir}")
        return f"Result for '{directory}' directory\n" + "\n".join(item_info)
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["directory"],
    ),
)
