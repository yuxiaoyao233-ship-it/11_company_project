# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      main.py
# Author:       wyh
# ---------------------------------------------------------------------------
# 导包
from agents.preprocess_agent import preprocess_fault_description
from graph.workflow import build_workflow
from knowledge_base.knowledge_graph import search_graph_by_phenomenon
from knowledge_base.vector_store import search_similar_cases

def test_preprocess_agent():
    # 模拟车间工人发来的一段口语化报修信息
    raw_fault = """
    3号水泵最近一周运行声音异常，嗡嗡响，有明显振动，
    出口压力表一直跳，不稳定，用手摸轴承附近感觉烫手，
    操作工怀疑是联轴器对中没有对齐，但还没找机修工检查。
    """

    print("=== 车间工人原始上报 ===")
    print(raw_fault)

    print("\n=== 智能体正在分析（本地3B模型，可能需要几秒钟） ===")

    try:
        res = preprocess_fault_description(raw_fault)

        print("\n=== 预处理智能体结构化输出 ===")
        # 格式化输出JSON
        print(res.model_dump_json(indent=2,ensure_ascii=False))

    except Exception as e:
        print(f'\n❌ 发生错误：{e}')

def test_knowledge_base():
    print("=== 测试1：向量库检索（找历史相似案例） ===")
    query = '水泵振动大，轴承温度高'
    print(f'检索词：{query}')
    cases = search_similar_cases(query,k=1)
    for i, case in enumerate(cases):
        print(f'命中案例 {i+1}:\n{case}\n')

    print("=== 测试 2：图数据库检索（找根因） ===")
    # 假设我们从预处理结果中拿到了这些现象
    phenomena = ['振动大','轴承发热']
    print(f'输入现象：{phenomena}')
    causes = search_graph_by_phenomenon(phenomena)
    print(f'图谱推理出的可能根因：{causes}')

# 将故障输入做一次全流程诊断
def diagnose_test():
    raw_fault = """
    3号水泵最近一周运行声音异常，嗡嗡响，有明显振动，
    出口压力表一直跳，不稳定，用手摸轴承附近感觉烫手，
    操作工怀疑是联轴器中没有对齐，但还没找机修工检查。
    """

    print("================================")
    print("🚀 启动多Agent故障诊断流水线")
    print("================================")
    print("原始输入：",raw_fault)

    # 构建工作流
    app = build_workflow()

    # 初始化状态
    initial_state = {
        'raw_input': raw_fault,
        'retry_count': 0
    }

    # 运行（注意：LangGraph执行时会自动在节点间传递并更新State）
    result = app.invoke(initial_state)

    print('\n==================================')
    print('📊 最终诊断报告')
    print('\n==================================')
    print(f'【设备类型】：{result["preprocess_result"].device_type}')
    print(f'【严重程度】：{result["preprocess_result"].severity}')
    print(f'【根因分析】：{", ".join(result["root_causes"])}')
    print(f'\n【维修方案】：\n{result["solution"]}')


if __name__ == '__main__':
    # 测试数据预处理智能体
    # test_preprocess_agent()
    # 测试向量数据库
    # test_knowledge_base()
    # 全流程诊断
    diagnose_test()