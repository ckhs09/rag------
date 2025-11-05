#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
交互式查询模块
实现基于向量检索和大模型生成的问答功能
"""

import ollama
import chromadb
from typing import List, Dict, Any


def getconfig() -> Dict[str, str]:
    """
    获取配置信息
    
    Returns:
        Dict[str, str]: 包含嵌入模型和大模型配置的字典
    """
    return {
        "embedmodel": "nomic-embed-text",
        "llmmodel": "llama3"
    }


def query_vector_database(query: str, collection, embedmodel: str, top_k: int = 4) -> List[Dict[str, Any]]:
    """
    使用查询向量在向量数据库中检索相关文档
    
    Args:
        query: 用户查询问题
        collection: ChromaDB集合
        embedmodel: 嵌入模型名称
        top_k: 返回结果数量
        
    Returns:
        List[Dict[str, Any]]: 检索到的相关文档列表
    """
    # 生成查询向量
    embedding = ollama.embeddings(model=embedmodel, prompt=query)
    query_vector = embedding["embedding"]
    
    # 在向量数据库中检索
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )
    
    return results


def generate_answer(query: str, docs: List[str], llmmodel: str) -> str:
    """
    使用大模型生成答案
    
    Args:
        query: 用户查询问题
        docs: 检索到的相关文档
        llmmodel: 大模型名称
        
    Returns:
        str: 生成的答案
    """
    # 组装Prompt
    context = "\n\n".join(docs)
    prompt = f"""使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答案。
    {context}
    
    问题: {query}
    有用的回答:"""
    
    # 调用大模型生成答案
    response = ollama.generate(
        model=llmmodel,
        prompt=prompt,
        stream=False,
        options={
            "temperature": 0.7
        }
    )
    
    return response["response"]


def interactive_query():
    """
    交互式查询主函数
    """
    # 获取配置
    config = getconfig()
    embedmodel = config["embedmodel"]
    llmmodel = config["llmmodel"]
    
    # 连接向量数据库
    try:
        chroma = chromadb.HttpClient(host="localhost", port=8000)
        collection = chroma.get_or_create_collection("ragdb")
        print("成功连接到向量数据库")
    except Exception as e:
        print(f"连接向量数据库失败: {e}")
        return
    
    print("交互式问答系统已启动，输入 'quit' 或 'exit' 退出")
    print("-" * 50)
    
    while True:
        try:
            # 获取用户输入
            query = input("\nEnter your query: ").strip()
            
            # 检查退出条件
            if query.lower() in ['quit', 'exit', '']:
                print("退出问答系统")
                break
            
            if not query:
                continue
                
            print("正在检索相关文档...")
            
            # 检索相关文档
            results = query_vector_database(query, collection, embedmodel)
            
            # 提取文档内容
            docs = []
            if results and 'documents' in results and results['documents']:
                docs = results['documents'][0]  # 获取第一个查询的结果
            
            if not docs:
                print("未找到相关文档")
                continue
                
            print(f"找到 {len(docs)} 个相关文档，正在生成答案...")
            
            # 生成答案
            answer = generate_answer(query, docs, llmmodel)
            print(f"\n答案: {answer}")
            
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            print(f"处理查询时出错: {e}")


if __name__ == "__main__":
    interactive_query()