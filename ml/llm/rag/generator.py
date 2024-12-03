from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import get_peft_model, LoraConfig, TaskType
from huggingface_hub import login
from dotenv import load_dotenv
import os
import torch

login(add_to_git_credential=True)
load_dotenv()

hf_token = os.getenv("HF_TOKEN")
login(token=hf_token)

model_name = "Bllossom/llama-3.2-Korean-Bllossom-3B"

class Generator:
    def __init__(self):
        # model = LlamaForCausalLM.from_pretrained(model_name).to("cuda")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=4,
            lora_alpha=32,
            lora_dropout=0.1
        )
        self.generator = get_peft_model(model, self.lora_config)
        # self.tokenizer = LlamaTokenizerFast.from_pretrained(model_name)

    def generate_response(self, retrieved_docs):
        input_text = "당신은 친절한 의사입니다.".join(retrieved_docs) + "\n위의 질환을 갖고 있는 환자에게 간단한 진단 및 행동 지침에 대해 안내해주세요."
        inputs = self.tokenizer(input_text, return_tensors="pt").to("cuda")
        print(len(inputs))
        outputs = self.generator.generate(inputs["input_ids"], max_length=2048)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response