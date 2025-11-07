class SummaryExtractor:
    """
    摘要抽取器：从文档内容中提取或生成摘要信息
    """
    
    def __init__(self, max_length=150):
        self.max_length = max_length
    
    def extract(self, document_content):
        """
        从文档中提取摘要
        
        Args:
            document_content (str): 文档内容
            
        Returns:
            str: 文档摘要
        """
        # 简单实现：截取前max_length个字符作为摘要
        # 实际应用中可能会使用更复杂的算法或模型
        if len(document_content) <= self.max_length:
            return document_content
        else:
            # 找到合适的句子边界
            summary = document_content[:self.max_length]
            last_period = summary.rfind('.')
            if last_period > 0:
                summary = summary[:last_period + 1]
            return summary


if __name__ == "__main__":
    # 示例用法
    extractor = SummaryExtractor()
    document = "这是一个示例文档。它包含一些文本内容，用于演示如何使用摘要抽取器。摘要抽取器可以从较长的文档中提取关键信息，生成简洁的摘要。这对于快速了解文档内容非常有用。"
    summary = extractor.extract(document)
    print(f"原文: {document}")
    print(f"摘要: {summary}")