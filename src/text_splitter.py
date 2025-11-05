# src/text_splitter.py
import jieba
import re
from typing import List

def split_text_by_sentences(source_text: str, sentences_per_chunk: int, overlap: int) -> List[str]:
    """
    简单地把文档分割为多个知识块，每个知识块都包含指定数量的句子
    
    Args:
        source_text: 源文本内容
        sentences_per_chunk: 每个知识块包含的句子数
        overlap: 相邻知识块之间的重叠句子数
    
    Returns:
        分割后的知识块列表
    """
    # 使用正则表达式分割句子，保留分隔符
    sentence_endings = r'[。！？.!?]'
    sentences = re.split(f'({sentence_endings})', source_text)
    
    # 重新组合句子与其标点符号
    combined_sentences = []
    for i in range(0, len(sentences)-1, 2):
        if i+1 < len(sentences):
            combined_sentences.append(sentences[i] + sentences[i+1])
        else:
            combined_sentences.append(sentences[i])
    
    # 处理最后一个元素（如果没有标点符号结尾）
    if len(sentences) % 2 == 1 and sentences[-1].strip():
        combined_sentences.append(sentences[-1])
    
    # 将句子分组成知识块
    chunks = []
    for i in range(0, len(combined_sentences), sentences_per_chunk - overlap):
        chunk_sentences = combined_sentences[i:i + sentences_per_chunk]
        if chunk_sentences:  # 只添加非空的知识块
            chunk = ''.join(chunk_sentences)
            chunks.append(chunk.strip())
        
        # 如果剩余句子不足，提前退出循环
        if i + sentences_per_chunk >= len(combined_sentences):
            break
    
    return chunks