import os
from .config import MAX_CHARS

def get_file_content(working_directory, file_path):
  full_path = os.path.join(working_directory, file_path)

  abs_working = os.path.abspath(working_directory)
  abs_file_path = os.path.abspath(full_path)
  print(abs_working)
  print(abs_file_path)

  if not abs_file_path.startswith(abs_working):
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.isfile(abs_file_path):
    return f'Error: File not found or is not a regular file: "{file_path}"'
  
  try:
    with open(abs_file_path, 'r') as f:
      file_content_string = f.read(MAX_CHARS + 1)
    
    if len(file_content_string) > MAX_CHARS:
      file_content_string = file_content_string[:MAX_CHARS] + f'[...File "{abs_file_path}" truncated at {MAX_CHARS} characters]'

    return file_content_string
  except Exception:
    return "Error: Failed read file content!"