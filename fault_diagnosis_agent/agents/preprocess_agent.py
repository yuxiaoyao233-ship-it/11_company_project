# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      preprocess_agent.py
# Author:       wyh
# ---------------------------------------------------------------------------
# 实现数据预处理智能体，负责把口语化故障描述整理成结构化的诊断输入
# 调用大模型并强制它输出上面定义的结构
# 把原来的独立函数改造成LangGraph的节点函数
# 导包
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import DiagnosisState
from models.llm import get_llm
from models.schemas import PreprocessResult

# 编写高质量的 System Prompt（系统提示词）
SYSTEM_PROMPT_TEST = """
你是工业设备故障诊断系统中的【数据预处理智能体】。
你的任务是把车间工人提供的口语化故障描述，整理成结构化的诊断输入。

要求：
1. 识别设备类型（如：水泵、电机、风机等）
2. 用一句话专业的话概括故障现象。
3. 提取 3-6 个初步可能的工程原因。
4. 提取 5-8 个用于检索的核心关键词（包含设备名、现象、部件名）。
5. 评估严重程度： 低、中、高（影响安全生产或导致停机为高）。
6. 如果原文缺少关键信息（如未说明设备型号、没有振动数据等），在 uncertainty 中指出。
"""

def preprocess_fault_description(raw_text: str) -> PreprocessResult:
    """
    输入原始故障描述，输出结构化预处理结果
    """
    llm = get_llm()
    # 强制大模型输出符合 PreprocessResult 结构的 JSON
    structured_llm = llm.with_structured_output(PreprocessResult)

    human_prompt = f"""
    车间工人上报的原始故障描述：
    {raw_text}
    
    请提取并整理信息。
    """

    messages = [
        SystemMessage(content=SYSTEM_PROMPT_TEST),
        HumanMessage(content=human_prompt)
    ]

    # 调用大模型
    res = structured_llm.invoke(messages)
    return res

# 定义LangGraph节点：数据预处理智能体 ——> 预处理
# 编写系统提示词
SYSTEM_PROMPT = """
你是数据预处理智能体。把车间口语化故障描述整理成结构化JSON。
提取设备类型、概括现象、提取3-6个初步原因、提取5-8个关键词、评估严重程度（低/中/高）。
"""

def preprocess_node(state: DiagnosisState):
    """LangGraph 节点：预处理"""
    print("\n--- [节点1] 数据预处理智能体运行中 ---")
    llm = get_llm()
    structured_llm = llm.with_structured_output(PreprocessResult)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f'原始故障描述：{state["raw_input"]}')
    ]
    result = structured_llm.invoke(messages)

    # 更新State
    return {"preprocess_result":result}