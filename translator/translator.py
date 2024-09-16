import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel


class TranslatorKorEng:
    def __init__(
        self,
        model_id="google/gemma-1.1-7b-it",
        peft_model_id="brildev7/gemma-1.1-7b-it-translation-koen-sft-qlora",
        max_new_tokens=1024,
        temperature=0.2,
        top_p=0.95,
        do_sample=True,
        use_cache=False,
    ):
        model_id = model_id
        peft_model_id = peft_model_id
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
        )

        tokenizer = AutoTokenizer.from_pretrained(model_id)
        tokenizer.pad_token_id = tokenizer.eos_token_id

        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=quantization_config,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            attn_implementation="flash_attention_2",
        )
        model = PeftModel.from_pretrained(model, peft_model_id)

        self._model = model
        self._tokenizer = tokenizer
        self._max_new_tokens = max_new_tokens
        self._temperature = temperature
        self._top_p = top_p
        self._do_sample = do_sample
        self._use_cache = use_cache

    def translate(self, passage):
        prompt_template = """
        Translate the following into English:
        {}

        output:
        """
        prompt = prompt_template.format(passage)

        inputs = self._tokenizer(prompt, return_tensors="pt").to(self._model.device)
        outputs = self._model.generate(
            **inputs,
            max_new_tokens=self._max_new_tokens,
            temperature=self._temperature,
            top_p=self._top_p,
            do_sample=self._do_sample,
            use_cache=self._use_cache,
        )
        return self._tokenizer.decode(outputs[0], skip_special_tokens=True)
