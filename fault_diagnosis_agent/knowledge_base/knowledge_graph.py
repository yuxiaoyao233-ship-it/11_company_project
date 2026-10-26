# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      knowledge_graph.py
# Author:       wyh
# ---------------------------------------------------------------------------
# 编写图数据库封装（内存级的NetworkX）
# 3B模型做复杂的图查询比较吃力，直接用Python写死逻辑（模拟Cypher查询），查找“现象”对应的“根因”
# 导包
import json
import os
from pathlib import Path
from config import EQUIPMENT_GRAPH_DIR
import networkx as nx

def init_knowledge_graph():
    """
    读取 JSON 文件，构建 NetworkX 有向图
    """
    G = nx.DiGraph()
    with open(EQUIPMENT_GRAPH_DIR,'r',encoding='utf-8') as f:
        data = json.load(f)
        # print(data)
        # print(data['nodes'])

    for node in data['nodes']:
        G.add_node(node['id'],type=node['type'])

    for edge in data['edges']:
        G.add_edge(edge['source'],edge['target'],relation=edge['relation'])

    return G

def search_graph_by_phenomenon(phenomenon_list: list):
    """
    根据故障现象（如['振动大','轴承发热']），在图谱中寻找可能得根因
    """
    G = init_knowledge_graph()
    possible_causes = set()

    for ph in phenomenon_list:
        # 由于现象可能不完全等于图谱中的节点名（比如输入"轴承发热"，图谱里是"轴承温度高"）
        # 这里我们做简单的匹配
        if G.has_node(ph):
            # 查找该现象指向的后继节点（因为我们的数据是 现象 -> 根因）
            successors = G.successors(ph)
            for cause in successors:
                edge_data = G.get_edge_data(ph, cause)
                # 验证关系是否是导致关系
                if edge_data and "导致" in edge_data["relation"]:
                    possible_causes.add(cause)

    return list(possible_causes)

if __name__ == '__main__':
    # print("当前工作目录是:", os.getcwd())  # 看看你现在到底在哪
    # print("目标文件绝对路径是:", os.path.abspath('./data/graph/equipment_graph.json'))  # 看看程序跑去哪找文件了
    g = init_knowledge_graph()

