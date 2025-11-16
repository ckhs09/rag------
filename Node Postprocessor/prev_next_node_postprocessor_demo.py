"""
PrevNextNodePostprocessor 演示脚本

此脚本演示了如何使用 PrevNextNodePostprocessor 来添加相邻节点的上下文信息。
PrevNextNodePostprocessor 可以基于文档结构关系，添加前一个或后一个节点作为上下文。
"""

import logging
logging.basicConfig(level=logging.INFO)

from llama_index.core.postprocessor import PrevNextNodePostprocessor
from llama_index.core.schema import TextNode
from llama_index.core.storage.docstore import SimpleDocumentStore


def create_sample_document():
    """创建示例文档数据，模拟文档片段"""
    docstore = SimpleDocumentStore()
    
    # 创建一个模拟文档的不同部分
    nodes = [
        TextNode(
            text="第一章：引言。人工智能是现代计算机科学中的一个重要领域。",
            id_="doc1_part1"
        ),
        TextNode(
            text="第二章：历史发展。人工智能的概念最早可以追溯到20世纪50年代。",
            id_="doc1_part2"
        ),
        TextNode(
            text="第三章：核心技术。机器学习是实现人工智能的关键技术之一。",
            id_="doc1_part3"
        ),
        TextNode(
            text="第四章：应用领域。人工智能已广泛应用于医疗、金融、交通等行业。",
            id_="doc1_part4"
        ),
        TextNode(
            text="第五章：未来发展。随着算力提升和数据积累，AI技术将持续进步。",
            id_="doc1_part5"
        )
    ]
    
    # 添加节点间的关系
    for i in range(len(nodes)):
        if i > 0:
            nodes[i].relationships["previous"] = nodes[i-1].node_id
        if i < len(nodes) - 1:
            nodes[i].relationships["next"] = nodes[i+1].node_id
    
    # 将节点添加到文档存储中
    docstore.add_documents(nodes)
    
    # 为节点分配人工模拟的相似度分数
    similarities = [0.95, 0.3, 0.88, 0.85, 0.92]
    for i, node in enumerate(nodes):
        node.score = similarities[i]
        
    return nodes, docstore


def main():
    print("=== PrevNextNodePostprocessor 演示 ===\n")
    
    # 创建示例数据
    nodes, docstore = create_sample_document()
    
    print("原始节点:")
    for i, node in enumerate(nodes):
        prev_id = node.relationships.get("previous", "None")
        next_id = node.relationships.get("next", "None")
        print(f"{i+1}. (ID: {node.node_id}, 上一节点: {prev_id}, 下一节点: {next_id}) {node.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 模拟检索到的节点（中间部分章节）
    retrieved_nodes = [nodes[2]]  # 只检索到第三章
    print("检索到的节点:")
    for i, node in enumerate(retrieved_nodes):
        print(f"{i+1}. (相似度: {node.score:.2f}) {node.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 使用 PrevNextNodePostprocessor 添加前一个节点作为上下文
    processor = PrevNextNodePostprocessor(
        docstore=docstore,
        num_nodes=1,  # 获取1个相邻节点
        mode="previous"  # 获取前一个节点
    )
    enhanced_nodes = processor.postprocess_nodes(retrieved_nodes)
    
    print("使用 PrevNextNodePostprocessor 添加前一个节点后:")
    for i, node in enumerate(enhanced_nodes):
        print(f"{i+1}. (相似度: {node.score:.2f}) {node.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 使用 PrevNextNodePostprocessor 添加后一个节点作为上下文
    processor2 = PrevNextNodePostprocessor(
        docstore=docstore,
        num_nodes=1,  # 获取1个相邻节点
        mode="next"  # 获取后一个节点
    )
    enhanced_nodes2 = processor2.postprocess_nodes(retrieved_nodes)
    
    print("使用 PrevNextNodePostprocessor 添加后一个节点后:")
    for i, node in enumerate(enhanced_nodes2):
        print(f"{i+1}. (相似度: {node.score:.2f}) {node.text}")
    
    print("\n" + "="*50 + "\n")
    
    # 使用 PrevNextNodePostprocessor 添加前后节点作为上下文
    processor3 = PrevNextNodePostprocessor(
        docstore=docstore,
        num_nodes=1,  # 获取1个相邻节点
        mode="both"  # 获取前后节点
    )
    enhanced_nodes3 = processor3.postprocess_nodes(retrieved_nodes)
    
    print("使用 PrevNextNodePostprocessor 添加前后节点后:")
    for i, node in enumerate(enhanced_nodes3):
        print(f"{i+1}. (相似度: {node.score:.2f}) {node.text}")


if __name__ == "__main__":
    main()