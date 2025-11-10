"""
BM25 Retriever（BM25检索器）示例脚本
功能：
1. 基于Elasticsearch的词汇搜索
2. 适合关键词丰富的查询
"""

import math
from collections import Counter
import re


class BM25Retriever:
    def __init__(self, documents=None, k1=1.5, b=0.75):
        """
        初始化BM25检索器
        :param documents: 文档集合
        :param k1: 饱和参数，控制词频饱和度
        :param b: 长度归一化参数
        """
        self.documents = documents or []
        self.k1 = k1
        self.b = b
        self.avgdl = 0  # 平均文档长度
        self.idf = {}   # 逆文档频率
        self.doc_freqs = []  # 文档频率
        self.initialize()
    
    def initialize(self):
        """初始化参数"""
        # 计算平均文档长度
        total_length = sum(len(doc.get('content', '').split()) for doc in self.documents)
        self.avgdl = total_length / len(self.documents) if self.documents else 0
        
        # 计算文档频率
        df = {}
        for doc in self.documents:
            content = doc.get('content', '')
            words = set(content.split())
            for word in words:
                df[word] = df.get(word, 0) + 1
        
        # 计算IDF值
        N = len(self.documents)
        for word, freq in df.items():
            self.idf[word] = math.log((N - freq + 0.5) / (freq + 0.5) + 1)
    
    def bm25_score(self, query, document):
        """
        计算BM25得分
        :param query: 查询字符串
        :param document: 文档
        :return: BM25得分
        """
        content = document.get('content', '')
        words = content.split()
        doc_len = len(words)
        
        # 计算词频
        tf = Counter(words)
        
        # 计算BM25得分
        score = 0.0
        for word in query.split():
            if word in tf:
                idf = self.idf.get(word, 0)
                tf_score = tf[word]
                numerator = tf_score * (self.k1 + 1)
                denominator = tf_score + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
                score += idf * numerator / denominator
        
        return score
    
    def search(self, query, top_k=10):
        """
        执行BM25检索
        :param query: 查询字符串
        :param top_k: 返回结果数量
        :return: 检索结果列表
        """
        results = []
        
        for doc in self.documents:
            score = self.bm25_score(query, doc)
            if score > 0:
                results.append({
                    'document': doc,
                    'score': score
                })
        
        # 按得分排序并返回前top_k个结果
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]


# 示例使用
if __name__ == "__main__":
    # 模拟文档数据
    sample_documents = [
        {
            "id": 1,
            "title": "Machine Learning Algorithms",
            "content": "Machine learning algorithms are used in data science and artificial intelligence applications"
        },
        {
            "id": 2,
            "title": "Deep Learning Networks",
            "content": "Deep learning neural networks form the backbone of modern artificial intelligence systems"
        },
        {
            "id": 3,
            "title": "Natural Language Processing",
            "content": "Natural language processing combines computational linguistics with machine learning algorithms"
        },
        {
            "id": 4,
            "title": "Computer Vision",
            "content": "Computer vision systems use deep learning to interpret and understand visual information"
        }
    ]
    
    # 创建BM25检索器实例
    retriever = BM25Retriever(sample_documents)
    
    # 执行检索
    query = "machine learning algorithms"
    results = retriever.search(query, top_k=3)
    
    print(f"Query: {query}")
    print("BM25 Retrieval Results:")
    for i, result in enumerate(results, 1):
        doc = result['document']
        print(f"{i}. {doc['title']} (Score: {result['score']:.4f})")
        print(f"   {doc['content']}")