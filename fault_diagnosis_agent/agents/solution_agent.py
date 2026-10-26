# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      solution_agent.py
# Author:       wyh
# ---------------------------------------------------------------------------
# 维修方案生成智能体，基于根因和历史案例，给出最终方案
# 导包
from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import DiagnosisState
from models.llm import get_llm


def solution_node(state: DiagnosisState):
    """LangGraph 节点：生成维修方案"""
    print('\n--- [节点4] 维修方案生成智能体运行中 ---')
    llm = get_llm()

    causes = ', '.join(state.get('root_causes',[]))
    vector_info = '\n'.join(state.get('vector_context',[]))

    prompt = f"""
    已确认的故障根因：{causes}
    历史维修案例参考：\n{vector_info}
    
    请生成一份给车间工人的标准维修方案，包含：
    1. 维修步骤
    2. 需要准备的备件
    3. 安全注意事项
    要求：条理清晰，语言简练，符合工业现场作业规范。
    """

    response = llm.invoke([
        SystemMessage(content='你是高级维修工程师。'),
        HumanMessage(content=prompt)
    ])

    return {'solution': response.content}