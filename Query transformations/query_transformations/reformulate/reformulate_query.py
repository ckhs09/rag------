"""
Query Reformulation 示例
将输入问题转换为更有利于嵌入的问题，以提高召回知识的精确性
"""

import re

def basic_reformulate(query):
    """
    基础查询重写：规范化查询语句
    """
    # 移除多余空格
    query = re.sub(r'\s+', ' ', query).strip()
    
    # 转换为标准问句格式
    if not query.endswith('?'):
        query += '?'
    
    # 将简写转换为完整形式
    replacements = {
        "what's": "what is",
        "don't": "do not",
        "can't": "cannot",
        "won't": "will not",
        "n't": " not",
        "'re": " are",
        "'ve": " have",
        "'ll": " will",
        "'d": " would"
    }
    
    for short, full in replacements.items():
        query = query.replace(short, full)
    
    return query

def specific_reformulate(query):
    """
    特定领域查询重写：添加领域关键词以提高检索准确性
    """
    # 检测是否涉及特定领域
    tech_keywords = ['python', 'java', 'javascript', 'react', 'vue', 'database', 'algorithm']
    
    # 如果查询包含技术关键词，则添加"technical"前缀
    for keyword in tech_keywords:
        if keyword.lower() in query.lower():
            query = f"Technical question about {query}"
            break
    
    return query

def multiple_reformulations(query):
    """
    生成多种查询重写版本
    """
    reformulations = []
    
    # 原始查询
    reformulations.append(f"Original: {query}")
    
    # 简化版本
    simplified = re.sub(r'\b(what|which|how|why|when|where)\b', '', query, 1, flags=re.IGNORECASE)
    simplified = re.sub(r'\s+', ' ', simplified).strip()
    reformulations.append(f"Simplified: {simplified}")
    
    # 详细版本
    detailed = f"Please provide detailed information about: {query}"
    reformulations.append(f"Detailed: {detailed}")
    
    # 问题导向版本
    question_oriented = query
    if not query.lower().startswith('what') and not query.lower().startswith('how'):
        question_oriented = f"What is {query}?"
    reformulations.append(f"Question-oriented: {question_oriented}")
    
    return reformulations

# 示例使用
if __name__ == "__main__":
    test_queries = [
        "what's python",
        "how 2 use react???",
        "explain database indexing",
        "机器学习算法"
    ]
    
    print("=== 基础查询重写示例 ===")
    for query in test_queries:
        print(f"原始查询: {query}")
        print(f"重写结果: {basic_reformulate(query)}")
        print()
    
    print("=== 特定领域查询重写示例 ===")
    for query in test_queries:
        print(f"原始查询: {query}")
        print(f"重写结果: {specific_reformulate(query)}")
        print()
    
    print("=== 多版本查询重写示例 ===")
    for query in test_queries[:2]:  # 只演示前两个
        print(f"原始查询: {query}")
        reformulations = multiple_reformulations(query)
        for rf in reformulations:
            print(f"  {rf}")
        print()