"""
Text Similarity Reranker（文本相似度重排检索器）示例脚本
功能：
1. 使用机器学习模型根据语义相似性对文档重新排名
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TextSimilarityReranker:
    def __init__(self, base_retriever=None):
        """
        初始化文本相似度重排器
        :param base_retriever: 基础检索器
        """
        self.base_retriever = base_retriever
        self.vectorizer = TfidfVectorizer()
    
    def rerank(self, query, documents):
        """
        根据文本相似度重新排序文档
        :param query: 查询字符串
        :param documents: 待重排的文档列表
        :return: 重排后的文档列表
        """
        if not documents:
            return []
        
        # 提取文档内容
        doc_contents = [doc.get('content', '') for doc in documents]
        
        # 向量化查询和文档
        try:
            all_texts = [query] + doc_contents
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            
            # 计算查询与文档之间的相似度
            query_vector = tfidf_matrix[0]
            doc_vectors = tfidf_matrix[1:]
            similarities = cosine_similarity(query_vector, doc_vectors).flatten()
            
            # 结合原始得分和相似度得分
            reranked_docs = []
            for i, doc in enumerate(documents):
                original_score = doc.get('score', 0)
                similarity_score = similarities[i]
                
                # 组合得分（这里简单加权平均）
                combined_score = 0.3 * original_score + 0.7 * similarity_score
                
                reranked_docs.append({
                    'document': doc,
                    'score': combined_score,
                    'original_score': original_score,
                    'similarity_score': similarity_score
                })
            
            # 按组合得分排序
            reranked_docs.sort(key=lambda x: x['score'], reverse=True)
            return reranked_docs
            
        except Exception as e:
            print(f"Reranking error: {e}")
            return [{'document': doc, 'score': doc.get('score', 0)} for doc in documents]
    
    def search(self, query, top_k=10):
        """
        执行带重排的检索
        :param query: 查询字符串
        :param top_k: 返回结果数量
        :return: 重排后的检索结果列表
        """
        # 使用基础检索器获取初始结果
        if self.base_retriever:
            initial_results = self.base_retriever.search(query, top_k * 2)  # 获取更多候选结果
        else:
            # 如果没有基础检索器，则创建一个简单的模拟检索器
            initial_results = self._mock_search(query, top_k * 2)
        
        # 提取文档
        documents = [result['document'] for result in initial_results]
        
        # 重排结果
        reranked_results = self.rerank(query, documents)
        
        # 返回前top_k个结果
        return reranked_results[:top_k]
    
    def _mock_search(self, query, top_k):
        """
        模拟基础检索器
        """
        # 这里只是一个示例，实际应用中应该有一个真正的基础检索器
        mock_docs = [
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
            }
        ]
        
        # 模拟评分
        results = []
        for doc in mock_docs:
            # 简单的关键词匹配评分
            content = doc['content'].lower()
            score = sum(content.count(word) for word in query.lower().split())
            if score > 0:
                results.append({
                    'document': doc,
                    'score': score
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]


# 示例使用
if __name__ == "__main__":
    # 创建文本相似度重排器实例
    reranker = TextSimilarityReranker()
    
    # 执行检索和重排
    query = "artificial intelligence machine learning algorithms"
    results = reranker.search(query, top_k=3)
    
    print(f"Query: {query}")
    print("Text Similarity Reranker Results:")
    for i, result in enumerate(results, 1):
        doc = result['document']
        print(f"{i}. {doc['title']}")
        print(f"   Combined Score: {result['score']:.4f} "
              f"(Original: {result.get('original_score', 0):.4f}, "
              f"Similarity: {result.get('similarity_score', 0):.4f})")
        print(f"   {doc['content'][:100]}...")