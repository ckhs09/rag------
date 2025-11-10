"""
KNN Retriever（K近邻检索器）示例脚本
功能：
1. 替代knn搜索功能
2. 返回kNN搜索中的顶级文档
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


class KNNRetriever:
    def __init__(self, documents=None, n_neighbors=5):
        """
        初始化KNN检索器
        :param documents: 文档集合
        :param n_neighbors: 邻居数量
        """
        self.documents = documents or []
        self.n_neighbors = min(n_neighbors, len(documents)) if documents else n_neighbors
        self.vectorizer = TfidfVectorizer()
        self.nn_model = NearestNeighbors(n_neighbors=self.n_neighbors, metric='cosine')
        self.document_vectors = None
        self.fit()
    
    def fit(self):
        """训练向量化模型和最近邻模型"""
        if self.documents:
            contents = [doc.get('content', '') for doc in self.documents]
            self.document_vectors = self.vectorizer.fit_transform(contents)
            self.nn_model.fit(self.document_vectors)
    
    def search(self, query, top_k=None):
        """
        执行KNN检索
        :param query: 查询字符串
        :param top_k: 返回结果数量（默认使用n_neighbors）
        :return: 检索结果列表
        """
        if not self.document_vectors:
            return []
        
        if top_k is None:
            top_k = self.n_neighbors
        
        top_k = min(top_k, self.n_neighbors)
        
        # 将查询转换为向量
        query_vector = self.vectorizer.transform([query])
        
        # 查找最近邻
        distances, indices = self.nn_model.kneighbors(query_vector, n_neighbors=top_k)
        
        results = []
        for i, (distance, index) in enumerate(zip(distances[0], indices[0])):
            # 转换距离为相似度分数（距离越小相似度越高）
            similarity = 1 - distance
            results.append({
                'document': self.documents[index],
                'score': similarity,
                'distance': distance
            })
        
        # 按相似度排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results


# 示例使用
if __name__ == "__main__":
    # 模拟文档数据
    sample_documents = [
        {
            "id": 1,
            "title": "Machine Learning Basics",
            "content": "Machine learning is an application of artificial intelligence that provides systems the ability to automatically learn and improve from experience."
        },
        {
            "id": 2,
            "title": "Neural Networks",
            "content": "Neural networks are a series of algorithms that mimic the operations of a human brain to recognize relationships between vast amounts of data."
        },
        {
            "id": 3,
            "title": "Deep Learning Architectures",
            "content": "Deep learning architectures such as deep neural networks, convolutional neural networks, and recurrent neural networks have been applied to fields like computer vision and speech recognition."
        },
        {
            "id": 4,
            "title": "Reinforcement Learning",
            "content": "Reinforcement learning is an area of machine learning concerned with how intelligent agents ought to take actions in an environment in order to maximize the notion of cumulative reward."
        },
        {
            "id": 5,
            "title": "Supervised Learning",
            "content": "Supervised learning is the machine learning task of learning a function that maps an input to an output based on example input-output pairs."
        }
    ]
    
    # 创建KNN检索器实例
    retriever = KNNRetriever(sample_documents, n_neighbors=3)
    
    # 执行检索
    query = "artificial intelligence learning algorithms"
    results = retriever.search(query, top_k=3)
    
    print(f"Query: {query}")
    print("KNN Retrieval Results:")
    for i, result in enumerate(results, 1):
        doc = result['document']
        print(f"{i}. {doc['title']} (Similarity: {result['score']:.4f}, Distance: {result['distance']:.4f})")
        print(f"   {doc['content'][:100]}...")