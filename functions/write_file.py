import os
from google.genai import types

def write_file(working_directory, file_path, content):
  full_path = os.path.join(working_directory, file_path)

  abs_working = os.path.abspath(working_directory)
  abs_file_path = os.path.abspath(full_path)

  if not abs_file_path.startswith(abs_working):
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.exists(abs_file_path):
    try:
      os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
      with open(abs_file_path, "w") as f:
        pass
    except Exception:
      return f"Error: failed create missing file at: {file_path}"
    
  try:
    with open(abs_file_path, "w") as f:
      f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception:
    return f"Error: failed to write in {file_path}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the specified directory, creating the file and any missing directories if needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory. Must be within working directory boundaries.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)