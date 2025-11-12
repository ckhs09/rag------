"""
Query Decomposition 示例
将初始查询的输入问题分解成不同的多个子问题，分别查询，最后合成答案
"""

import re

def identify_question_components(query):
    """
    识别问题的主要组成部分
    """
    # 识别疑问词
    wh_words = ["what", "how", "why", "when", "where", "who", "which", "whose", "whom"]
    wh_match = None
    for wh in wh_words:
        if wh in query.lower():
            wh_match = wh
            break
    
    # 识别主要实体
    # 这是一个简化的实体识别方法
    entities = []
    # 查找可能的实体名词（这里使用简单的启发式方法）
    words = query.split()
    for i, word in enumerate(words):
        # 如果单词以大写字母开头或者是我们知道的实体词
        known_entities = ["python", "java", "react", "vue", "database", "sql", "nosql", "api", "rest", "graphql"]
        if word[0].isupper() or word.lower() in known_entities:
            entities.append(word)
    
    return {
        "wh_word": wh_match,
        "entities": entities,
        "raw_query": query
    }

def decompose_complex_query(query):
    """
    将复杂查询分解为多个子问题
    """
    subqueries = []
    
    # 模式1: "X和Y的区别/比较" 类型
    comparison_pattern = r"(.+?)和(.+?)(?:区别|比较|不同)"
    match = re.search(comparison_pattern, query)
    if match:
        item1, item2 = match.group(1), match.group(2)
        subqueries.append(f"{item1}是什么？")
        subqueries.append(f"{item2}是什么？")
        subqueries.append(f"{item1}和{item2}有什么不同？")
        return subqueries
    
    # 模式2: "如何X Y" 类型
    how_pattern = r"如何(.+?)(.+)"
    match = re.match(how_pattern, query)
    if match:
        action, object_ = match.group(1), match.group(2)
        subqueries.append(f"{action}{object_}的步骤是什么？")
        subqueries.append(f"{action}{object_}需要哪些工具或准备？")
        subqueries.append(f"{action}{object_}有什么注意事项？")
        return subqueries
    
    # 模式3: 复杂的多实体问题
    components = identify_question_components(query)
    entities = components["entities"]
    
    if len(entities) > 1:
        # 为每个实体创建子问题
        for entity in entities:
            subqueries.append(f"{entity}是什么？")
        
        # 添加关系问题
        if components["wh_word"]:
            subqueries.append(f"{components['wh_word']}是{', '.join(entities)}之间的关系？")
        else:
            subqueries.append(f"什么是{', '.join(entities)}之间的关系？")
        return subqueries
    
    # 默认分解方法
    if "的" in query:
        parts = query.split("的")
        for i in range(len(parts)):
            if i == 0:
                subqueries.append(f"{parts[i]}是什么？")
            else:
                subqueries.append(f"{parts[i]}是什么？")
        return subqueries
    
    # 如果无法分解，返回原查询
    return [query]

def decompose_for_multi_aspect_query(query):
    """
    将多方面问题分解为多个单一问题
    """
    # 识别问题的多个方面
    aspects = ["定义", "用途", "优势", "劣势", "示例", "历史", "发展", "原理"]
    
    subqueries = []
    
    # 检查查询是否询问多个方面
    aspect_indicators = {
        "定义": ["定义", "是什么", "意思", "概念"],
        "用途": ["用途", "用法", "使用", "应用", "作用"],
        "优势": ["优势", "优点", "好处", "优点"],
        "劣势": ["劣势", "缺点", "不足", "问题"],
        "示例": ["示例", "例子", "实例", "举例"],
        "历史": ["历史", "起源", "由来"],
        "发展": ["发展", "演变", "趋势", "未来"],
        "原理": ["原理", "机制", "工作方式", "如何工作"]
    }
    
    # 创建一个基础查询（去除方面指示词）
    base_query = query
    identified_aspects = []
    
    for aspect, indicators in aspect_indicators.items():
        for indicator in indicators:
            if indicator in query:
                identified_aspects.append(aspect)
                base_query = base_query.replace(indicator, "").replace("  ", " ").strip()
                break
    
    # 为每个识别的方面生成子问题
    if identified_aspects:
        for aspect in identified_aspects:
            subqueries.append(f"{base_query}的{aspect}是什么？")
    else:
        # 如果没有识别到特定方面，默认分解为几个常见方面
        for aspect in ["定义", "用途", "优势"]:
            subqueries.append(f"{query}的{aspect}是什么？")
    
    return subqueries

# 示例使用
if __name__ == "__main__":
    test_queries = [
        "Python和Java的区别",
        "如何学习机器学习",
        "React和Vue的比较",
        "数据库索引的原理和优势",
        "REST API是什么"
    ]
    
    print("=== 复杂查询分解示例 ===")
    for query in test_queries:
        print(f"原始查询: {query}")
        subqueries = decompose_complex_query(query)
        for i, subq in enumerate(subqueries, 1):
            print(f"  子问题{i}: {subq}")
        print()
    
    print("=== 多方面问题分解示例 ===")
    multi_aspect_queries = [
        "数据库索引的原理和优势",
        "机器学习的发展和应用"
    ]
    
    for query in multi_aspect_queries:
        print(f"原始查询: {query}")
        subqueries = decompose_for_multi_aspect_query(query)
        for i, subq in enumerate(subqueries, 1):
            print(f"  子问题{i}: {subq}")
        print()