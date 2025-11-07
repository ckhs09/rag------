# 元数据抽取器示例

这个项目包含了几个典型的元数据抽取器实现及其使用示例。

## 抽取器类型

### 1. 摘要抽取器 (SummaryExtractor)
从文档内容中提取或生成摘要信息，帮助快速了解文档的核心要点。

### 2. 问答抽取器 (QuestionsAnsweredExtractor)
识别文档中涉及的问题和对应答案，提取FAQ类型的问答对信息。

### 3. 标题抽取器 (TitleExtractor)
从文档中提取标题信息，识别不同层级的标题结构。

## 文件说明

- [summary_extractor.py](file:///c%3A/Users/m1950/Desktop/rag/Extractor/summary_extractor.py) - 摘要抽取器实现
- [questions_answered_extractor.py](file:///c%3A/Users/m1950/Desktop/rag/Extractor/questions_answered_extractor.py) - 问答抽取器实现
- [title_extractor.py](file:///c%3A/Users/m1950/Desktop/rag/Extractor/title_extractor.py) - 标题抽取器实现
- [demo.py](file:///c%3A/Users/m1950/Desktop/rag/Extractor/demo.py) - 演示所有抽取器的使用
- [README.md](file:///c%3A/Users/m1950/Desktop/rag/Extractor/README.md) - 项目说明文件

## 运行示例

```bash
python demo.py
```

## 使用方法

每个抽取器都可以单独使用：

```python
# 摘要抽取器
from summary_extractor import SummaryExtractor
extractor = SummaryExtractor()
summary = extractor.extract(document_content)

# 问答抽取器
from questions_answered_extractor import QuestionsAnsweredExtractor
extractor = QuestionsAnsweredExtractor()
qa_pairs = extractor.extract(document_content)

# 标题抽取器
from title_extractor import TitleExtractor
extractor = TitleExtractor()
titles = extractor.extract(document_content)
```