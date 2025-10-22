import os
import subprocess
import sys
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file you want to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Optional list of arguments passed to the python file."
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    joined = os.path.join(working_directory, file_path)
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(joined)
    checked = os.path.commonpath([abs_working, abs_target]) == abs_working
    if not checked:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    elif not os.path.isfile(abs_target):
        return f'Error: File "{file_path}" not found.'
    
    
    try:
        completed = subprocess.run(
            [sys.executable, file_path, *args],
            cwd = abs_working,
            timeout=30, 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            )
        if not completed.stdout and not completed.stderr:
            return "No output produced."
    
        result = f"STDOUT:{completed.stdout}STDERR:{completed.stderr}"
           
        if completed.returncode != 0:
            return result + f"\nProcess exited with code {completed.returncode}"
        if completed.returncode == 0:
            return result
    
    
    except Exception as e:
        return f"Error: executing Python file: {e}"