# 查询转换 (Query Transformations) 示例

查询转换（Query Transformations）是大语言模型应用中的重要技术，特别是在检索增强生成（RAG）系统中。它是在检索之前对用户输入的查询进行处理和转换，以提高检索效果和最终答案的质量。

## 四种主要的查询转换类型

### 1. 查询重写 (Reformulate)
将输入问题转换为更有利于嵌入的问题，以提高召回知识的精确性。

示例：
- 原始查询："what's python"
- 重写后："what is python?"

### 2. 查询扩展 (Expand)
对输入问题进行语义丰富与扩展，有利于从数据中生成更全面与更准确的答案。

示例：
- 原始查询："机器学习算法"
- 扩展后：
  - "机器学习算法 定义"
  - "机器学习算法 应用"
  - "机器学习算法 例子"

### 3. 查询分解 (Decompose)
将初始查询分解成不同的多个子问题，分别查询，最后合成答案。

示例：
- 原始查询："Python和Java的区别"
- 分解后：
  - "Python是什么？"
  - "Java是什么？"
  - "Python和Java有什么不同？"

### 4. 多步查询 (Step Back)
将初始查询分解成可以多步完成的子查询，通过分步查询得出答案。

示例：
- 原始查询："如何实现快速排序算法"
- 抽象问题："什么是快速排序算法的概念？"
- 执行步骤：
  1. 理解快速排序的基础概念
  2. 识别实现快速排序的关键要素
  3. 学习快速排序的具体实现步骤
  4. 查看快速排序的示例

## 文件结构

```
query_transformations/
├── main_demo.py              # 主演示程序
├── reformulate/
│   └── reformulate_query.py  # 查询重写示例
├── expand/
│   └── expand_query.py       # 查询扩展示例
├── decompose/
│   └── decompose_query.py    # 查询分解示例
└── step_back/
    └── step_back_query.py    # 多步查询示例
```

## 运行示例

```bash
# 运行主演示程序
python query_transformations/main_demo.py

# 单独运行各个示例
python query_transformations/reformulate/reformulate_query.py
python query_transformations/expand/expand_query.py
python query_transformations/decompose/decompose_query.py
python query_transformations/step_back/step_back_query.py
```

## 应用场景

1. **搜索引擎优化**：改进用户查询以获得更相关的结果
2. **问答系统**：将复杂问题分解为简单问题以提高回答准确性
3. **推荐系统**：扩展用户查询以发现更多相关内容
4. **知识图谱查询**：将自然语言查询转换为结构化查询

## 实现要点

1. **查询重写**：关注语法规范化和领域适配
2. **查询扩展**：使用同义词、上下文和假设文档增强查询
3. **查询分解**：识别查询中的多个实体或方面并分别处理
4. **多步查询**：从抽象概念到具体实现的逐步推理

这些技术可以单独使用，也可以组合使用，以适应不同的应用场景和需求。