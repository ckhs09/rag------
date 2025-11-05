# src/document_loader.py
import os
from typing import List

def load_document(file_path: str) -> str:
    """
    加载TXT文档
    
    Args:
        file_path: 文档路径
        
    Returns:
        文档内容字符串
        
    Raises:
        FileNotFoundError: 当文件不存在时
        IOError: 当文件读取失败时
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件 {file_path} 不存在")
    
    # 检查文件扩展名
    if not file_path.endswith('.txt'):
        raise ValueError("只支持TXT格式的文件")
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        raise IOError(f"读取文件失败: {str(e)}")

def split_document(document: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """
    使用递归字符分割器将文档分割成较小的块
    
    Args:
        document: 文档内容
        chunk_size: 每个块的最大长度
        chunk_overlap: 块之间的重叠长度
        
    Returns:
        分割后的文档块列表
    """
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""]
    )
    
    texts = text_splitter.split_text(document)
    return texts