"""
多模态文档处理演示程序
"""

from multimodal_processor import MultimodalProcessor
from advanced_multimodal_processor import AdvancedMultimodalProcessor


def basic_demo():
    """基础多模态处理演示"""
    print("=" * 50)
    print("基础多模态文档处理演示")
    print("=" * 50)
    
    # 创建处理器实例
    processor = MultimodalProcessor()
    
    # 处理示例文档
    processor.process_document("sample_document.txt")
    
    # 查询示例
    queries = [
        "多模态文档处理的核心组件有哪些？",
        "技术优势是什么？",
        "应用场景包括哪些？"
    ]
    
    for query in queries:
        print(f"\n查询: {query}")
        results = processor.query(query)
        
        for i, result in enumerate(results, 1):
            print(f"  结果 {i}:")
            print(f"    类型: {result['element'].element_type}")
            print(f"    内容: {result['element'].content}")
            print(f"    元数据: {result['element'].metadata}")


def advanced_demo():
    """高级多模态处理演示"""
    print("\n" + "=" * 50)
    print("高级多模态文档处理演示")
    print("=" * 50)
    
    # 创建高级处理器实例
    processor = AdvancedMultimodalProcessor()
    
    # 处理示例文档
    processor.process_document("sample_document.txt")
    
    # 查询示例
    queries = [
        "关键技术组成有哪些？",
        "文档解析层包含什么功能？",
        "应用场景包括哪些？"
    ]
    
    for query in queries:
        print(f"\n查询: {query}")
        results = processor.query(query)
        
        for i, result in enumerate(results, 1):
            print(f"  结果 {i}:")
            print(f"    类型: {result['type']}")
            print(f"    内容: {result['content']}")
            print(f"    元数据: {result['metadata']}")


if __name__ == "__main__":
    # 运行基础演示
    basic_demo()
    
    # 运行高级演示
    advanced_demo()
    
    print("\n" + "=" * 50)
    print("演示完成")
    print("=" * 50)