#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RAG应用主程序入口
整合各个模块并提供运行接口
"""

import sys
import os

# 添加src目录到Python路径中
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.document_loader import load_document, split_document
from src.rag_app import RAGApplication


def main():
    """
    主函数，演示RAG应用的基本流程
    """
    print("请选择运行模式:")
    print("1. 文档处理和向量存储")
    print("2. 交互式问答")
    choice = input("请输入选择 (1 或 2): ").strip()
    
    if choice == "1":
        # 指定文档路径
        file_path = "data/sample.txt"
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"错误: 文件 {file_path} 不存在")
            return
        
        # 创建输出目录
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"创建输出目录: {output_dir}")
        
        # 创建子目录用于存放生成的文件
        sub_dir = os.path.join(output_dir, "generated_files")
        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)
            print(f"创建生成文件子目录: {sub_dir}")
        
        print("1. 加载文档...")
        documents = load_document(file_path)
        print(f"   成功加载文档")
        
        print("2. 分割文档...")
        texts = split_document(documents, chunk_size=500, chunk_overlap=100)
        print(f"   文档分割为 {len(texts)} 个文本块")
        
        print("3. 初始化RAG应用...")
        # 注意：这里需要设置你的OpenAI API密钥
        rag_app = RAGApplication()
        
        print("4. 创建向量存储...")
        vector_store = rag_app.create_vector_store(texts)
        print("   向量存储创建成功")
        
        # 保存向量存储到子目录
        vector_store.save_local(sub_dir, "faiss_index")
        print(f"   向量存储已保存到 {sub_dir}")
        
        print("5. 测试问答功能...")
        # 示例问题
        query = "什么是人工智能？"
        print(f"   查询: {query}")
        
        # 检索相关文档
        relevant_docs = rag_app.search_documents(query, k=3)
        print(f"   找到 {len(relevant_docs)} 个相关文档")
        
        # 生成答案
        answer = rag_app.answer_question(query)
        print(f"   回答: {answer}")
        
        # 将答案保存到子目录中的文件
        answer_file = os.path.join(sub_dir, "answer.txt")
        with open(answer_file, "w", encoding="utf-8") as f:
            f.write(f"问题: {query}\n")
            f.write(f"答案: {answer}\n")
        print(f"   答案已保存到 {answer_file}")
        
        print("\nRAG应用演示完成!")
        
    elif choice == "2":
        try:
            from src.interactive_query import interactive_query
            interactive_query()
        except ImportError as e:
            print(f"导入交互式查询模块失败: {e}")
            print("请确保已安装所需的依赖包")
    else:
        print("无效选择")


if __name__ == "__main__":
    main()