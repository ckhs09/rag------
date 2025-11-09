"""
Document Summary Index 示例

这个文件演示了如何创建和使用文档摘要索引。
文档摘要索引用于从文档中提取摘要信息，便于快速浏览和检索。
"""

try:
    from llama_index.core import Document, SummaryIndex
    from llama_index.llms.openai import OpenAI
except ImportError:
    print("请安装所需的依赖库: pip install llama-index")

def create_summary_index():
    """创建一个文档摘要索引示例"""
    
    # 创建示例文档
    documents = [
        Document(text="LlamaIndex是一个用于连接大型语言模型(LLM)和外部数据的强大框架。它简化了构建基于LLM的应用程序的过程。"),
        Document(text="文档摘要索引是LlamaIndex提供的一种索引类型。它主要用于从长文档中提取摘要信息。"),
        Document(text="使用文档摘要索引可以显著减少处理大量文本所需的时间和计算资源。"),
    ]
    
    # 创建摘要索引
    summary_index = SummaryIndex.from_documents(documents)
    
    return summary_index

def query_summary_index(index):
    """查询摘要索引"""
    
    # 创建查询引擎
    query_engine = index.as_query_engine()
    
    # 查询示例
    response = query_engine.query("什么是LlamaIndex？")
    print(f"问题: 什么是LlamaIndex？")
    print(f"回答: {response}\n")
    
    response = query_engine.query("文档摘要索引的主要用途是什么？")
    print(f"问题: 文档摘要索引的主要用途是什么？")
    print(f"回答: {response}\n")

if __name__ == "__main__":
    print("=== 文档摘要索引示例 ===\n")
    
    # 创建索引
    summary_index = create_summary_index()
    
    # 查询索引
    query_summary_index(summary_index)