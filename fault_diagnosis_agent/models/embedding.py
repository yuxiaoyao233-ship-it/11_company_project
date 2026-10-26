# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      embedding.py
# Author:       wyh
# ---------------------------------------------------------------------------
# 把文字转成向量，封装嵌入模型
# 导包
from langchain_ollama import OllamaEmbeddings

def get_embedding():
    """
    封装本地 Ollama 嵌入模型
    """
    return OllamaEmbeddings(
        model='nomic-embed-text',
        base_url='http://localhost:11434'
    )
