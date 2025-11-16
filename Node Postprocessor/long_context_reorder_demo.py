"""
LongContextReorder 演示脚本

此脚本演示了如何使用 LongContextReorder 来重新排列检索结果。
LongContextReorder 将最相关的节点放在上下文的开头和结尾，因为 LLM 通常对首尾内容关注度更高。
"""

import logging
logging.basicConfig(level=logging.INFO)

from llama_index.core.postprocessor import LongContextReorder
from llama_index.core.schema import TextNode


def create_sample_data():
    """创建示例文档数据"""
    documents = [
        TextNode(text="人工智能概述：人工智能是计算机科学的一个重要分支，致力于创造能够模拟人类智能行为的系统。"),
        TextNode(text="机器学习基础：机器学习是实现人工智能的核心技术，通过算法使计算机能够从数据中自动学习规律。"),
        TextNode(text="深度学习原理：深度学习采用多层神经网络来模拟大脑处理信息的方式，是目前AI领域的研究热点。"),
        TextNode(text="自然语言处理：NLP技术使得计算机能够理解和生成人类语言，广泛应用于翻译、对话系统等领域。"),
        TextNode(text="计算机视觉应用：CV技术赋予计算机观察和理解图像的能力，在安防、医疗等领域发挥重要作用。"),
        TextNode(text="强化学习机制：强化学习通过奖励和惩罚机制训练智能体在环境中做出最优决策。"),
        TextNode(text="知识图谱构建：知识图谱以结构化方式表示现实世界中的实体及其相互关系。"),
        TextNode(text="语音识别技术：语音识别实现了人类语言到文字的自动转换，为人机交互提供了便利。"),
        TextNode(text="推荐系统设计：推荐系统通过分析用户行为数据为其提供个性化的物品推荐服务。"),
        TextNode(text="AI伦理与安全：在AI快速发展的同时，也需要关注其带来的伦理和社会影响问题。"),
    ]
    
    # 为节点分配人工模拟的相似度分数（有高有低）
    similarities = [0.95, 0.3, 0.88, 0.2, 0.85, 0.4, 0.82, 0.6, 0.92, 0.1]
    for i, node in enumerate(documents):
        node.score = similarities[i]
        
    return documents


def main():
    print("=== LongContextReorder 演示 ===\n")
    
    # 创建示例数据
    nodes = create_sample_data()
    
    print("原始节点 (按相似度降序排列):")
    sorted_nodes = sorted(nodes, key=lambda x: x.score, reverse=True)
    for i, node in enumerate(sorted_nodes):
        print(f"{i+1}. (相似度: {node.score:.2f}) {node.text[:50]}...")
    
    print("\n" + "="*50 + "\n")
    
    # 使用 LongContextReorder 重新排序
    processor = LongContextReorder()
    reordered_nodes = processor.postprocess_nodes(nodes)
    
    print("使用 LongContextReorder 重排序后:")
    for i, node in enumerate(reordered_nodes):
        position_desc = ""
        if i == 0:
            position_desc = " (移到开头)"
        elif i == len(reordered_nodes) - 1:
            position_desc = " (移到末尾)"
        elif i == 1 or i == len(reordered_nodes) - 2:
            position_desc = " (保持原位)"
        else:
            position_desc = " (保持原位)"
            
        print(f"{i+1}. (相似度: {node.score:.2f}) {node.text[:50]}...{position_desc}")
    
    print("\n" + "="*50 + "\n")
    
    print("重排序规则说明:")
    print("1. 最相关的节点(相似度最高)被放置在开头和结尾")
    print("2. 相关性较低的节点放置在中间位置")
    print("3. 这种排序利用了LLM对上下文首尾内容关注度更高的特点")


if __name__ == "__main__":
    main()