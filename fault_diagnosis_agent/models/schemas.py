# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      schemas.py
# Author:       wyh
# ---------------------------------------------------------------------------
# 使用pydantic定义数据结构
# 导包
from pydantic import BaseModel, Field
from typing import List, Optional

# 定义数据预处理智能体的输出结构
class PreprocessResult(BaseModel):
    """数据预处理智能体输出结构"""
    device_type: str = Field(description="设备类型，例如：电机、水泵、压缩机、变频器")
    fault_phenomenon: str = Field(description="故障现象的简洁描述")
    possible_causes: List[str] = Field(description="初步可能原因列表")
    keywords: List[str] = Field(description="提取用于后续检索的核心关键词")
    severity: str = Field(description="严重程度评估：低 / 中 / 高")
    uncertainty: Optional[str] = Field(
        default=None,
        description="原文中缺失、模糊或需要人工确认的信息，如果没有则填None"
    )
