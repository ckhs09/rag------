from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
import os

def load_local_documents(directory_path):
    """
    加载本地文档数据
    支持TXT、PDF、DOC、DOCX等格式
    """
    # 使用SimpleDirectoryReader加载指定目录下的所有文档
    reader = SimpleDirectoryReader(
        input_dir=directory_path,
        required_exts=[".txt", ".pdf", ".doc", ".docx", ".md"],
        recursive=True
    )
    
    documents = reader.load_data()
    print(f"成功加载 {len(documents)} 个文档")
    
    # 使用SentenceSplitter进行文本分割
    splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
    nodes = splitter.get_nodes_from_documents(documents)
    
    return nodes

if __name__ == "__main__":
    # 示例用法
    directory_path = "./data/documents"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"请在 {directory_path} 目录下放置您的文档文件")
    
    nodes = load_local_documents(directory_path)
    print(f"文档已分割为 {len(nodes)} 个节点")