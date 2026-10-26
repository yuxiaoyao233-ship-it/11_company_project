# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      root_cause_agent.py
# Author:       wyh
# ---------------------------------------------------------------------------
# 根因分析智能体，结合双引擎结果，让大模型做推理
# 导包
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import DiagnosisState
from models.llm import get_llm

def root_cause_node(state: DiagnosisState):
    """LangGraph 节点：根因分析"""
    print("\n--- [节点3] 根因分析智能体运行中 ---")
    llm = get_llm()

    vector_info = "\n".join(state.get('vector_context',[]))
    graph_info = ', '.join(state.get("graph_context",[]))
    issues_info = ', '.join(state.get("detected_issues",[]))

    prompt = f"""
    设备异常现象：{issues_info}
    历史相似维修案例：\n{vector_info}
    知识图谱推测的根因：{graph_info}
    
    请结合以上信息，推断该设备最核心的故障根因，并按可能性排序（最多3个）。
    请直接输出根因名称，用逗号分隔，不要输出其他废话。
    """

    response = llm.invoke([
        SystemMessage(content='你是资深设备诊断专家。'),
        HumanMessage(content=prompt)
    ])

    # 简单解析结果
    causes = [c.strip() for c in response.content.split(',') if c.strip()]

    return {'root_causes':causes}