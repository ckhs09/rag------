"""
方法3: 使用文档直接构造向量存储索引对象
"""

# 导入必要的模块
from llama_index.core import Document, VectorStoreIndex

def create_index_from_documents():
    """
    使用文档直接构造向量存储索引对象
    这是最常见的方法，适用于从原始文档开始构建索引的情况
    """
    print("=== 方法3: 使用文档直接构造 ===")
    
    # 创建一些示例文档
    # 这些文档可以来自任何来源：文件、数据库、网页抓取等
    documents = [
        Document(text="LlamaIndex（以前称为GPT Index）是一个用于LlamaHub和自定义数据的简单而灵活的接口。"),
        Document(text="VectorStoreIndex是最常用的索引模式，它将所有文档节点存储在向量存储中。"),
        Document(text="可以使用多种向量存储后端，如Faiss、Pinecone、Weaviate、Chroma等。"),
        Document(text="当查询索引时，它会识别与查询相关的节点，获取它们的嵌入向量，并在向量存储中执行最近邻搜索。"),
        Document(text="LlamaIndex支持多种类型的索引结构，包括向量存储索引、列表索引、树索引等。")
    ]
    
    # 从文档创建索引
    # 这种方法会自动执行以下步骤：
    # 1. 解析文档为Node对象
    # 2. 为Node生成嵌入向量
    # 3. 将Node和向量存储到向量库中
    # 4. 构造向量存储索引对象
    index = VectorStoreIndex.from_documents(documents)
    
    print("成功通过文档直接创建索引")
    print("这种方法会自动完成完整的索引构建流程")
    return index

if __name__ == "__main__":
    index = create_index_from_documents()
    print(f"创建的索引对象: {index}")