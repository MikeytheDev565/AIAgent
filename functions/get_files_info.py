import os
from config import character_limit

def get_files_info(working_directory, directory='.'):
    
    target = os.path.abspath(os.path.join(working_directory, directory))
    full_path = os.path.join(working_directory, directory)
    abs_work = os.path.abspath(working_directory)
    abs_work_with_sep = abs_work if abs_work.endswith(os.sep) else abs_work + os.sep


    try:
        if not (target == abs_work or target.startswith(abs_work_with_sep)):
            return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(full_path):
            return (f'Error: "{directory}" is not a directory')
        list_dir = os.listdir(full_path)
        files = []
        for file in list_dir:
            
            files.append(f"-{file} : file_size={os.path.getsize(os.path.join(full_path, file))}, is_dir={os.path.isdir(os.path.join(full_path, file))}")
        
            
            



        
    
        return "\n".join(files)
    except Exception as e:
        return f"Error: {e}"
    
def get_file_content(working_directory, file_path):
    
    target = os.path.abspath(os.path.join(working_directory, file_path))
    abs_work = os.path.abspath(working_directory)
    abs_work_with_sep = abs_work if abs_work.endswith(os.sep) else abs_work + os.sep

    try:
        if not ( target.startswith(abs_work_with_sep)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        

        with open(target, "r") as f:
            file_content_string = f.read(character_limit)
        
        if len(file_content_string) == 10000:
            file_content_string = file_content_string + f'" {file_path}" truncated at 10000 characters'
        
        return file_content_string





    except Exception as e:
        return f'Error: {e}'
