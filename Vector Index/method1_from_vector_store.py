"""
方法1: 通过 from_vector_store 方法构造向量存储索引对象
"""

# 导入必要的模块
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.faiss import FaissVectorStore
import faiss

def create_index_from_vector_store():
    """
    使用 from_vector_store 方法创建向量存储索引对象
    这种方法适用于已有向量存储的情况
    """
    print("=== 方法1: 使用 from_vector_store 方法 ===")
    
    # 创建一个FAISS向量存储
    # 假设使用OpenAI的嵌入维度 (1536) 或其他嵌入模型的维度
    dimension = 1536  
    faiss_index = faiss.IndexFlatL2(dimension)
    vector_store = FaissVectorStore(faiss_index=faiss_index)
    
    # 从现有的向量存储创建索引
    # 这种方法适合已经有存储了Node向量的向量库的情况
    index = VectorStoreIndex.from_vector_store(vector_store)
    
    print("成功通过 from_vector_store 方法创建索引")
    print("这种方法适用于重用已有的向量存储数据")
    return index

if __name__ == "__main__":
    index = create_index_from_vector_store()
    print(f"创建的索引对象: {index}")