from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
import sys
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.env_agent import EnvAgent
from utils.tool_collection.data_analysis_tool import analyze_data_tool
from utils.tool_collection.file_tool import load_file_tool, write_file_tool
from utils.tool_env import ToolEnv
from utils.var_env import VarEnv
from agent.llm import LLM

app = FastAPI()

tool_env = ToolEnv()
var_env = VarEnv()
tool_env.register_tool([analyze_data_tool, load_file_tool])
agent = EnvAgent(LLM(), tool_env, var_env)

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return FileResponse("ui.html")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = file.filename # type: ignore
    with open(file_path, "wb") as buffer: # type: ignore
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "status": "success"}

@app.post("/chat")
async def chat(message: str = Form(...)):
    msg = agent.call(message)
    return {"reply": msg}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    