import os
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_file(file_path):
    """Reads content from a file and returns it as a list of lines."""
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Error reading from file {file_path}: {e}")
        return []

def write_file(file_path, lines):
    """Writes lines to a file."""
    try:
        with open(file_path, 'w') as file:
            file.writelines(lines)
    except Exception as e:
        logger.error(f"Error writing to file {file_path}: {e}")

def change_file_permissions(file_path, permissions):
    """
    Change permissions of a file.
    
    Args:
        file_path (str): Path to the file whose permissions need to be changed.
        permissions (int): New permissions mode represented as an octal number.
        
    Returns:
        bool: True if permissions were successfully changed, False otherwise.
    """
    try:
        os.chmod(file_path, permissions)
        logging.info(f"Permissions changed for {file_path}")
        return True
    except Exception as e:
        logging.error(f"Error changing permissions for {file_path}: {e}")
        return False

def update_file_content(file_path, version_string, build_num):
    """Updates the content of a file by replacing version_string with build_num."""
    lines = read_file(file_path)
    if lines:
        modified_lines = []
        for line in lines:
            # Perform the replacement directly using re.sub()
            modified_line = re.sub(f"{version_string}[\d]+", f"{version_string}{build_num}", line)
            modified_lines.append(modified_line)
        
        write_file(file_path, modified_lines)
        logger.info(f"Version number updated to {build_num} in {file_path}")

def main():
    # Get the source path from the environment variable
    source_path = os.environ.get('SourcePath')
    if not source_path:
        logger.error("Source path environment variable 'SourcePath' not found.")
        return
    
    # Get the build number from the environment variable
    build_num = os.environ.get('BuildNum')
    if not build_num:
        logger.error("Build number environment variable 'BuildNum' not found.")
        return
    
    file_permissions = 0o755 

    # Update SConstruct file
    sconstruct_path = os.path.join(source_path, 'develop', 'global', 'src', 'SConstruct')
    if change_file_permissions(sconstruct_path, file_permissions):
        print("Permissions changed successfully.")
        update_file_content(sconstruct_path, "point=", build_num)
    else:
        print("Failed to change permissions.")
    
    
    # Update VERSION file
    version_path = os.path.join(source_path, 'develop', 'global', 'src', 'VERSION')
    if change_file_permissions(version_path, file_permissions):
        print("Permissions changed successfully.")
        update_file_content(version_path, "ADLMSDK_VERSION_POINT=", build_num)
    else:
        print("Failed to change permissions.")

if __name__ == "__main__":
    main()
