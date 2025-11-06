from llama_index.core import VectorStoreIndex
from llama_index.core.readers import DatabaseReader
from llama_index.core.node_parser import SentenceSplitter
from sqlalchemy import create_engine, text
import os

def load_database_data(connection_string, query):
    """
    从数据库加载结构化数据
    """
    # 创建DatabaseReader实例
    reader = DatabaseReader(
        engine=create_engine(connection_string)
    )
    
    # 执行查询获取数据
    documents = reader.load_data(query=query)
    print(f"从数据库加载了 {len(documents)} 条记录")
    
    # 分割数据
    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=20)
    nodes = splitter.get_nodes_from_documents(documents)
    
    return nodes

# 示例用法（需要根据实际数据库配置调整）
if __name__ == "__main__":
    # 示例：SQLite数据库
    connection_string = "sqlite:///./data/sample.db"
    
    # 确保数据目录存在
    os.makedirs("./data", exist_ok=True)
    
    # 创建示例数据库和表（仅用于演示）
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        # 这里只是示例，实际使用时应连接到真实数据库
        print("数据库连接字符串:", connection_string)
        print("请确保数据库中存在相应表结构")
        
    # 示例查询
    sample_query = "SELECT id, name, description FROM products LIMIT 10"
    
    try:
        nodes = load_database_data(connection_string, sample_query)
        print(f"数据已分割为 {len(nodes)} 个节点")
    except Exception as e:
        print(f"加载数据库数据时出错: {e}")
        print("请确保正确配置数据库连接参数和查询语句")