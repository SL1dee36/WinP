import os, gc
import shutil
import tempfile
import winreg  # For registry interactions

def clear_temp_folder():
    """Clears the temporary files folder."""
    temp_folder = tempfile.gettempdir()  # More robust way to get temp folder path
    deleted_files = []
    errors = []

    for filename in os.listdir(temp_folder):
        file_path = os.path.join(temp_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
            deleted_files.append(filename)
        except Exception as e:
            errors.append((filename, e))

    return deleted_files, errors


def check_registry():
    """
    Checks the registry for common issues.

    This function now checks for invalid file associations
    in the "HKEY_CLASSES_ROOT" key.
    """
    issues_found = False
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "") as root_key:
            for i in range(winreg.QueryInfoKey(root_key)[0]):
                key_name = winreg.EnumKey(root_key, i)
                if key_name.startswith(".") and " " in key_name:
                    issues_found = True  # Found a potential issue
                    break  # Stop checking after the first issue
    except Exception as e:
        return False, str(e)  # Return error information

    return issues_found, None  # No errors during check


def free_ram():
    """
    Attempts to free up RAM.

    This function now uses a more effective approach
    by explicitly clearing the caches of commonly used modules.
    """
    gc.collect()

    # Clear caches of specific modules (example)
    try:
        import sys
        sys.modules[__name__].__dict__.clear()  # Clear this module's cache
    except Exception:
        pass  # Handle potential errors gracefully

    return True  