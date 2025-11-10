"""
RRF Retriever（倒数排名融合检索器）示例脚本
功能：
1. 根据倒数排名融合(RRF)算法生成顶级文档
2. 可以组合多个第一阶段检索器
"""

import math
from typing import List, Dict, Any


class RRF_Retriever:
    def __init__(self, retrievers: List[Any] = None, k: float = 60.0):
        """
        初始化RRF检索器
        :param retrievers: 检索器列表
        :param k: RRF参数k，默认为60
        """
        self.retrievers = retrievers or []
        self.k = k
    
    def add_retriever(self, retriever):
        """添加检索器"""
        self.retrievers.append(retriever)
    
    def rrf_score(self, rank: int) -> float:
        """
        计算RRF得分
        :param rank: 排名（从1开始）
        :return: RRF得分
        """
        return 1 / (rank + self.k)
    
    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        执行RRF检索
        :param query: 查询字符串
        :param top_k: 返回结果数量
        :return: 融合后的检索结果列表
        """
        # 收集所有检索器的结果
        all_results = []
        for i, retriever in enumerate(self.retrievers):
            results = retriever.search(query, top_k=50)  # 获取较多候选结果
            all_results.append(results)
        
        # 构建文档得分映射
        doc_scores = {}  # {doc_id: [score1, score2, ...]}
        
        for i, results in enumerate(all_results):
            for rank, result in enumerate(results):
                doc = result['document']
                doc_id = doc.get('id', str(hash(doc.get('content', ''))))
                
                if doc_id not in doc_scores:
                    doc_scores[doc_id] = [0.0] * len(self.retrievers)
                
                # 计算RRF得分并分配给对应检索器位置
                rrf_score = self.rrf_score(rank + 1)
                doc_scores[doc_id][i] = rrf_score
        
        # 计算每个文档的总得分
        final_scores = {}
        for doc_id, scores in doc_scores.items():
            final_scores[doc_id] = sum(scores)
        
        # 排序并返回结果
        sorted_docs = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        
        # 构建最终结果
        results = []
        for doc_id, score in sorted_docs[:top_k]:
            # 找到原始文档数据
            for retriever_results in all_results:
                for result in retriever_results:
                    doc = result['document']
                    if doc.get('id', str(hash(doc.get('content', '')))) == doc_id:
                        results.append({
                            'document': doc,
                            'score': score
                        })
                        break
                else:
                    continue
                break
        
        return results[:top_k]


# 示例使用
if __name__ == "__main__":
    # 模拟文档数据
    sample_documents = [
        {
            "id": 1,
            "title": "Introduction to Artificial Intelligence",
            "content": "Artificial intelligence is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals."
        },
        {
            "id": 2,
            "title": "Machine Learning Overview",
            "content": "Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence."
        },
        {
            "id": 3,
            "title": "Deep Learning Techniques",
            "content": "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning."
        },
        {
            "id": 4,
            "title": "Neural Network Architectures",
            "content": "Neural networks are a series of algorithms that mimic the operations of a human brain to recognize relationships between vast amounts of data."
        }
    ]
    
    # 模拟不同的检索器
    class MockRetriever:
        def __init__(self, name, documents):
            self.name = name
            self.documents = documents
        
        def search(self, query, top_k=10):
            # 简单模拟，基于标题匹配返回结果
            results = []
            query_words = set(query.lower().split())
            
            for doc in self.documents:
                title_words = set(doc['title'].lower().split())
                content_words = set(doc['content'].lower().split())
                
                # 计算匹配得分
                title_matches = len(query_words.intersection(title_words))
                content_matches = len(query_words.intersection(content_words))
                score = title_matches * 2 + content_matches
                
                if score > 0:
                    results.append({
                        'document': doc,
                        'score': score
                    })
            
            results.sort(key=lambda x: x['score'], reverse=True)
            return results[:top_k]
    
    # 创建模拟检索器
    retriever1 = MockRetriever("KeywordRetriever", sample_documents)
    retriever2 = MockRetriever("SemanticRetriever", sample_documents)
    
    # 创建RRF检索器
    rrf_retriever = RRF_Retriever([retriever1, retriever2])
    
    # 执行检索
    query = "machine learning artificial intelligence"
    results = rrf_retriever.search(query, top_k=3)
    
    print(f"Query: {query}")
    print("RRF Retrieval Results:")
    for i, result in enumerate(results, 1):
        doc = result['document']
        print(f"{i}. {doc['title']} (RRF Score: {result['score']:.4f})")
        print(f"   {doc['content'][:100]}...")