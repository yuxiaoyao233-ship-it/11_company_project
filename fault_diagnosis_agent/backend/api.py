# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      api.py
# Author:       wyh
# ---------------------------------------------------------------------------
# 写一个/apo/diagnose接口
# 接受文字——> 调用LangGraph工作流——>把State打包成JSON返回
# 导包
import os.path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from pydantic import BaseModel

from config import FRONTEND_DIR
from graph.workflow import build_workflow

app = FastAPI(title="工业设备故障诊断多Agent系统")

# 编译一次工作流，全局复用（避免每次请求都重新建图）
diagnosis_app = build_workflow()

# 请求体模型
class DiagnoseRequest(BaseModel):
    fault_description : str

# 核心诊断接口
@app.post('/api/diagnose')
def diagnose(req: DiagnoseRequest):
    initial_state = {
        'raw_input': req.fault_description,
        'retry_count': 0,
    }
    # 执行LangGraph工作流
    result = diagnosis_app.invoke(initial_state)

    pre = result['preprocess_result']
    # 组装成前端友好的JSON
    return {
        "device_type": pre.device_type,
        "severity": pre.severity,
        "fault_phenomenon": pre.fault_phenomenon,
        "keywords": pre.keywords,
        "detected_issues": result.get("detected_issues", []),
        "graph_causes": result.get("graph_context", []),
        "vector_cases": result.get("vector_context", []),
        "root_causes": result.get("root_causes", []),
        "solution": result.get("solution", ""),
    }

# 挂载前端静态文件（把fronted/目录作为静态资源）放在所有API路由之后

@app.get('/')
def index():
    return FileResponse(os.path.join(str(FRONTEND_DIR),'index.html'))

app.mount('/static',StaticFiles(directory=str(FRONTEND_DIR)),name='static')


