"""
高级多模态文档处理器
该模块展示了更完整的多模态文档处理流程，包括表格和图像处理的模拟实现
"""

import json
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum


class ElementType(Enum):
    """元素类型枚举"""
    TEXT = "text"
    TABLE = "table"
    IMAGE = "image"


@dataclass
class MultimodalElement:
    """多模态元素"""
    element_type: ElementType
    content: Any
    metadata: Dict[str, Any]
    vector: List[float] = None
    
    def to_dict(self):
        return {
            "element_type": self.element_type.value,
            "content": self.content,
            "metadata": self.metadata,
            "vector": self.vector
        }


class AdvancedDocumentParser:
    """高级文档解析器"""
    
    def parse_mixed_document(self, file_path: str) -> List[MultimodalElement]:
        """
        模拟解析包含文本、表格和图像的混合文档
        在实际应用中，这里会集成PDF解析库、OCR引擎等
        """
        elements = []
        
        # 模拟解析出的文本内容
        text_content = """多模态文档处理技术概述
        
        多模态文档处理是一种新兴的信息处理技术，能够同时处理文本、表格和图像等不同形式的内容。"""
        
        elements.append(MultimodalElement(
            element_type=ElementType.TEXT,
            content=text_content,
            metadata={
                "page": 1,
                "position": "beginning",
                "source": file_path
            }
        ))
        
        # 模拟解析出的表格内容
        table_content = {
            "headers": ["技术组件", "功能描述", "重要程度"],
            "rows": [
                ["文档解析", "提取不同模态内容", "高"],
                ["内容切分", "分割长文本为块", "中"],
                ["向量化", "转换为向量表示", "高"],
                ["索引构建", "建立高效检索结构", "高"]
            ]
        }
        
        elements.append(MultimodalElement(
            element_type=ElementType.TABLE,
            content=table_content,
            metadata={
                "page": 1,
                "position": "middle",
                "source": file_path
            }
        ))
        
        # 模拟解析出的图像内容（OCR后的文本描述）
        image_content = "系统架构图：展示了一个三层架构，包括表示层、业务逻辑层和数据访问层。"
        
        elements.append(MultimodalElement(
            element_type=ElementType.IMAGE,
            content=image_content,
            metadata={
                "page": 2,
                "position": "top",
                "description": "系统架构示意图",
                "source": file_path
            }
        ))
        
        return elements


class ContentChunker:
    """内容切分器"""
    
    def chunk_text(self, text: str, max_chunk_size: int = 300) -> List[str]:
        """切分文本"""
        paragraphs = text.split('\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) <= max_chunk_size:
                current_chunk += paragraph + "\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + "\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
    
    def process_table(self, table_data: dict) -> List[str]:
        """处理表格数据，生成可检索的文本描述"""
        descriptions = []
        
        # 表格整体描述
        headers_str = ", ".join(table_data["headers"])
        table_desc = f"表格包含以下列: {headers_str}"
        descriptions.append(table_desc)
        
        # 每行数据的描述
        for row in table_data["rows"]:
            row_desc = f"数据行: {', '.join(row)}"
            descriptions.append(row_desc)
            
        return descriptions


class Vectorizer:
    """向量化器"""
    
    def vectorize(self, content: str) -> List[float]:
        """
        简单的文本向量化实现
        在实际应用中，这里会使用预训练的嵌入模型如BERT、Sentence-BERT等
        """
        # 简化的向量表示方法
        words = content.split()
        vector = [
            min(len(words) / 100, 1.0),           # 文本长度特征
            min(len(content) / 1000, 1.0),        # 字符数特征
            hash(content[:20]) % 1000 / 1000.0    # 内容哈希特征
        ]
        return vector


class MultimodalIndex:
    """多模态索引"""
    
    def __init__(self):
        self.elements: List[MultimodalElement] = []
    
    def add_element(self, element: MultimodalElement):
        """添加元素到索引"""
        # 为元素生成向量表示
        if isinstance(element.content, str):
            element.vector = self._vectorizer.vectorize(element.content)
        elif isinstance(element.content, dict):
            # 对于表格等结构化数据，先转换为文本再向量化
            content_str = json.dumps(element.content)
            element.vector = self._vectorizer.vectorize(content_str)
        
        self.elements.append(element)
    
    def _vectorizer(self):
        """获取向量化器实例"""
        return Vectorizer()
    
    def search(self, query: str, top_k: int = 3) -> List[MultimodalElement]:
        """基于向量相似度的搜索"""
        query_vector = self._vectorizer().vectorize(query)
        
        # 计算相似度（简化版余弦相似度）
        similarities = []
        for element in self.elements:
            similarity = self._cosine_similarity(query_vector, element.vector)
            similarities.append((element, similarity))
        
        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in similarities[:top_k]]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算余弦相似度"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        
        return dot_product / (magnitude1 * magnitude2)


class AdvancedMultimodalProcessor:
    """高级多模态处理器"""
    
    def __init__(self):
        self.parser = AdvancedDocumentParser()
        self.chunker = ContentChunker()
        self.index = MultimodalIndex()
    
    def process_document(self, file_path: str):
        """处理多模态文档"""
        print(f"开始处理文档: {file_path}")
        
        # 1. 解析文档
        raw_elements = self.parser.parse_mixed_document(file_path)
        print(f"解析出 {len(raw_elements)} 个原始元素")
        
        # 2. 预处理和切分
        processed_elements = []
        for element in raw_elements:
            if element.element_type == ElementType.TEXT:
                # 切分文本
                chunks = self.chunker.chunk_text(element.content)
                for i, chunk in enumerate(chunks):
                    text_element = MultimodalElement(
                        element_type=ElementType.TEXT,
                        content=chunk,
                        metadata={**element.metadata, "chunk_id": i}
                    )
                    processed_elements.append(text_element)
                    
            elif element.element_type == ElementType.TABLE:
                # 处理表格为文本描述
                descriptions = self.chunker.process_table(element.content)
                for i, desc in enumerate(descriptions):
                    table_element = MultimodalElement(
                        element_type=ElementType.TEXT,  # 表格已转换为文本
                        content=desc,
                        metadata={**element.metadata, "table_part": i}
                    )
                    processed_elements.append(table_element)
                    
            elif element.element_type == ElementType.IMAGE:
                # 图像已转换为文本描述
                image_element = MultimodalElement(
                    element_type=ElementType.TEXT,  # 图像已转换为文本
                    content=element.content,
                    metadata=element.metadata
                )
                processed_elements.append(image_element)
        
        print(f"预处理后得到 {len(processed_elements)} 个元素")
        
        # 3. 向量化和索引
        for element in processed_elements:
            self.index.add_element(element)
        
        print("文档处理完成！")
    
    def query(self, question: str, top_k: int = 3) -> List[Dict]:
        """查询接口"""
        results = self.index.search(question, top_k)
        
        # 转换为字典格式便于显示
        formatted_results = []
        for result in results:
            formatted_results.append({
                "type": result.element_type.value,
                "content": result.content,
                "metadata": result.metadata,
                "similarity": "N/A"  # 简化处理，实际应该计算具体的相似度值
            })
        
        return formatted_results


# 使用示例
def main():
    # 初始化处理器
    processor = AdvancedMultimodalProcessor()
    
    # 处理示例文档
    processor.process_document("sample_document.txt")
    
    # 执行查询
    queries = [
        "什么是多模态文档处理技术？",
        "文档处理包含哪些技术组件？",
        "系统架构图展示了什么内容？"
    ]
    
    for query in queries:
        print(f"\n查询: {query}")
        results = processor.query(query)
        
        for i, result in enumerate(results, 1):
            print(f"  结果 {i}:")
            print(f"    类型: {result['type']}")
            print(f"    内容: {result['content']}")
            print(f"    元数据: {result['metadata']}")


if __name__ == "__main__":
    main()