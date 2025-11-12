"""
查询转换（Query Transformations）完整演示
展示四种主要的查询转换类型：
1. 查询重写（Reformulate）
2. 查询扩展（Expand）
3. 查询分解（Decompose）
4. 多步查询（Step Back）
"""

from reformulate.reformulate_query import basic_reformulate, specific_reformulate, multiple_reformulations
from expand.expand_query import expand_with_synonyms, expand_with_context, expand_with_hyde
from decompose.decompose_query import decompose_complex_query, decompose_for_multi_aspect_query
from step_back.step_back_query import step_back_and_decompose

def demonstrate_all_transformations():
    """
    演示所有查询转换类型
    """
    # 测试查询
    test_query = "如何实现快速排序算法"
    
    print("=" * 60)
    print("查询转换（Query Transformations）完整演示")
    print("=" * 60)
    print(f"原始查询: {test_query}")
    print()
    
    # 1. 查询重写
    print("1. 查询重写（Reformulate）")
    print("-" * 30)
    print(f"基础重写: {basic_reformulate(test_query)}")
    print(f"特定领域重写: {specific_reformulate(test_query)}")
    print("多版本重写:")
    for rf in multiple_reformulations(test_query):
        print(f"  {rf}")
    print()
    
    # 2. 查询扩展
    print("2. 查询扩展（Expand）")
    print("-" * 30)
    print("同义词扩展:")
    for exp in expand_with_synonyms(test_query):
        print(f"  {exp}")
    print("上下文扩展:")
    for exp in expand_with_context(test_query):
        print(f"  {exp}")
    print("HyDE扩展:")
    for exp in expand_with_hyde(test_query):
        print(f"  {exp}")
    print()
    
    # 3. 查询分解
    print("3. 查询分解（Decompose）")
    print("-" * 30)
    print("复杂查询分解:")
    for i, subq in enumerate(decompose_complex_query(test_query), 1):
        print(f"  子问题{i}: {subq}")
    print("多方面查询分解:")
    for i, subq in enumerate(decompose_for_multi_aspect_query(test_query), 1):
        print(f"  子问题{i}: {subq}")
    print()
    
    # 4. 多步查询
    print("4. 多步查询（Step Back）")
    print("-" * 30)
    result = step_back_and_decompose(test_query)
    print(f"抽象问题: {result['step_back_query']}")
    print("执行步骤:")
    for step in result['steps']:
        print(f"  步骤 {step['step']}: {step['query']}")
    print()

if __name__ == "__main__":
    demonstrate_all_transformations()
    
    # 额外演示其他查询
    print("\n" + "=" * 60)
    print("额外示例演示")
    print("=" * 60)
    
    additional_queries = [
        "机器学习与深度学习的区别",
        "数据库索引的原理和优势"
    ]
    
    for query in additional_queries:
        print(f"\n原始查询: {query}")
        print("查询分解结果:")
        subqueries = decompose_complex_query(query)
        for i, subq in enumerate(subqueries, 1):
            print(f"  子问题{i}: {subq}")