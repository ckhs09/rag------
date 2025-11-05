#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RAG应用核心模块
实现文档向量化、存储和检索功能
"""

import os
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA


class RAGApplication:
    """
    RAG应用类，封装了文档处理、向量化、检索和问答功能
    """
    
    def __init__(self, openai_api_key=None):
        """
        初始化RAG应用
        
        Args:
            openai_api_key (str, optional): OpenAI API密钥
        """
        # 设置OpenAI API密钥
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
            
        # 初始化嵌入模型
        self.embeddings = OpenAIEmbeddings()
        
        # 初始化向量存储
        self.vector_store = None
        
        # 初始化语言模型
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-instruct")
    
    def create_vector_store(self, documents):
        """
        创建向量存储
        
        Args:
            documents (list): 文档对象列表
            
        Returns:
            FAISS: 向量存储对象
        """
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        return self.vector_store
    
    def search_documents(self, query, k=4):
        """
        搜索与查询相关的文档
        
        Args:
            query (str): 查询字符串
            k (int): 返回的文档数量
            
        Returns:
            list: 相关文档列表
        """
        if not self.vector_store:
            raise ValueError("向量存储未初始化，请先调用create_vector_store方法")
            
        retriever = self.vector_store.as_retriever(search_kwargs={"k": k})
        return retriever.get_relevant_documents(query)
    
    def answer_question(self, query):
        """
        基于检索到的文档回答问题
        
        Args:
            query (str): 用户问题
            
        Returns:
            str: 回答结果
        """
        if not self.vector_store:
            raise ValueError("向量存储未初始化，请先调用create_vector_store方法")
            
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever()
        )
        
        return qa_chain.invoke(query)["result"]