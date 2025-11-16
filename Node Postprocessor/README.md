# Node Postprocessor 示例项目

这个项目包含了几个演示 LlamaIndex 中不同类型 Node Postprocessor 的脚本。

## Node Postprocessor 简介

Node Postprocessor 是 LlamaIndex 中用于优化检索结果的重要组件。它们在检索节点之后、响应合成之前对节点进行处理，以提高检索结果的相关性和质量。

## 包含的示例

### 1. SimilarityPostprocessor (相似度过滤器)
- 文件: [similarity_postprocessor_demo.py](similarity_postprocessor_demo.py)
- 功能: 根据相似度分数过滤掉低相关性的检索结果
- 使用场景: 设置相似度阈值，过滤低于阈值的节点

### 2. KeywordNodePostprocessor (关键词处理器)
- 文件: [keyword_node_postprocessor_demo.py](keyword_node_postprocessor_demo.py)
- 功能: 根据关键词匹配排除或包含特定内容的节点
- 使用场景: 通过关键词控制哪些节点应该被包含或排除

### 3. PrevNextNodePostprocessor (前后节点处理器)
- 文件: [prev_next_node_postprocessor_demo.py](prev_next_node_postprocessor_demo.py)
- 功能: 为检索到的节点添加相邻节点的上下文信息
- 使用场景: 避免因文本分割造成的语义不完整问题

### 4. LongContextReorder (长上下文重排序器)
- 文件: [long_context_reorder_demo.py](long_context_reorder_demo.py)
- 功能: 对检索结果按照相关性进行重新排序
- 使用场景: 利用LLM对首尾内容关注度更高的特性，优化结果顺序

## 如何运行示例

1. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

2. 运行各个示例脚本:
   ```
   python similarity_postprocessor_demo.py
   python keyword_node_postprocessor_demo.py
   python prev_next_node_postprocessor_demo.py
   python long_context_reorder_demo.py
   ```

## 学习建议

建议按照以下顺序学习这些示例：

1. 首先运行每个脚本，观察输出结果
2. 查看代码中对每种 Postprocessor 的使用方法
3. 修改参数值，观察效果变化
4. 尝试结合多种 Postprocessor 使用

通过这些示例，您可以深入了解 Node Postprocessor 在 RAG 应用中的作用和使用方法。