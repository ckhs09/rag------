# 简单的RAG应用

本项目演示了一个基本的RAG（检索增强生成）应用的开发过程。项目展示了如何结合文档检索与大语言模型生成回答的基本流程，解决传统大模型在知识更新和特定领域知识支持上的局限性。

## 项目特点

- 支持多种文档加载方式（本地文件、网页、数据库等）
- 实现多种文本分割策略（递归字符分割、语义分割等）
- 集成多种向量存储和检索方案（FAISS、Chroma、Elasticsearch等）
- 提供多种检索算法（关键词检索、向量检索、混合检索等）
- 支持多种大语言模型接口（OpenAI、Ollama等）

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
│   ├── interactive_query.py
│   └── main.py
├── 4.3/                      # 相似度算法实现
│   └── similarity_algorithms.py
├── Data pipeline/             # 数据处理管道
│   ├── csv_analysis_pipeline.py
│   ├── file_pipeline.py
│   ├── flexible_pipeline.py
│   └── json_pipeline.py
├── Extractor/                 # 信息提取器
│   ├── questions_answered_extractor.py
│   ├── summary_extractor.py
│   └── title_extractor.py
├── Retriever/                 # 检索器实现
│   └── retrievers/
├── Vector Index/              # 向量索引实现
│   ├── keyword_table_index.py
│   ├── knowledge_graph_index.py
│   ├── summary_index.py
│   └── tree_index.py
├── data loading/              # 数据加载模块
│   └── data_loading/
└── tests/
    └── test_rag.py
```

## 核心模块

### 文档加载 (Document Loading)
支持从多种来源加载数据:
- 本地文档 (TXT, CSV, JSON等)
- 网络内容 (网页抓取)
- 数据库 (SQL, NoSQL)
- 云存储 (S3, Google Cloud Storage等)
- 社交媒体平台

### 文本分割 (Text Splitting)
提供多种文本分割策略:
- 基于字符的递归分割
- 基于语义的分割
- 自定义规则分割

### 向量索引 (Vector Indexing)
实现了多种向量索引方式:
- FAISS向量存储
- Chroma向量数据库
- 关键词表索引
- 摘要索引
- 树形索引
- 知识图谱索引

### 检索器 (Retrievers)
支持多种检索算法:
- 关键词检索 (BM25)
- 向量相似度检索 (KNN)
- 混合检索 (RRF)
- 重排序器

### 提取器 (Extractors)
从文档中提取特定信息:
- 标题提取
- 内容摘要
- 问题回答对提取

## 技术栈

- Python 3.8+
- LangChain - 构建RAG应用的框架
- FAISS/Chroma - 向量存储
- OpenAI API/Ollama - 大语言模型API
- Elasticsearch - 搜索引擎
- Ollama - 本地大语言模型部署

## 快速开始

1. 安装依赖:
```bash
pip install -r requirements.txt
```

2. 配置环境变量:
```bash
export OPENAI_API_KEY=your-api-key
```

3. 运行主程序:
```bash
python src/main.py
```

## 使用说明

项目提供了两种运行模式:
1. 文档处理和向量存储模式 - 处理文档并创建向量索引
2. 交互式问答模式 - 基于已有向量索引进行问答交互

在交互式问答模式中，系统会连接到Chroma向量数据库，并使用Ollama提供的大语言模型生成答案。