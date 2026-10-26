# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      config.py
# Author:       wyh
# ---------------------------------------------------------------------------
# 导包
import os
from pathlib import Path

# 1. 获取项目根路径
BASE_DIR = Path(__file__).resolve().parent

# 2. 定义数据目录
DATA_DIR = BASE_DIR / 'data'
CASES_DIR = DATA_DIR / 'cases'
GRAPH_DIR = DATA_DIR / 'graph'

# 3. 定义具体的文件路径
EQUIPMENT_GRAPH_DIR = GRAPH_DIR / 'equipment_graph.json'

# 4. 定义向量数据库目录
CHROMA_DB_DIR = BASE_DIR / 'chroma_db'

# 5. 挂载前端静态文件（把 fronted/ 目录作为静态资源）
FRONTEND_DIR = BASE_DIR / "frontend"

