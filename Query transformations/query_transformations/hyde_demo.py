"""
HyDE (Hypothetical Document Embeddings) 查询转换示例

HyDE是一种查询扩展技术，它通过生成假设的理想答案来改进查询表示，
然后使用该假设答案的嵌入向量来检索真实文档。
"""

import random

class HyDEQueryTransformer:
    """
    HyDE查询转换器
    """
    
    def __init__(self):
        # 预定义的一些查询及其假设答案模板
        self.hypothetical_answers = {
            "什么是机器学习": """机器学习是人工智能的一个分支，它使计算机能够在不被明确编程的情况下从数据中学习。
            它通过算法解析数据，从中学习，并基于学习到的知识对新数据做出决策或预测。
            机器学习广泛应用于图像识别、语音识别、自然语言处理、推荐系统等领域。""",
            
            "如何实现快速排序": """快速排序是一种高效的排序算法，采用分治法策略。
            实现步骤：
            1. 选择一个元素作为基准（pivot）
            2. 重新排列数组，使得比基准小的元素在基准前面，比基准大的在后面
            3. 递归地对基准前后的子数组进行快速排序
            时间复杂度平均为O(n log n)，最坏情况下为O(n²)。""",
            
            "python装饰器的作用": """Python装饰器是一种设计模式，允许用户在不修改原函数代码的情况下，
            给函数增加新的功能。装饰器本质上是一个接受函数作为参数并返回函数的高阶函数。
            常用于日志记录、性能测试、事务处理、缓存等场景。""",
            
            "数据库索引的原理": """数据库索引是一种数据结构，用于提高数据库表数据检索的速度。
            常见的索引类型包括B树、B+树、哈希索引等。
            索引虽然能加速查询，但会减慢数据插入和更新的速度，并占用额外存储空间。""",
            
            "什么是区块链": """区块链是一种分布式数据库技术，由一系列按时间顺序链接的数据块组成。
            每个区块包含一批交易信息，并通过密码学方法与前一个区块相连接。
            区块链具有去中心化、不可篡改、透明可追溯等特点，广泛应用于加密货币等领域。"""
        }
    
    def generate_hypothetical_document(self, query):
        """
        为给定查询生成假设的理想答案文档
        
        Args:
            query (str): 输入查询
            
        Returns:
            str: 假设的答案文档
        """
        # 精确匹配预定义的查询
        for key, answer in self.hypothetical_answers.items():
            if key in query or query in key:
                return answer
        
        # 模糊匹配
        query_lower = query.lower()
        for key, answer in self.hypothetical_answers.items():
            if any(word in query_lower for word in key.lower().split()):
                return answer
        
        # 如果没有匹配项，生成一个通用的假设文档
        return self._generate_generic_hypothetical_document(query)
    
    def _generate_generic_hypothetical_document(self, query):
        """
        生成通用的假设文档
        
        Args:
            query (str): 输入查询
            
        Returns:
            str: 通用假设文档
        """
        # 基于查询类型生成假设文档
        if query.startswith("什么是") or query.startswith("what is"):
            subject = query[3:].strip('？?')
            return f"{subject}是一个重要的概念，在相关领域中发挥着重要作用。它有着明确的定义和特征，并且有广泛的应用场景。"
        
        elif query.startswith("如何") or "how to" in query.lower():
            action = query[2:].strip('？?')
            return f"执行{action}需要按照一定的步骤进行。首先要做准备工作，然后按照流程操作，最后检查结果。在操作过程中需要注意安全和质量控制。"
        
        elif "区别" in query or "比较" in query or "difference" in query.lower():
            items = query.replace("和", " ").replace("与", " ").split()
            return f"{items[0]}和{items[1]}是两个相关但不同的概念。它们各自有不同的特点、用途和适用场景。了解它们的异同有助于正确选择和使用。"
        
        else:
            # 通用模板
            return f"关于'{query}'这个问题，可以从多个角度来分析和理解。它涉及到相关的理论基础、实践应用以及发展趋势等方面的内容。"
    
    def extract_key_phrases(self, document):
        """
        从假设文档中提取关键短语
        
        Args:
            document (str): 假设文档
            
        Returns:
            list: 关键短语列表
        """
        # 简单的句子分割和关键短语提取
        sentences = document.strip().split('。')
        key_phrases = []
        
        for sentence in sentences[:3]:  # 只处理前3个句子
            sentence = sentence.strip()
            if sentence:
                words = sentence.split()
                # 提取前5个词组成的短语
                phrase = ''.join(words[:5]) if len(words) >= 5 else ''.join(words)
                if phrase and len(phrase) > 3:  # 过滤太短的短语
                    key_phrases.append(phrase)
        
        return key_phrases
    
    def expand_query_with_hyde(self, query):
        """
        使用HyDE方法扩展查询
        
        Args:
            query (str): 原始查询
            
        Returns:
            dict: 包含假设文档、关键短语和扩展查询的字典
        """
        # 生成假设文档
        hypo_doc = self.generate_hypothetical_document(query)
        
        # 提取关键短语
        key_phrases = self.extract_key_phrases(hypo_doc)
        
        # 构建扩展查询
        expanded_queries = [query]  # 包含原始查询
        
        # 基于关键短语的扩展
        for phrase in key_phrases[:3]:  # 最多使用3个关键短语
            expanded_queries.append(f"{query} {phrase}")
        
        # 添加上下文扩展
        expanded_queries.append(f"{query} 定义和应用")
        expanded_queries.append(f"{query} 详细介绍")
        
        return {
            "original_query": query,
            "hypothetical_document": hypo_doc,
            "key_phrases": key_phrases,
            "expanded_queries": expanded_queries
        }

def demo_hyde_transformation():
    """
    演示HyDE查询转换
    """
    transformer = HyDEQueryTransformer()
    
    test_queries = [
        "什么是机器学习",
        "如何实现快速排序",
        "python装饰器的作用",
        "数据库索引的原理",
        "区块链技术的特点",
        "什么是深度学习"
    ]
    
    print("HyDE (Hypothetical Document Embeddings) 查询转换演示")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n原始查询: {query}")
        
        # 执行HyDE转换
        result = transformer.expand_query_with_hyde(query)
        
        print(f"假设文档:\n{result['hypothetical_document']}\n")
        
        print("关键短语:")
        for i, phrase in enumerate(result['key_phrases'], 1):
            print(f"  {i}. {phrase}")
        
        print("\n扩展查询:")
        for i, expanded in enumerate(result['expanded_queries'], 1):
            print(f"  {i}. {expanded}")
        
        print("-" * 60)

if __name__ == "__main__":
    demo_hyde_transformation()