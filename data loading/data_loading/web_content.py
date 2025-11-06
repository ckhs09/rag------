from llama_index.core import VectorStoreIndex
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.node_parser import SentenceSplitter
from urllib.parse import urlparse

def load_web_pages(urls):
    """
    从网页URL加载内容
    """
    # 验证URL格式
    valid_urls = []
    for url in urls:
        try:
            result = urlparse(url)
            if all([result.scheme, result.netloc]):
                valid_urls.append(url)
            else:
                print(f"无效的URL格式: {url}")
        except Exception as e:
            print(f"URL解析错误 {url}: {e}")
    
    if not valid_urls:
        print("没有有效的URL可加载")
        return []
    
    # 使用SimpleWebPageReader加载网页内容
    reader = SimpleWebPageReader()
    documents = reader.load_data(valid_urls)
    print(f"成功加载 {len(documents)} 个网页")
    
    # 分割内容
    splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=50)
    nodes = splitter.get_nodes_from_documents(documents)
    
    return nodes

if __name__ == "__main__":
    # 示例网页URL列表
    example_urls = [
        "https://example.com",
        "https://httpbin.org/html"
    ]
    
    print("正在加载网页内容...")
    nodes = load_web_pages(example_urls)
    
    if nodes:
        print(f"网页内容已分割为 {len(nodes)} 个节点")
        for i, node in enumerate(nodes[:3]):  # 显示前3个节点
            print(f"\n节点 {i+1}:")
            print(node.text[:200] + "..." if len(node.text) > 200 else node.text)