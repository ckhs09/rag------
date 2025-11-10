"""
Standard Retriever（标准检索器）示例脚本
功能：
1. 替代传统的query功能
2. 返回传统查询中的顶级文档
"""

class StandardRetriever:
    def __init__(self, index_data=None):
        """
        初始化标准检索器
        :param index_data: 索引数据，模拟Elasticsearch索引
        """
        self.index_data = index_data or []
    
    def search(self, query, top_k=10):
        """
        执行标准检索
        :param query: 查询字符串
        :param top_k: 返回结果数量
        :return: 检索结果列表
        """
        # 模拟基于关键词的检索
        results = []
        query_terms = query.lower().split()
        
        for doc in self.index_data:
            score = 0
            doc_content = (doc.get('title', '') + ' ' + doc.get('content', '')).lower()
            
            # 计算关键词匹配得分
            for term in query_terms:
                score += doc_content.count(term)
            
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
    # 模拟索引数据
    sample_data = [
        {
            "id": 1,
            "title": "Introduction to Machine Learning",
            "content": "Machine learning is a subset of artificial intelligence that focuses on algorithms and statistical models."
        },
        {
            "id": 2,
            "title": "Deep Learning Basics",
            "content": "Deep learning is part of a broader family of machine learning methods based on artificial neural networks."
        },
        {
            "id": 3,
            "title": "Natural Language Processing",
            "content": "Natural language processing is a subfield of linguistics, computer science, and artificial intelligence."
        }
    ]
    
    # 创建检索器实例
    retriever = StandardRetriever(sample_data)
    
    # 执行检索
    query = "machine learning algorithms"
    results = retriever.search(query, top_k=2)
    
    print(f"Query: {query}")
    print("Results:")
    for i, result in enumerate(results, 1):
        doc = result['document']
        print(f"{i}. {doc['title']} (Score: {result['score']})")
        print(f"   {doc['content'][:100]}...")