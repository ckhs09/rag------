import re

class QuestionsAnsweredExtractor:
    """
    问答抽取器：识别文档中涉及的问题和对应答案
    """
    
    def __init__(self):
        # 匹配常见问答格式的正则表达式
        self.qa_patterns = [
            r'(Q:|Question:|问题:)\s*(.*?)\n*(A:|Answer:|答:)\s*(.*?)(?=\n\n|$)',
            r'(Q:|Question:|问题:)\s*(.*?)\n(.*?)(?=\n\n|$)',
            r'\n(.*?)\s*\?\s*\n(.*?)(?=\n\n|$)'
        ]
    
    def extract(self, document_content):
        """
        从文档中提取问答对
        
        Args:
            document_content (str): 文档内容
            
        Returns:
            list: 包含问答对的列表
        """
        qa_pairs = []
        
        # 尝试使用不同模式匹配问答对
        for pattern in self.qa_patterns:
            matches = re.findall(pattern, document_content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                if len(match) >= 4:  # 完整的问答格式
                    question = match[1].strip()
                    answer = match[3].strip()
                elif len(match) >= 3:  # 简化的问答格式
                    question = match[1].strip()
                    answer = match[2].strip()
                else:
                    continue
                    
                if question and answer:
                    qa_pairs.append({
                        'question': question,
                        'answer': answer
                    })
        
        # 如果没有找到明确的问答对，尝试按段落分割
        if not qa_pairs:
            paragraphs = document_content.split('\n\n')
            for i, para in enumerate(paragraphs):
                if '?' in para and len(para) > 20:
                    # 简单启发式：包含问号且较长的段落可能是问题
                    # 下一个段落可能是答案
                    if i + 1 < len(paragraphs):
                        qa_pairs.append({
                            'question': para.strip(),
                            'answer': paragraphs[i + 1].strip()
                        })
        
        return qa_pairs


if __name__ == "__main__":
    # 示例用法
    extractor = QuestionsAnsweredExtractor()
    document = """Q: 什么是人工智能?
A: 人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。

Question: 机器学习是什么？
Answer: 机器学习是人工智能的一个子领域，它使计算机能够从数据中学习并做出决策或预测，而无需明确编程来执行特定任务。

什么是深度学习？
深度学习是机器学习的一个分支，它模拟人脑的神经网络结构，通过多层次的数据处理来学习数据的特征表示。"""
    
    qa_pairs = extractor.extract(document)
    print("提取的问答对:")
    for i, qa in enumerate(qa_pairs, 1):
        print(f"{i}. 问: {qa['question']}")
        print(f"   答: {qa['answer']}")
        print()