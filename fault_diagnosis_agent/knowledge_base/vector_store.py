# -*-coding:utf-8 -*- #
# ---------------------------------------------------------------------------
# ProjectName:   11_company_project
# FileName:      vector_store.py
# Author:       wyh
# ---------------------------------------------------------------------------
# 实现历史案例的加载和相似度检索
# 导包
import os.path
from config import CHROMA_DB_DIR, CASES_DIR
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from models.embedding import get_embedding

def init_vector_store():
    """
    初始化向量库。如果本地没有数据，则读取data/cases下的文本并存入
    """
    embedding = get_embedding()

    # 如果已经建过库，直接加载
    if os.path.exists(str(CHROMA_DB_DIR)):
        return Chroma(persist_directory=str(CHROMA_DB_DIR),embedding_function=embedding)

    # 否则，加载本地数据
    print('正在初始化向量数据库，加载历史维修档案...')
    loader = DirectoryLoader(str(CASES_DIR),glob='**/*.txt',loader_cls=TextLoader,loader_kwargs={'encoding':'utf-8'})
    docs = loader.load()

    # 切分文档（这里简单处理，直接存入）
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=str(CHROMA_DB_DIR)
    )
    print('向量数据库初始化完成！')
    return vectorstore

def search_similar_cases(query: str, k: int = 2):
    """
    根据查询词检索相似的历史案例
    """
    vectorstore = init_vector_store()
    # 相似度检索，返回前 k 个结果
    results = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in results]
