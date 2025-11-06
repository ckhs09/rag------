#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
相似度计算算法实现
包含余弦相似度、点积、欧几里得距离三种算法
用于理解和比较嵌入模型中的相似度计算方法
"""

import math
from typing import List, Union


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    计算两个向量之间的余弦相似度
    
    余弦相似度衡量两个向量在方向上的相似性，不考虑 magnitude
    值范围: [-1, 1]，1表示完全相同方向，-1表示完全相反方向，0表示垂直
    
    Args:
        vec1: 第一个向量
        vec2: 第二个向量
        
    Returns:
        float: 余弦相似度值
        
    Raises:
        ValueError: 当向量维度不匹配或为空时
    """
    if len(vec1) != len(vec2):
        raise ValueError("向量维度必须相同")
    
    if len(vec1) == 0:
        raise ValueError("向量不能为空")
    
    # 计算点积
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    
    # 计算向量的模长
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    
    # 避免除零错误
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    # 计算余弦相似度
    cosine_sim = dot_product / (magnitude1 * magnitude2)
    
    return cosine_sim


def dot_product(vec1: List[float], vec2: List[float]) -> float:
    """
    计算两个向量之间的点积
    
    点积衡量两个向量在方向和magnitude上的综合相似性
    值范围: (-∞, +∞)，值越大表示越相似
    
    Args:
        vec1: 第一个向量
        vec2: 第二个向量
        
    Returns:
        float: 点积值
        
    Raises:
        ValueError: 当向量维度不匹配时
    """
    if len(vec1) != len(vec2):
        raise ValueError("向量维度必须相同")
    
    return sum(a * b for a, b in zip(vec1, vec2))


def euclidean_distance(vec1: List[float], vec2: List[float]) -> float:
    """
    计算两个向量之间的欧几里得距离
    
    欧几里得距离衡量两个向量在空间中的直线距离
    值范围: [0, +∞)，0表示完全相同，值越大表示越不相似
    
    Args:
        vec1: 第一个向量
        vec2: 第二个向量
        
    Returns:
        float: 欧几里得距离值
        
    Raises:
        ValueError: 当向量维度不匹配时
    """
    if len(vec1) != len(vec2):
        raise ValueError("向量维度必须相同")
    
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))


def normalize_vector(vec: List[float]) -> List[float]:
    """
    对向量进行归一化处理（L2归一化）
    
    Args:
        vec: 输入向量
        
    Returns:
        List[float]: 归一化后的向量
    """
    magnitude = math.sqrt(sum(a * a for a in vec))
    if magnitude == 0:
        return vec
    return [a / magnitude for a in vec]


def similarity_comparison(vec1: List[float], vec2: List[float]) -> dict:
    """
    综合比较两个向量的三种相似度计算结果
    
    Args:
        vec1: 第一个向量
        vec2: 第二个向量
        
    Returns:
        dict: 包含三种相似度计算结果的字典
    """
    # 归一化向量用于比较
    norm_vec1 = normalize_vector(vec1)
    norm_vec2 = normalize_vector(vec2)
    
    results = {
        "cosine_similarity": cosine_similarity(vec1, vec2),
        "dot_product": dot_product(vec1, vec2),
        "euclidean_distance": euclidean_distance(vec1, vec2),
        "cosine_similarity_normalized": cosine_similarity(norm_vec1, norm_vec2),
        "dot_product_normalized": dot_product(norm_vec1, norm_vec2),
        "euclidean_distance_normalized": euclidean_distance(norm_vec1, norm_vec2)
    }
    
    return results


# 示例和测试代码
if __name__ == "__main__":
    # 定义测试向量
    vector_a = [1.0, 2.0, 3.0]
    vector_b = [4.0, 5.0, 6.0]
    vector_c = [1.0, 2.0, 3.0]  # 与A相同
    vector_d = [-1.0, -2.0, -3.0]  # 与A相反
    
    print("向量相似度计算示例:")
    print(f"向量 A: {vector_a}")
    print(f"向量 B: {vector_b}")
    print(f"向量 C: {vector_c} (与A相同)")
    print(f"向量 D: {vector_d} (与A相反)")
    print("-" * 50)
    
    # 计算相似度
    print("原始向量比较:")
    print(f"A 和 B 的余弦相似度: {cosine_similarity(vector_a, vector_b):.4f}")
    print(f"A 和 B 的点积: {dot_product(vector_a, vector_b):.4f}")
    print(f"A 和 B 的欧几里得距离: {euclidean_distance(vector_a, vector_b):.4f}")
    print()
    
    print("相同向量比较:")
    print(f"A 和 C 的余弦相似度: {cosine_similarity(vector_a, vector_c):.4f}")
    print(f"A 和 C 的点积: {dot_product(vector_a, vector_c):.4f}")
    print(f"A 和 C 的欧几里得距离: {euclidean_distance(vector_a, vector_c):.4f}")
    print()
    
    print("相反向量比较:")
    print(f"A 和 D 的余弦相似度: {cosine_similarity(vector_a, vector_d):.4f}")
    print(f"A 和 D 的点积: {dot_product(vector_a, vector_d):.4f}")
    print(f"A 和 D 的欧几里得距离: {euclidean_distance(vector_a, vector_d):.4f}")
    print()
    
    # 综合比较
    print("综合比较结果:")
    comparison = similarity_comparison(vector_a, vector_b)
    for key, value in comparison.items():
        print(f"{key}: {value:.4f}")