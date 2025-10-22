import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file you want to add or overwrite content to, if it does not exist create the file.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that should be written to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    joined = os.path.join(working_directory, file_path)
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(joined)
    checked = os.path.commonpath([abs_working, abs_target]) == abs_working
    if not checked:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    os.makedirs(os.path.dirname(abs_target), exist_ok=True)

    try:
        with open(abs_target, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"