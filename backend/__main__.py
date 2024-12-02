import uvicorn, os, torch

current_file_path = os.path.abspath(__file__)
print("Current file path:", current_file_path)

print("#####")
print(torch.__version__)  # PyTorch 버전 확인
print(torch.version.cuda)  # CUDA 버전 확인
print(torch.cuda.is_available())  # CUDA 가용성 확인

if __name__ == '__main__':
    uvicorn.run("main:app",host="0.0.0.0",port=1001, reload=True,workers=100)

