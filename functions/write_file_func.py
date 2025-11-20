import os

def write_file(working_directory, file_path, content):
    
    target = os.path.abspath(os.path.join(working_directory, file_path))
    abs_work = os.path.abspath(working_directory)
    abs_work_with_sep = abs_work if abs_work.endswith(os.sep) else abs_work + os.sep
    #print(target)


    if not ( target.startswith(abs_work_with_sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
      
      if os.path.exists(file_path):

        with open(target, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
      else:
            os.makedirs(os.path.dirname(target))
            with open(target, "w") as f:
                f.write(content)
        
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    

    

    except Exception as e:
       return f'Error: {e}'
    