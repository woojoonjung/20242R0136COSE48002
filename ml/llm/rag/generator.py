from transformers import LlamaTokenizer, LlamaForCausalLM, LlamaTokenizerFast
from huggingface_hub import login
from dotenv import load_dotenv
import os

load_dotenv()

hf_token = os.getenv("HF_TOKEN")
login(token=hf_token)

model_name = "meta-llama/Meta-Llama-3-8B-Instruct"

class Generator:
    def __init__(self):
        self.generator = LlamaForCausalLM.from_pretrained(model_name).to("cuda")
        self.tokenizer = LlamaTokenizerFast.from_pretrained(model_name)

    def generate_response(self, retrieved_docs):
        input_text = "당신은 친절한 의사입니다.".join(retrieved_docs) + "\n위의 질환을 갖고 있는 환자에게 간단한 진단 및 행동 지침에 대해 안내해주세요."
        inputs = self.tokenizer(input_text, return_tensors="pt")
        outputs = self.generator.generate(inputs["input_ids"], max_length=400)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response