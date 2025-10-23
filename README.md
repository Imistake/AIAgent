Description:
A small command-line agent that uses Google’s Gemini to analyze and modify a simple calculator project by iteratively calling tools. It maintains a conversation history, asks the model what to do next, executes tool calls (like listing files, reading file contents, running Python, or writing files), feeds the tool results back into the conversation, and repeats until the model returns a final answer.

Key features:

Conversation loop with a max-iteration cap and error handling.

Appends model replies and tool results to shared message history each turn.
    
Tooling:
    - get_files_info: list files in the calculator workspace.
    - get_file_content: read specific file contents.
    - run_python_file: execute a Python file and capture output.
    -   write_file: write content to a file.

Prints function calls (e.g., “- Calling function: get_files_info”) and final model response.
