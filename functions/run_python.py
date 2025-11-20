import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    
    
    target = os.path.abspath(os.path.join(working_directory, file_path))
    abs_work = os.path.abspath(working_directory)
    abs_work_with_sep = abs_work if abs_work.endswith(os.sep) else abs_work + os.sep
    


    if not target.startswith(abs_work_with_sep):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not target.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    if (not os.path.exists(target)):
        return f'Error: File "{file_path}" not found.'

    
    
    

    try:
        
        command = ["python", target]
        
        process = subprocess.run(args=command + args,  timeout=30, capture_output=True,text=True)

        if not process.stderr and not process.stdout:
            return f"No output produced."

        if process.returncode != 0:
            return f"STDOUT: {process.stdout} STDERR: {process.stderr} Process exited with code {process.returncode}"
        
        return f"STDOUT: {process.stdout} STDERR: { process.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"