import os

def get_files_info(working_directory, directory="."):
  full_path = os.path.join(working_directory, directory)

  abs_working = os.path.abspath(working_directory)
  abs_full_path = os.path.abspath(full_path)
  
  if not abs_full_path.startswith(abs_working):
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
  
  try:
    if not os.path.isdir(abs_full_path):
      return f'Error: "{directory}" is not a directory'
    
    result = []
    for file in os.listdir(abs_full_path):
      file_path = os.path.join(abs_full_path, file)
      size = os.path.getsize(file_path)
      is_dir = os.path.isdir(file_path)
      result.append(f"- {file}: file_size={size} bytes, is_dir={is_dir}")

    return "\n".join(result)
  except Exception as e:
    return f"Error: {e}"