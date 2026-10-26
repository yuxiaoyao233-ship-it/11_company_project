# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      workflow.py
# Author:       wyh
# ---------------------------------------------------------------------------
# *********编排工作流*********
# 把节点串成一张图
# 导包
from langgraph.graph import StateGraph,END
from graph.state import DiagnosisState

# 导入所有节点函数
from agents.preprocess_agent import preprocess_node
from agents.detect_agent import detect_node
from agents.root_cause_agent import root_cause_node
from agents.solution_agent import solution_node

def build_workflow():
    """构建多智能体工作流"""
    workflow = StateGraph(DiagnosisState)

    # 1. 添加节点
    workflow.add_node('preprocess',preprocess_node)
    workflow.add_node('detect',detect_node)
    workflow.add_node('root_cause',root_cause_node)
    workflow.add_node('solution',solution_node)

    # 2. 设置起点
    workflow.set_entry_point('preprocess')

    # 3. 定义普通边（线性流转）
    workflow.add_edge('preprocess','detect')
    workflow.add_edge('detect','root_cause')
    workflow.add_edge('root_cause','solution')
    workflow.add_edge('solution',END)

    # 4. 编译图
    app = workflow.compile()
    return app

if __name__ == '__main__':
    # 打印工作流ASCII字符画
    app = build_workflow()
    # print(app.get_graph().draw_ascii())
    # 生成工作流PNG图片
    app.get_graph().draw_mermaid_png(output_file_path='./workflow.png')