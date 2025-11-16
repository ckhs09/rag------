"""
KeywordNodePostprocessor 演示脚本

此脚本演示了如何使用 KeywordNodePostprocessor 来根据关键词筛选节点。
KeywordNodePostprocessor 支持 required_keywords 和 exclude_keywords 参数。
"""

import logging
logging.basicConfig(level=logging.INFO)

from llama_index.core.postprocessor import KeywordNodePostprocessor
from llama_index.core.schema import TextNode


def create_sample_data():
    """创建示例文档数据"""
    documents = [
        TextNode(text="人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。"),
        TextNode(text="机器学习是人工智能的一个子集，它使计算机能够从数据中学习并做出决策或预测。"),
        TextNode(text="深度学习是机器学习的一个分支，它模仿人脑的工作方式处理数据和创建模式，用于决策制定。"),
        TextNode(text="自然语言处理是人工智能的一个领域，致力于让计算机理解和生成人类语言。"),
        TextNode(text="计算机视觉是人工智能的一个领域，专注于让计算机能够看和理解图像及视频内容。"),
        TextNode(text="今天的天气真好，适合外出散步和运动。"),
        TextNode(text="我喜欢在周末阅读书籍和观看电影。"),
    ]
    
    # 为节点分配人工模拟的相似度分数
    similarities = [0.95, 0.92, 0.88, 0.85, 0.82, 0.3, 0.2]
    for i, node in enumerate(documents):
        node.score = similarities[i]
        
    return documents


def main():
    print("=== KeywordNodePostprocessor 演示 ===\n")
    
    # 创建示例数据
    nodes = create_sample_data()
    
    print("原始节点:")
    for i, node in enumerate(nodes):
        print(f"{i+1}. (相似度: {node.score:.2f}) {node.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 使用 KeywordNodePostprocessor 筛选包含指定关键词的节点
    processor = KeywordNodePostprocessor(required_keywords=["人工智能"], exclude_keywords=[])
    filtered_nodes = processor.postprocess_nodes(nodes)
    
    print("使用 KeywordNodePostprocessor 筛选包含'人工智能'关键词的节点:")
    for i, node in enumerate(filtered_nodes):
        print(f"{i+1}. (相似度: {node.score:.2f}) {node.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 使用 KeywordNodePostprocessor 排除包含指定关键词的节点
    processor2 = KeywordNodePostprocessor(required_keywords=[], exclude_keywords=["天气"])
    filtered_nodes2 = processor2.postprocess_nodes(nodes)
    
    print("使用 KeywordNodePostprocessor 排除包含'天气'关键词的节点:")
    for i, node in enumerate(filtered_nodes2):
        print(f"{i+1}. (相似度: {node.score:.2f}) {node.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 同时使用必须包含和排除关键词
    processor3 = KeywordNodePostprocessor(required_keywords=["人工智能"], exclude_keywords=["计算机"])
    filtered_nodes3 = processor3.postprocess_nodes(nodes)
    
    print("使用 KeywordNodePostprocessor 筛选包含'人工智能'但排除'计算机'的节点:")
    for i, node in enumerate(filtered_nodes3):
        print(f"{i+1}. (相似度: {node.score:.2f}) {node.text}")


if __name__ == "__main__":
    main()