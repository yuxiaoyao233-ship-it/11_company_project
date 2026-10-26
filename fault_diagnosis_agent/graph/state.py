# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      state.py
# Author:       wyh
# ---------------------------------------------------------------------------
# 定义个State字典，用来在各个Agent之间传递数据
# 导包
from typing import TypedDict, Optional, List
from models.schemas import PreprocessResult

class DiagnosisState(TypedDict):
    """系统的共享状态，贯穿所有节点"""
    raw_input: str                  # 原始输入
    preprocess_result: Optional[PreprocessResult]   # 预处理结构化结果
    detected_issues: List[str]      # 异常识别结果
    vector_context: List[str]       # 向量库检索到的历史案例
    graph_context: List[str]        # 图谱推理出的可能根因
    root_causes: List[str]          # 根因分析最终确认的根因
    solution: str                   # 维修方案
    retry_count: int               # 重试计数（用于回退逻辑）


