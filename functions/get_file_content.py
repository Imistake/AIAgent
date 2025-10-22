import os
from functions.config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a single file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file you want to read, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    joined = os.path.join(working_directory, file_path)
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(joined)
    checked = os.path.commonpath([abs_working, abs_target]) == abs_working
    if not checked:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(abs_target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_target, "r") as f:
            content = f.read(MAX_CHARS + 1)
        is_truncated = len(content) > MAX_CHARS
        visible = content[:MAX_CHARS]
        if is_truncated:
            return visible + "\n" f'[...File "{file_path}" truncated at 10000 characters]'
        return visible
    except Exception as e:
        return f"Error: {e}"
            

