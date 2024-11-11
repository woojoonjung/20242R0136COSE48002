import transformers
import torch
from peft import get_peft_model, LoraConfig, TaskType
from huggingface_hub import login
from dotenv import load_dotenv
import os

# Hugging Face 로그인 및 환경 변수 설정
load_dotenv()
hf_token = os.getenv("HF_TOKEN")
login(token=hf_token)

# 모델 이름 정의
model_name = "meta-llama/Meta-Llama-3-8B-Instruct"

class Generator:
    def __init__(self):
        # Llama 모델을 로드하면서 `LoRA` 설정 적용
        model = transformers.LlamaForCausalLM.from_pretrained(
            model_name,
            use_auth_token=hf_token,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        print("모델이 성공적으로 로드되었습니다.")

        # LoRA 설정
        self.lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=4,
            lora_alpha=32,
            lora_dropout=0.1
        )
        # LoRA 적용
        self.model = get_peft_model(model, self.lora_config)
        self.tokenizer = transformers.LlamaTokenizerFast.from_pretrained(model_name)

        # Text generation 파이프라인 설정
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto"
        )

    def generate_response(self, retrieved_docs):
        # 입력 텍스트 생성
        input_text = "당신은 친절한 의사입니다.".join(retrieved_docs) + "\n위의 질환을 갖고 있는 환자에게 간단한 진단 및 행동 지침에 대해 안내해주세요."
        
        # 파이프라인을 통해 텍스트 생성
        outputs = self.pipeline(input_text, max_new_tokens=400)
        response = outputs[0]["generated_text"]
        
        return response