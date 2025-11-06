from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
import requests
from urllib.parse import urlparse
import os

def load_cloud_documents(file_urls, download_dir="./data/downloads"):
    """
    从云存储下载并加载文档
    支持常见的云存储链接（Google Drive, Dropbox, OneDrive等直接下载链接）
    """
    # 创建下载目录
    os.makedirs(download_dir, exist_ok=True)
    
    downloaded_files = []
    
    # 下载文件
    for url in file_urls:
        try:
            print(f"正在下载: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # 从URL获取文件名
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path) or f"file_{len(downloaded_files)}.txt"
            file_path = os.path.join(download_dir, filename)
            
            # 保存文件
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            downloaded_files.append(file_path)
            print(f"已保存至: {file_path}")
            
        except Exception as e:
            print(f"下载失败 {url}: {e}")
    
    if not downloaded_files:
        print("没有成功下载任何文件")
        return []
    
    # 使用SimpleDirectoryReader加载下载的文件
    from llama_index.core import SimpleDirectoryReader
    
    reader = SimpleDirectoryReader(
        input_files=downloaded_files,
        filename_as_id=True
    )
    
    documents = reader.load_data()
    print(f"成功加载 {len(documents)} 个云存储文档")
    
    # 分割文档
    splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
    nodes = splitter.get_nodes_from_documents(documents)
    
    return nodes

if __name__ == "__main__":
    # 示例云存储文件链接（需要替换为实际可访问的直链）
    example_urls = [
        "https://httpbin.org/json",  # 示例JSON数据
    ]
    
    print("正在从云存储加载文档...")
    nodes = load_cloud_documents(example_urls)
    
    if nodes:
        print(f"云存储文档已分割为 {len(nodes)} 个节点")