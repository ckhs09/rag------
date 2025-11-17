"""
多模态文档处理器
该模块演示了如何处理包含文本、表格和图像的多模态文档
"""

import os
from typing import List, Dict, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class MultimodalElement:
    """多模态元素基类"""
    element_type: str  # text, table, image
    content: Any       # 元素内容
    metadata: Dict     # 元素元数据


class DocumentParser(ABC):
    """文档解析器抽象基类"""
    
    @abstractmethod
    def parse(self, file_path: str) -> List[MultimodalElement]:
        pass


class SimpleTextParser(DocumentParser):
    """简单文本解析器"""
    
    def parse(self, file_path: str) -> List[MultimodalElement]:
        elements = []
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 简单按段落分割文本
        paragraphs = content.split('\n\n')
        for i, para in enumerate(paragraphs):
            if para.strip():
                elements.append(MultimodalElement(
                    element_type="text",
                    content=para.strip(),
                    metadata={"source": file_path, "paragraph_index": i}
                ))
        
        return elements


class Chunker:
    """文本切分器"""
    
    def chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """将文本切分为指定大小的块"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks


class Vectorizer:
    """向量化器"""
    
    def vectorize(self, content: str) -> List[float]:
        """模拟向量化过程"""
        # 在实际应用中，这里会使用真实的嵌入模型如SentenceTransformer
        # 这里我们简化为基于字符长度的模拟向量
        vector = [len(content) % 100 / 100.0, 
                 hash(content[:10]) % 100 / 100.0,
                 len(content.split()) % 100 / 100.0]
        return vector


class MultimodalStorage:
    """多模态存储"""
    
    def __init__(self):
        self.documents = []  # 存储所有文档元素
    
    def store(self, element: MultimodalElement, vector: List[float]):
        """存储文档元素及其向量"""
        stored_element = {
            "element": element,
            "vector": vector
        }
        self.documents.append(stored_element)
    
    def search(self, query_vector: List[float], top_k: int = 3) -> List[Dict]:
        """基于向量相似度搜索最相关的文档"""
        # 简化的相似度计算（欧氏距离）
        def euclidean_distance(v1, v2):
            return sum((a - b) ** 2 for a, b in zip(v1, v2)) ** 0.5
        
        # 计算所有文档与查询的相似度
        similarities = []
        for doc in self.documents:
            distance = euclidean_distance(query_vector, doc["vector"])
            similarities.append((doc, 1 / (1 + distance)))  # 转换为相似度分数
        
        # 按相似度排序并返回top_k个结果
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in similarities[:top_k]]


class MultimodalProcessor:
    """多模态文档处理器主类"""
    
    def __init__(self):
        self.parser = SimpleTextParser()
        self.chunker = Chunker()
        self.vectorizer = Vectorizer()
        self.storage = MultimodalStorage()
    
    def process_document(self, file_path: str):
        """处理文档的完整流程"""
        print(f"Processing document: {file_path}")
        
        # 1. 解析与提取
        elements = self.parser.parse(file_path)
        print(f"Parsed {len(elements)} elements")
        
        # 2. 预处理与切分
        processed_elements = []
        for element in elements:
            if element.element_type == "text":
                # 对文本进行切分
                chunks = self.chunker.chunk_text(element.content)
                for i, chunk in enumerate(chunks):
                    chunk_element = MultimodalElement(
                        element_type="text",
                        content=chunk,
                        metadata={**element.metadata, "chunk_index": i}
                    )
                    processed_elements.append(chunk_element)
            else:
                processed_elements.append(element)
        
        print(f"Processed into {len(processed_elements)} chunks")
        
        # 3. 向量化与索引
        for element in processed_elements:
            vector = self.vectorizer.vectorize(element.content)
            self.storage.store(element, vector)
        
        print("Document processing completed!")
    
    def query(self, query_text: str, top_k: int = 3) -> List[Dict]:
        """查询接口"""
        query_vector = self.vectorizer.vectorize(query_text)
        results = self.storage.search(query_vector, top_k)
        return results


# 使用示例
if __name__ == "__main__":
    # 创建示例文档
    sample_doc = """多模态文档处理技术
    多模态文档处理是指对包含文本、表格、图像等多种类型内容的文档进行综合处理的技术。
    
    核心组件包括：
    1. 文档解析：提取不同类型的内容
    2. 内容切分：将长文本分割为适当大小的块
    3. 向量化：将文本转换为向量表示
    4. 存储与检索：建立索引并支持快速检索
    
    技术优势：
    - 支持复杂的文档结构
    - 提高检索准确性
    - 实现跨模态的信息融合"""
    
    with open("sample_document.txt", "w", encoding="utf-8") as f:
        f.write(sample_doc)
    
    # 初始化处理器
    processor = MultimodalProcessor()
    
    # 处理文档
    processor.process_document("sample_document.txt")
    
    # 查询示例
    results = processor.query("什么是多模态文档处理？")
    
    print("\n查询结果:")
    for i, result in enumerate(results, 1):
        print(f"{i}. 类型: {result['element'].element_type}")
        print(f"   内容: {result['element'].content[:100]}...")
        print(f"   元数据: {result['element'].metadata}\n")