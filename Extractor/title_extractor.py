import re

class TitleExtractor:
    """
    标题抽取器：从文档中提取标题信息
    """
    
    def __init__(self):
        # 匹配不同级别的标题格式
        self.title_patterns = {
            'markdown': [
                (1, r'^#\s+(.*)'),      # H1
                (2, r'^##\s+(.*)'),     # H2
                (3, r'^###\s+(.*)'),    # H3
                (4, r'^####\s+(.*)'),   # H4
                (5, r'^#####\s+(.*)'),  # H5
                (6, r'^######\s+(.*)')  # H6
            ],
            'html': [
                (1, r'<h1[^>]*>(.*?)</h1>'),
                (2, r'<h2[^>]*>(.*?)</h2>'),
                (3, r'<h3[^>]*>(.*?)</h3>'),
                (4, r'<h4[^>]*>(.*?)</h4>'),
                (5, r'<h5[^>]*>(.*?)</h5>'),
                (6, r'<h6[^>]*>(.*?)</h6>')
            ],
            'numbered': [
                (1, r'^(\d+\.)+\s+(.*)'),          # 1.1 标题
                (2, r'^(\d+\.\d+\.)+\s+(.*)'),     # 1.1.1 标题
            ],
            'plain_text': [
                (1, r'^([A-Z][^.!?]*?)$'),         # 全大写行作为一级标题
                (2, r'^(\w[^.!?:]{20,})$')         # 长句子行作为二级标题
            ]
        }
    
    def extract(self, document_content):
        """
        从文档中提取标题
        
        Args:
            document_content (str): 文档内容
            
        Returns:
            list: 包含标题信息的列表
        """
        titles = []
        lines = document_content.split('\n')
        
        line_num = 0
        for line in lines:
            line_num += 1
            line_stripped = line.strip()
            
            # 检查各种格式的标题
            for format_type, patterns in self.title_patterns.items():
                for level, pattern in patterns:
                    match = re.match(pattern, line_stripped, re.IGNORECASE)
                    if match:
                        title_text = match.group(1).strip()
                        # 对于HTML格式，可能需要进一步清理标签
                        if format_type == 'html':
                            title_text = re.sub(r'<[^>]+>', '', title_text).strip()
                        
                        titles.append({
                            'level': level,
                            'text': title_text,
                            'format': format_type,
                            'line_number': line_num
                        })
                        break  # 找到匹配就跳出循环
        
        # 按行号排序
        titles.sort(key=lambda x: x['line_number'])
        return titles


if __name__ == "__main__":
    # 示例用法
    extractor = TitleExtractor()
    document = """# 人工智能简介

## 什么是人工智能

人工智能是计算机科学的一个重要分支。

### 人工智能的发展历史

人工智能的概念最早由约翰·麦卡锡在1956年提出。

## 机器学习

### 监督学习

监督学习是机器学习中最常见的类型之一。

# 深度学习

## 神经网络基础

神经网络是深度学习的基本组成单元。"""
    
    titles = extractor.extract(document)
    print("提取的标题:")
    for title in titles:
        print(f"级别 {title['level']} [{title['format']}]: {title['text']} (第{title['line_number']}行)")