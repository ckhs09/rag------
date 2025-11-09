"""
Tree Index 示例

这个文件演示了如何创建和使用树索引。
树索引用于层次化数据的索引，通过构建树状结构来组织和检索信息。
"""

try:
    from llama_index.core import Document
    from llama_index.core.indices.tree import TreeIndex
    from llama_index.llms.openai import OpenAI
except ImportError:
    print("请安装所需的依赖库: pip install llama-index")

def create_tree_index():
    """创建树索引示例"""
    
    # 创建示例文档
    documents = [
        Document(text="计算机科学是研究计算机及其应用的学科。它包含许多子领域。"),
        Document(text="人工智能是计算机科学的一个分支，致力于创建智能机器。机器学习是人工智能的一个子集。"),
        Document(text="数据结构是计算机科学中的重要概念，用于组织和存储数据。数组和链表是基本的数据结构。"),
        Document(text="算法是解决问题的步骤集合，是编程的基础。排序算法包括冒泡排序和快速排序等。"),
    ]
    
    # 创建树索引
    tree_index = TreeIndex.from_documents(documents)
    
    return tree_index

def query_tree_index(index):
    """查询树索引"""
    
    # 创建查询引擎
    query_engine = index.as_query_engine()
    
    # 查询示例
    response = query_engine.query("计算机科学包含哪些子领域？")
    print(f"问题: 计算机科学包含哪些子领域？")
    print(f"回答: {response}\n")
    
    response = query_engine.query("人工智能和机器学习有什么关系？")
    print(f"问题: 人工智能和机器学习有什么关系？")
    print(f"回答: {response}\n")

if __name__ == "__main__":
    print("=== 树索引示例 ===\n")
    
    # 创建索引
    tree_index = create_tree_index()
    
    # 查询索引
    query_tree_index(tree_index)