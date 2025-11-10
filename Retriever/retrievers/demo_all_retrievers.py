"""
演示所有检索器类型的主程序
"""

from elasticsearch_retriever.standard_retriever import StandardRetriever
from elasticsearch_retriever.bm25_retriever import BM25Retriever
from vector_retriever.vector_retriever import VectorRetriever
from vector_retriever.knn_retriever import KNNRetriever
from hybrid_retriever.rrf_retriever import RRF_Retriever
from hybrid_retriever.text_similarity_reranker import TextSimilarityReranker


def create_sample_documents():
    """创建示例文档"""
    return [
        {
            "id": 1,
            "title": "Introduction to Machine Learning",
            "content": "Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention."
        },
        {
            "id": 2,
            "title": "Deep Learning Neural Networks",
            "content": "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Learning can be supervised, semi-supervised or unsupervised and reinforcement learning."
        },
        {
            "id": 3,
            "title": "Natural Language Processing",
            "content": "Natural language processing is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data."
        },
        {
            "id": 4,
            "title": "Computer Vision Systems",
            "content": "Computer vision is an interdisciplinary scientific field that deals with how computers can gain high-level understanding from digital images or videos. From the perspective of engineering, it seeks to understand and automate tasks that the human visual system can do."
        },
        {
            "id": 5,
            "title": "Reinforcement Learning Algorithms",
            "content": "Reinforcement learning is an area of machine learning concerned with how intelligent agents ought to take actions in an environment in order to maximize the notion of cumulative reward. Reinforcement learning is one of the three basic machine learning paradigms."
        }
    ]


def demonstrate_standard_retriever(documents, query):
    """演示Standard Retriever"""
    print("=" * 60)
    print("Standard Retriever (标准检索器)")
    print("功能：")
    print("1. 替代传统的query功能")
    print("2. 返回传统查询中的顶级文档")
    print("-" * 60)
    
    retriever = StandardRetriever(documents)
    results = retriever.search(query, top_k=3)
    
    print(f"查询: {query}")
    print("结果:")
    for i, result in enumerate(results, 1):
        doc = result['document']
        print(f"  {i}. {doc['title']} (得分: {result['score']})")
        print(f"     {doc['content'][:80]}...")
    print()


def demonstrate_bm25_retriever(documents, query):
    """演示BM25 Retriever"""
    print("=" * 60)
    print("BM25 Retriever (BM25检索器)")
    print("功能：")
    print("1. 基于Elasticsearch的词汇搜索")
    print("2. 适合关键词丰富的查询")
    print("-" * 60)
    
    retriever = BM25Retriever(documents)
    results = retriever.search(query, top_k=3)
    
    print(f"查询: {query}")
    print("结果:")
    for i, result in enumerate(results, 1):
        doc = result['document']
        print(f"  {i}. {doc['title']} (得分: {result['score']:.4f})")
        print(f"     {doc['content'][:80]}...")
    print()


def demonstrate_vector_retriever(documents, query):
    """演示Vector Retriever"""
    print("=" * 60)
    print("Vector Retriever (向量检索器)")
    print("功能：")
    print("1. 密集型检索，基于向量相似度")
    print("-" * 60)
    
    retriever = VectorRetriever(documents)
    results = retriever.search(query, top_k=3)
    
    print(f"查询: {query}")
    print("结果:")
    for i, result in enumerate(results, 1):
        doc = result['document']
        print(f"  {i}. {doc['title']} (相似度: {result['score']:.4f})")
        print(f"     {doc['content'][:80]}...")
    print()


def demonstrate_knn_retriever(documents, query):
    """演示KNN Retriever"""
    print("=" * 60)
    print("KNN Retriever (K近邻检索器)")
    print("功能：")
    print("1. 替代knn搜索功能")
    print("2. 返回kNN搜索中的顶级文档")
    print("-" * 60)
    
    retriever = KNNRetriever(documents, n_neighbors=3)
    results = retriever.search(query, top_k=3)
    
    print(f"查询: {query}")
    print("结果:")
    for i, result in enumerate(results, 1):
        doc = result['document']
        print(f"  {i}. {doc['title']} (相似度: {result['score']:.4f}, 距离: {result['distance']:.4f})")
        print(f"     {doc['content'][:80]}...")
    print()


def demonstrate_rrf_retriever(documents, query):
    """演示RRF Retriever"""
    print("=" * 60)
    print("RRF Retriever (倒数排名融合检索器)")
    print("功能：")
    print("1. 根据倒数排名融合(RRF)算法生成顶级文档")
    print("2. 可以组合多个第一阶段检索器")
    print("-" * 60)
    
    # 创建多个不同的检索器
    standard_retriever = StandardRetriever(documents)
    bm25_retriever = BM25Retriever(documents)
    
    # 创建RRF检索器
    rrf_retriever = RRF_Retriever([standard_retriever, bm25_retriever])
    results = rrf_retriever.search(query, top_k=3)
    
    print(f"查询: {query}")
    print("结果:")
    for i, result in enumerate(results, 1):
        doc = result['document']
        print(f"  {i}. {doc['title']} (RRF得分: {result['score']:.4f})")
        print(f"     {doc['content'][:80]}...")
    print()


def demonstrate_text_similarity_reranker(documents, query):
    """演示Text Similarity Reranker"""
    print("=" * 60)
    print("Text Similarity Reranker (文本相似度重排检索器)")
    print("功能：")
    print("1. 使用机器学习模型根据语义相似性对文档重新排名")
    print("-" * 60)
    
    # 使用BM25作为基础检索器
    base_retriever = BM25Retriever(documents)
    reranker = TextSimilarityReranker(base_retriever)
    results = reranker.search(query, top_k=3)
    
    print(f"查询: {query}")
    print("结果:")
    for i, result in enumerate(results, 1):
        doc = result['document']
        print(f"  {i}. {doc['title']}")
        print(f"     组合得分: {result['score']:.4f} "
              f"(原始得分: {result.get('original_score', 0):.4f}, "
              f"相似度得分: {result.get('similarity_score', 0):.4f})")
        print(f"     {doc['content'][:80]}...")
    print()


def main():
    """主函数"""
    # 创建示例文档
    documents = create_sample_documents()
    
    # 查询语句
    query = "machine learning artificial intelligence algorithms"
    
    print("检索器类型演示程序")
    print("所有检索器都使用相同的文档集和查询语句")
    print()
    
    # 演示各种检索器
    demonstrate_standard_retriever(documents, query)
    demonstrate_bm25_retriever(documents, query)
    demonstrate_vector_retriever(documents, query)
    demonstrate_knn_retriever(documents, query)
    demonstrate_rrf_retriever(documents, query)
    demonstrate_text_similarity_reranker(documents, query)
    
    print("=" * 60)
    print("演示结束")


if __name__ == "__main__":
    main()