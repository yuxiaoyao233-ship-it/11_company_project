# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      detect_agent.py
# Author:       wyh
# ---------------------------------------------------------------------------
# 异常识别智能体，负责从预处理结果中提取异常特征，并去知识库检索
# 导包
from graph.state import DiagnosisState
from knowledge_base.knowledge_graph import search_graph_by_phenomenon
from knowledge_base.vector_store import search_similar_cases
from models.schemas import PreprocessResult


def detect_node(state: DiagnosisState):
    """LangGraph节点：异常识别与双引擎召回"""
    print("\n--- [节点2：异常识别与知识库召回运行中 ---]")
    pre: PreprocessResult = state['preprocess_result']

    # 1. 提取现象与关键词
    issues = [pre.fault_phenomenon] + pre.possible_causes
    keywords_str = "， ".join(pre.keywords)

    # 2. 查向量库（历史案例）
    vector_context = search_similar_cases(keywords_str,k=1)

    # 3. 查图数据库（利用现象去查根因）
    # 简单处理，直接拿文本去匹配图谱节点（实际业务做NER实体抽取）
    graph_causes = search_graph_by_phenomenon(['振动大','轴承发热']) # 模拟匹配
    if not graph_causes:
        graph_causes = search_graph_by_phenomenon(pre.keywords)

    return {
        'detected_issues' : issues,
        'vector_context': vector_context,
        'graph_context': graph_causes
    }