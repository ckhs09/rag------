"""
Vector Retriever（向量检索器）示例脚本
功能：
1. 密集型检索，基于向量相似度
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class VectorRetriever:
    def __init__(self, documents=None):
        """
        初始化向量检索器
        :param documents: 文档集合
        """
        self.documents = documents or []
        self.vectorizer = TfidfVectorizer()
        self.document_vectors = None
        self.fit()
    
    def fit(self):
        """训练向量化模型并转换文档"""
        if self.documents:
            contents = [doc.get('content', '') for doc in self.documents]
            self.document_vectors = self.vectorizer.fit_transform(contents)
    
    def search(self, query, top_k=10):
        """
        执行向量检索
        :param query: 查询字符串
        :param top_k: 返回结果数量
        :return: 检索结果列表
        """
        if not self.document_vectors:
            return []
        
        # 将查询转换为向量
        query_vector = self.vectorizer.transform([query])
        
        # 计算余弦相似度
        similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
        
        # 获取前top_k个结果
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for i in top_indices:
            if similarities[i] > 0:  # 只返回相似度大于0的结果
                results.append({
                    'document': self.documents[i],
                    'score': similarities[i]
                })
        
        return results


# 示例使用
if __name__ == "__main__":
    # 模拟文档数据
    sample_documents = [
        {
            "id": 1,
            "title": "Introduction to Machine Learning",
            "content": "Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data."
        },
        {
            "id": 2,
            "title": "Deep Learning Fundamentals",
            "content": "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Learning can be supervised, semi-supervised or unsupervised."
        },
        {
            "id": 3,
            "title": "Natural Language Processing",
            "content": "Natural language processing is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language."
        },
        {
            "id": 4,
            "title": "Computer Vision Overview",
            "content": "Computer vision is an interdisciplinary scientific field that deals with how computers can gain high-level understanding from digital images or videos."
        }
    ]
    
    # 创建向量检索器实例
    retriever = VectorRetriever(sample_documents)
    
    # 执行检索
    query = "artificial intelligence and machine learning systems"
    results = retriever.search(query, top_k=3)
    
    print(f"Query: {query}")
    print("Vector Retrieval Results:")
    for i, result in enumerate(results, 1):
        doc = result['document']
        print(f"{i}. {doc['title']} (Similarity: {result['score']:.4f})")
        print(f"   {doc['content'][:100]}...")