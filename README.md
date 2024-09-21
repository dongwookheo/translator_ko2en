# translator_ko2en
[translator_ko2en.py](https://github.com/dongwookheo/translator_ko2en/blob/main/translator_ko2en.py): The translator that converts Korean to English using Gemma.  
[abstract_translator.py](https://github.com/dongwookheo/translator_ko2en/blob/main/abstract_translator.py): The translator that extracts the abstract and translates it into Korean the conference paper using OpenAI API.  
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
- [openai](https://pypi.org/project/openai/)
## How to use
### translator_ko2en.py
![image](https://github.com/user-attachments/assets/2bf2c83e-4712-42f6-94b5-1cdcc9d232fc)

0. Sign in huggingface-cli
1. Run `translator_ko2en.py`  
2. Enter the Korean text you want to translate to English.
3. To save the translation, enter 's'. To copy the translation to the clipboard, enter 'c'. You can use both options together.

### abstract_translator.py
0. Sign in openai and get the API key.
1. Run `abstract_translator.py`  
    ```bash
    python3 abstract_translator.py -c <conference_name> -y <year> -p <number_of_paper_to_translate> -k <api_key>
    ```
## Reference
[Model](https://huggingface.co/brildev7/gemma-1.1-7b-it-translation-koen-sft-qlora)  
[arxiv_gpt_korean_translator](https://github.com/gisbi-kim/arxiv_gpt_korean_translator)  
