"""
Knowledge Graph Index 示例

这个文件演示了如何创建和使用知识图谱索引。
知识图谱索引用于构建和查询实体之间的关系网络。
"""

try:
    from llama_index.core import Document
    from llama_index.core.indices.knowledge_graph import KnowledgeGraphIndex
    from llama_index.llms.openai import OpenAI
except ImportError:
    print("请安装所需的依赖库: pip install llama-index")

def create_knowledge_graph_index():
    """创建知识图谱索引示例"""
    
    # 创建示例文档
    documents = [
        Document(text="苹果公司由史蒂夫·乔布斯、史蒂夫·沃兹尼亚克和罗纳德·韦恩于1976年4月1日创立。"),
        Document(text="史蒂夫·乔布斯是苹果公司的联合创始人之一，担任过CEO职务。"),
        Document(text="iPhone是苹果公司推出的智能手机系列，首次发布于2007年。"),
    ]
    
    # 创建知识图谱索引
    kg_index = KnowledgeGraphIndex.from_documents(documents)
    
    return kg_index

def query_knowledge_graph_index(index):
    """查询知识图谱索引"""
    
    # 创建查询引擎
    query_engine = index.as_query_engine()
    
    # 查询示例
    response = query_engine.query("谁创立了苹果公司？")
    print(f"问题: 谁创立了苹果公司？")
    print(f"回答: {response}\n")
    
    response = query_engine.query("史蒂夫·乔布斯在苹果公司担任什么职务？")
    print(f"问题: 史蒂夫·乔布斯在苹果公司担任什么职务？")
    print(f"回答: {response}\n")

if __name__ == "__main__":
    print("=== 知识图谱索引示例 ===\n")
    
    # 创建索引
    kg_index = create_knowledge_graph_index()
    
    # 查询索引
    query_knowledge_graph_index(kg_index)