# 简单的RAG应用

本项目演示了一个最基本的RAG（检索增强生成）应用的开发过程。

## 项目结构

```
rag/
├── README.md
├── requirements.txt
├── data/
│   └── sample.txt
├── src/
│   ├── document_loader.py
│   ├── rag_app.py
│   └── main.py
└── tests/
    └── test_rag.py
```

## 技术栈

- Python 3.8+
- LangChain - 构建RAG应用的框架
- FAISS - 向量存储
- OpenAI API / 阿里百炼 - 大语言模型API