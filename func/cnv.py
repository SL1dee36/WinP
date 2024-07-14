import os

def get_file_path():
    """
    Ask user for the file path and validate its existence.

    Returns:
    str: Validated file path entered by the user.
    """
    file_path = input("Enter the file path: ")
    while not os.path.exists(file_path):
        print("File does not exist. Please enter a valid file path.")
        file_path = input("Enter the file path: ")
    return file_path

def get_file_extension(file_path):
    """
    Get the current file extension from the file path.

    Args:
    file_path (str): Path to the file.

    Returns:
    str: Current file extension.
    """
    return os.path.splitext(file_path)[1]

def convert_file_type(file_path, new_extension):
    """
    Convert the file type to the specified new file extension.

    Args:
    file_path (str): Path to the file.
    new_extension (str): New file extension to which the file should be converted.

    Returns:
    str: Message indicating the success or failure of the file type conversion.
    """
    try:
        new_file_path = os.path.splitext(file_path)[0] + new_extension
        os.rename(file_path, new_file_path)
        return f"File type successfully converted to {new_extension}"
    except Exception as e:
        return f"An error occurred while converting the file type: {e}"

# Usage
file_path = get_file_path()
current_extension = get_file_extension(file_path)
print(f"The current file type is: {current_extension}")

new_extension = input("Enter the new file extension you want: ")
result = convert_file_type(file_path, new_extension)
print(result)