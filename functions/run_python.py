import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
  full_path = os.path.join(working_directory, file_path)

  abs_working = os.path.abspath(working_directory)
  abs_file_path = os.path.abspath(full_path)

  if not abs_file_path.startswith(abs_working):
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.exists(abs_file_path):
    return f'Error: File "{file_path}" not found.'
  
  _, ext = os.path.splitext(abs_file_path)
  if ext != ".py":
    return f'Error: "{file_path}" is not a Python file.'
  
  try:
    file_output = subprocess.run(
      ["python3", abs_file_path] + args,
      capture_output=True,
      text=True,
      cwd=abs_working,
      timeout=30,
    )

    parts = []
    if file_output.stdout:
        parts.append(f"STDOUT:{file_output.stdout}")
    if file_output.stderr:
        parts.append(f"STDERR:{file_output.stderr}")
    if file_output.returncode != 0:
        parts.append(f"Process exited with code {file_output.returncode}")

    if not parts:
        return "No output produced."

    return "\n".join(parts)
  except Exception as e:
    return f"Error: executing Python file: {e}"