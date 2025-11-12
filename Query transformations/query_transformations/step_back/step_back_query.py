"""
Step-back Prompting 示例
将初始查询分解成可以多步完成的子查询，通过分步查询得出答案
"""

def identify_abstraction_level(query):
    """
    识别查询的抽象级别
    """
    # 具体概念关键词
    concrete_indicators = [
        "具体", "详细", "步骤", "如何", "实现", "代码", "示例", 
        "example", "code", "implementation", "step", "how to"
    ]
    
    # 抽象概念关键词
    abstract_indicators = [
        "本质", "原理", "概念", "定义", "基础", "根本", 
        "concept", "principle", "fundamental", "basis", "essence"
    ]
    
    concrete_score = sum(1 for indicator in concrete_indicators if indicator in query.lower())
    abstract_score = sum(1 for indicator in abstract_indicators if indicator in query.lower())
    
    if concrete_score > abstract_score:
        return "concrete"
    elif abstract_score > concrete_score:
        return "abstract"
    else:
        return "neutral"

def step_back_query(query):
    """
    执行"后退一步"操作，将具体问题转换为更抽象的问题
    """
    # 抽象化规则
    abstraction_rules = [
        (r"如何实现(.+)", r"\1是什么"),
        (r"(.+)的步骤是什么", r"\1的本质是什么"),
        (r"(.+)的具体例子", r"\1的概念是什么"),
        (r"(.+)的代码示例", r"\1的原理是什么"),
        (r"为什么(.+)工作", r"(.+)的原理是什么"),
        (r"(.+)如何工作", r"\1的工作原理是什么")
    ]
    
    step_back_question = query
    
    # 应用抽象化规则
    for pattern, replacement in abstraction_rules:
        import re
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            step_back_question = re.sub(pattern, replacement, query, flags=re.IGNORECASE)
            break
    
    # 如果没有匹配的规则，使用通用抽象化
    if step_back_question == query:
        if query.startswith("如何"):
            step_back_question = "什么是" + query[2:] + "的概念？"
        elif "步骤" in query:
            step_back_question = query.replace("步骤", "基本概念")
        else:
            step_back_question = f"什么是{query}的基础知识？"
    
    return step_back_question

def create_step_by_step_plan(abstract_query, original_query):
    """
    基于抽象问题和原始问题创建逐步计划
    """
    steps = []
    
    # 步骤1: 理解基础概念
    steps.append({
        "step": 1,
        "query": abstract_query,
        "purpose": "理解基础概念和原理"
    })
    
    # 步骤2: 了解关键要素
    steps.append({
        "step": 2,
        "query": f"{original_query}涉及哪些关键要素？",
        "purpose": "识别解决问题所需的关键组成部分"
    })
    
    # 步骤3: 学习具体实现
    if "如何" in original_query or "步骤" in original_query:
        steps.append({
            "step": 3,
            "query": original_query,
            "purpose": "学习具体实现方法或步骤"
        })
    
    # 步骤4: 查看示例
    if "如何" in original_query:
        example_query = original_query.replace("如何", "请给出")
        if "请给出" not in example_query:
            example_query = "请给出" + original_query[2:] + "的例子"
            
        steps.append({
            "step": 4,
            "query": example_query,
            "purpose": "通过示例加深理解"
        })
    
    return steps

def step_back_and_decompose(query):
    """
    完整的Step-back和分解过程
    """
    # 识别当前查询的抽象级别
    level = identify_abstraction_level(query)
    
    # 如果查询已经很抽象，直接进行分解
    if level == "abstract":
        return {
            "original_query": query,
            "step_back_query": query,
            "steps": create_step_by_step_plan(query, query)
        }
    
    # 否则执行step-back操作
    abstracted_query = step_back_query(query)
    
    # 创建逐步计划
    steps = create_step_by_step_plan(abstracted_query, query)
    
    return {
        "original_query": query,
        "step_back_query": abstracted_query,
        "steps": steps
    }

# 示例使用
if __name__ == "__main__":
    test_queries = [
        "如何实现快速排序算法",
        "机器学习的基本原理是什么",
        "如何构建REST API",
        "React Hooks的工作原理",
        "数据库索引的实现步骤"
    ]
    
    print("=== Step-back Prompting 示例 ===")
    for query in test_queries:
        print(f"原始查询: {query}")
        
        result = step_back_and_decompose(query)
        print(f"抽象问题: {result['step_back_query']}")
        print("执行步骤:")
        
        for step in result['steps']:
            print(f"  步骤 {step['step']}: {step['query']}")
            print(f"    目的: {step['purpose']}")
        
        print("-" * 50)