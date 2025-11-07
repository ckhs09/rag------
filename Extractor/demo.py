"""
元数据抽取器演示文件
展示如何使用各种抽取器处理文档
"""

from summary_extractor import SummaryExtractor
from questions_answered_extractor import QuestionsAnsweredExtractor
from title_extractor import TitleExtractor

def main():
    # 示例文档内容
    sample_document = """# 人工智能与机器学习指南

## 什么是人工智能

人工智能（Artificial Intelligence, AI）是计算机科学的一个分支，它企图了解智能的实质，
并生产出一种新的能以人类智能相似的方式做出反应的智能机器。

该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。

### 人工智能的发展历史

人工智能的概念最早由约翰·麦卡锡在1956年提出。自那时起，AI经历了多次起伏，
目前正处于高速发展阶段。

## 机器学习

机器学习（Machine Learning, ML）是人工智能的一个子领域，它使计算机能够从数据中学习
并做出决策或预测，而无需明确编程来执行特定任务。

Q: 机器学习与人工智能有什么区别？
A: 人工智能是更广泛的概念，而机器学习是实现人工智能的一种方法。

### 监督学习

监督学习是机器学习中最常见的类型之一，它使用标记的数据集来训练算法，
使其能够对未见过的数据进行预测。

什么是深度学习？
深度学习是机器学习的一个分支，它模拟人脑的神经网络结构，
通过多层次的数据处理来学习数据的特征表示。

## 应用领域

人工智能在医疗、金融、交通、教育等领域都有广泛应用。

### 医疗领域

人工智能在医疗影像分析、疾病预测、个性化治疗等方面发挥重要作用。

## 未来展望

随着计算能力的提升和数据量的增加，人工智能技术将继续快速发展，
为人类社会带来更多便利和创新。"""

    print("=" * 60)
    print("元数据抽取器演示")
    print("=" * 60)
    
    # 1. 使用摘要抽取器
    print("\n1. 摘要抽取器结果:")
    print("-" * 30)
    summary_extractor = SummaryExtractor(max_length=100)
    summary = summary_extractor.extract(sample_document)
    print(f"文档摘要: {summary}")
    
    # 2. 使用问答抽取器
    print("\n2. 问答抽取器结果:")
    print("-" * 30)
    qa_extractor = QuestionsAnsweredExtractor()
    qa_pairs = qa_extractor.extract(sample_document)
    if qa_pairs:
        for i, qa in enumerate(qa_pairs, 1):
            print(f"问答对 {i}:")
            print(f"  问: {qa['question']}")
            print(f"  答: {qa['answer']}")
    else:
        print("未找到问答对")
    
    # 3. 使用标题抽取器
    print("\n3. 标题抽取器结果:")
    print("-" * 30)
    title_extractor = TitleExtractor()
    titles = title_extractor.extract(sample_document)
    if titles:
        for title in titles:
            indent = "  " * (title['level'] - 1)
            print(f"{indent}级别 {title['level']} [{title['format']}]: {title['text']}")
    else:
        print("未找到标题")

if __name__ == "__main__":
    main()