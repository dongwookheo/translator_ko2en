def copy_to_clipboard(text: str) -> None:
    """Copy the given text to the clipboard.

    Parameters
    ----------
    text : str
        The text to be copied
    """
    import pyperclip

    pyperclip.copy(text)
    print("클립보드에 복사되었습니다.")


def save_to_file(text: str, file_path: str, mode: str = "a") -> None:
    """Save the given text to the file.

    Parameters
    ----------
    text : str
        The text to be saved
    file_path : str
        The path to the file
    mode : str, optional
        The mode to open the file, by default "a"
    """
    with open(file_path, mode) as f:
        f.write(text + "\n\n")  # Add EOF
    print("파일에 저장되었습니다.")
