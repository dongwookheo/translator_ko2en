import re
from translator.translator import TranslatorKorEng
from utils.tools import copy_to_clipboard, save_to_file


def handle_output(output: str) -> None:
    """Handle the output of the translator.

    Parameters
    ----------
    output : str
        The output of the translator

    If the user wants to copy the output to the clipboard,
    save it to a file, or cancel the translation.
    "c" for copy, "s" for save, "q" for cancel, and "cs" or "sc" for both.
    """
    actions = {
        "c": lambda: copy_to_clipboard(output),
        "s": lambda: save_to_file(output, "translated.txt", "a"),
        "q": lambda: print("현재 문장의 번역을 취소합니다."),
        "cs": lambda: (
            copy_to_clipboard(output),
            save_to_file(output, "translated.txt", "a"),
        ),
        "sc": lambda: (
            save_to_file(output, "translated.txt", "a"),
            copy_to_clipboard(output),
        ),
    }

    while True:
        choice = input(
            "현재 출력을 어떻게 하시겠습니까? 복사(c)/저장(s)/취소(q): "
        ).lower()
        action = actions.get(choice)

        if action:
            action()
            return
        print("잘못된 입력입니다. 다시 입력해주세요.")


if __name__ == "__main__":
    translator = TranslatorKorEng()

    while "q" not in (
        passage := input(
            "영어로 번역하고 싶은 문장을 입력하세요. ('q'를 입력하면 종료됩니다): "
        ).lower()
    ):

        print(output := translator.translate(passage))
        translated = re.search(f"output:\s*(.*)", output, re.DOTALL).group(1).strip()

        handle_output(translated)
    else:
        print("번역기를 종료합니다.")
