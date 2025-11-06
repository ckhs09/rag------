from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
import json
import requests

class SocialMediaReader:
    """
    社交媒体数据读取器基类
    """
    def __init__(self):
        pass
    
    def load_data(self):
        raise NotImplementedError("子类必须实现load_data方法")

class TwitterReader(SocialMediaReader):
    """
    Twitter数据读取器示例
    注意：实际使用需要Twitter API认证
    """
    def __init__(self, bearer_token=None):
        super().__init__()
        self.bearer_token = bearer_token
        self.headers = {"Authorization": f"Bearer {bearer_token}"} if bearer_token else {}
    
    def load_data(self, query="#example", max_results=10):
        """
        根据查询加载推文数据
        注意：这只是一个示例框架，实际需要有效的API密钥
        """
        # 模拟数据（实际应用中应调用Twitter API）
        mock_tweets = [
            {"id": "1", "text": "这是第一条示例推文内容", "author": "user1", "created_at": "2023-01-01"},
            {"id": "2", "text": "这是第二条示例推文内容，包含一些话题标签 #example", "author": "user2", "created_at": "2023-01-02"},
            {"id": "3", "text": "第三条推文内容，用于演示社交媒体数据加载", "author": "user3", "created_at": "2023-01-03"}
        ]
        
        # 转换为Document格式
        from llama_index.core import Document
        
        documents = []
        for tweet in mock_tweets[:max_results]:
            doc_text = f"Tweet from @{tweet['author']} on {tweet['created_at']}:\n{tweet['text']}"
            doc = Document(text=doc_text, metadata=tweet)
            documents.append(doc)
        
        print(f"加载了 {len(documents)} 条社交媒体数据")
        return documents

def load_social_media_data():
    """
    加载社交媒体公开数据
    """
    # 初始化Twitter读取器
    reader = TwitterReader(bearer_token=None)  # 实际使用时需要提供有效token
    
    # 加载数据
    documents = reader.load_data(query="#example", max_results=5)
    
    if not documents:
        print("未加载到任何社交媒体数据")
        return []
    
    # 分割数据
    splitter = SentenceSplitter(chunk_size=256, chunk_overlap=10)
    nodes = splitter.get_nodes_from_documents(documents)
    
    return nodes

if __name__ == "__main__":
    print("正在加载社交媒体数据...")
    nodes = load_social_media_data()
    
    if nodes:
        print(f"社交媒体数据已分割为 {len(nodes)} 个节点")
        for i, node in enumerate(nodes[:2]):  # 显示前2个节点
            print(f"\n节点 {i+1}:")
            print(node.text[:150] + "..." if len(node.text) > 150 else node.text)
    else:
        print("使用模拟数据完成演示")