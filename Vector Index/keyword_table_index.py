"""
Keyword Table Index 示例

这个文件演示了如何创建和使用关键词表索引。
关键词表索引用于基于关键词的快速检索，通过提取文档中的关键词来构建索引表。
"""

try:
    from llama_index.core import Document
    from llama_index.core.indices.keyword_table import KeywordTableIndex
    from llama_index.llms.openai import OpenAI
except ImportError:
    print("请安装所需的依赖库: pip install llama-index")

def create_keyword_table_index():
    """创建关键词表索引示例"""
    
    # 创建示例文档
    documents = [
        Document(text="Python是一种高级编程语言，以其简洁和易读性而闻名。它广泛用于Web开发、数据科学和人工智能领域。"),
        Document(text="机器学习是人工智能的一个重要分支，通过算法使计算机能够从数据中学习并做出预测。"),
        Document(text="Web开发涉及创建网站和Web应用程序。常用的前端技术包括HTML、CSS和JavaScript。"),
        Document(text="数据科学是一门跨学科领域，结合了统计学、计算机科学和专业知识，用于从数据中提取洞察。"),
    ]
    
    # 创建关键词表索引
    keyword_index = KeywordTableIndex.from_documents(documents)
    
    return keyword_index

def query_keyword_table_index(index):
    """查询关键词表索引"""
    
    # 创建查询引擎
    query_engine = index.as_query_engine()
    
    # 查询示例
    response = query_engine.query("Python的应用领域有哪些？")
    print(f"问题: Python的应用领域有哪些？")
    print(f"回答: {response}\n")
    
    response = query_engine.query("什么是Web开发？")
    print(f"问题: 什么是Web开发？")
    print(f"回答: {response}\n")

if __name__ == "__main__":
    print("=== 关键词表索引示例 ===\n")
    
    # 创建索引
    keyword_index = create_keyword_table_index()
    
    # 查询索引
    query_keyword_table_index(keyword_index)