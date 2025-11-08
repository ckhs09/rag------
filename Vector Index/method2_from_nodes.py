"""
方法2: 使用 Node 列表构造向量存储索引对象
"""

# 导入必要的模块
from llama_index.core import VectorStoreIndex, Document

def create_index_from_nodes():
    """
    使用 Node 列表构造向量存储索引对象
    这种方法适用于已经有处理好的Node对象列表的情况
    """
    print("=== 方法2: 使用 Node 列表构造 ===")
    
    # 创建一些示例节点 (这里用Document模拟Node)
    # 在实际应用中，这些可能是经过特定处理的Node对象
    nodes = [
        Document(text="LlamaIndex是一个强大的数据框架，用于连接自定义数据源与大型语言模型。"),
        Document(text="向量存储索引是LlamaIndex中最常用的索引类型之一。"),
        Document(text="FAISS是Facebook AI开发的一个高效相似性搜索库。"),
        Document(text="通过向量存储索引，我们可以实现语义级别的文档检索。"),
        Document(text="Node对象是LlamaIndex中数据的基本单位，代表源数据的某个块。")
    ]
    
    # 从节点列表直接创建索引
    # 这种方法会跳过文档加载和节点解析步骤，直接使用提供的Node对象
    index = VectorStoreIndex(nodes)
    
    print("成功通过Node列表创建索引")
    print("这种方法适用于已经有预处理好的Node对象列表的情况")
    return index

if __name__ == "__main__":
    index = create_index_from_nodes()
    print(f"创建的索引对象: {index}")