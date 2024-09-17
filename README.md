# translator_ko2en
The translator that converts Korean to English using Gemma.
## Environment
- Ubuntu 22.04LTS  
- Python 3.10  
- [torch](https://pytorch.org/get-started/locally/)
- [transformers](https://huggingface.co/docs/transformers/installation)
- [peft](https://huggingface.co/docs/peft/install)
- [huggingface-cli](https://huggingface.co/docs/huggingface_hub/main/ko/guides/cli)
- [pyperclip](https://pypi.org/project/pyperclip/)
- [bitsandbytes](https://pypi.org/project/bitsandbytes/)
- [flash-attn](https://pypi.org/project/flash-attn/)
## How to use
![image](https://github.com/user-attachments/assets/2bf2c83e-4712-42f6-94b5-1cdcc9d232fc)

0. Sign in huggingface-cli
1. Run `main.py`
2. Enter the Korean text you want to translate to English.
3. To save the translation, enter 's'. To copy the translation to the clipboard, enter 'c'. You can use both options together.
## Reference
[Model](https://huggingface.co/brildev7/gemma-1.1-7b-it-translation-koen-sft-qlora)
