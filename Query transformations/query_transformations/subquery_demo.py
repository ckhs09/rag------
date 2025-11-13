"""
子问题查询转换演示

子问题查询转换是一种将复杂问题分解为多个相关子问题的技术，
每个子问题都可以独立查询和回答，最后将结果综合起来形成完整答案。
"""

import re

class SubQueryTransformer:
    """
    子问题查询转换器
    """
    
    def __init__(self):
        # 定义常见实体类型
        self.entity_types = {
            "技术术语": ["python", "java", "javascript", "react", "vue", "angular", "docker", "kubernetes"],
            "概念术语": ["机器学习", "深度学习", "人工智能", "区块链", "云计算", "大数据"],
            "工具产品": ["github", "gitlab", "jira", "jenkins", "nginx", "apache"],
            "编程概念": ["算法", "数据结构", "设计模式", "面向对象", "函数式编程"]
        }
    
    def identify_entities(self, query):
        """
        识别查询中的实体
        
        Args:
            query (str): 输入查询
            
        Returns:
            list: 识别出的实体列表
        """
        entities = []
        query_lower = query.lower()
        
        # 查找已知实体
        for entity_type, entity_list in self.entity_types.items():
            for entity in entity_list:
                if entity in query_lower:
                    entities.append({
                        "name": entity,
                        "type": entity_type,
                        "position": query_lower.find(entity)
                    })
        
        # 查找可能的专有名词（首字母大写的词）
        capitalized_words = re.findall(r'\b[A-Z][a-z]+\b', query)
        for word in capitalized_words:
            if word.lower() not in [e["name"] for e in entities]:
                entities.append({
                    "name": word,
                    "type": "专有名词",
                    "position": query.find(word)
                })
        
        # 按位置排序
        entities.sort(key=lambda x: x["position"])
        return entities
    
    def decompose_comparison_query(self, query):
        """
        分解比较类查询为子问题
        
        Args:
            query (str): 比较类查询
            
        Returns:
            list: 子问题列表
        """
        subqueries = []
        
        # 匹配"X和Y的区别/比较/不同"模式
        comparison_patterns = [
            r"(.+?)和(.+?)(?:区别|比较|不同|对比)",
            r"(.+?) vs (.+?)",
            r"(.+?) versus (.+?)",
            r"(.+?)与(.+?)(?:区别|比较|不同|对比)"
        ]
        
        for pattern in comparison_patterns:
            match = re.search(pattern, query)
            if match:
                item1, item2 = match.group(1).strip(), match.group(2).strip()
                subqueries.append(f"{item1}是什么?")
                subqueries.append(f"{item2}是什么?")
                subqueries.append(f"{item1}和{item2}有什么相同点?")
                subqueries.append(f"{item1}和{item2}有什么不同点?")
                subqueries.append(f"什么时候应该选择{item1}而不是{item2}?")
                subqueries.append(f"什么时候应该选择{item2}而不是{item1}?")
                return subqueries
        
        return [query]  # 如果不是比较查询，返回原查询
    
    def decompose_multi_entity_query(self, query):
        """
        分解多实体查询为子问题
        
        Args:
            query (str): 多实体查询
            
        Returns:
            list: 子问题列表
        """
        subqueries = []
        entities = self.identify_entities(query)
        
        if len(entities) <= 1:
            return [query]  # 单实体查询不需要分解
        
        # 为每个实体创建解释性子问题
        for entity in entities:
            subqueries.append(f"{entity['name']}是什么?")
        
        # 添加关系查询
        entity_names = [e['name'] for e in entities]
        subqueries.append(f"{'、'.join(entity_names)}之间有什么关系?")
        
        return subqueries
    
    def decompose_how_to_query(self, query):
        """
        分解"How to"类查询为子问题
        
        Args:
            query (str): How to类查询
            
        Returns:
            list: 子问题列表
        """
        subqueries = []
        
        # 提取动作和对象
        how_patterns = [
            r"如何(.+?)(.+)",
            r"怎样(.+?)(.+)",
            r"怎么(.+?)(.+)",
            r"how to (.+?) (.+)",
            r"how do i (.+?) (.+)"
        ]
        
        for pattern in how_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                action, obj = match.group(1).strip(), match.group(2).strip()
                # 移除可能的标点符号
                obj = obj.rstrip('?？')
                
                subqueries.append(f"{obj}是什么?")
                subqueries.append(f"为什么要{action}{obj}?")
                subqueries.append(f"{action}{obj}的前置条件是什么?")
                subqueries.append(f"{action}{obj}的具体步骤是什么?")
                subqueries.append(f"{action}{obj}需要注意什么?")
                subqueries.append(f"{action}{obj}有什么优缺点?")
                return subqueries
        
        # 如果没有匹配，使用通用分解
        obj = query.replace("如何", "").replace("怎样", "").replace("怎么", "").rstrip('?？')
        subqueries.append(f"{obj}是什么?")
        subqueries.append(f"{obj}的基本原理是什么?")
        subqueries.append(f"实现{obj}需要哪些步骤?")
        return subqueries
    
    def decompose_aspect_based_query(self, query):
        """
        基于方面的查询分解
        
        Args:
            query (str): 查询
            
        Returns:
            list: 子问题列表
        """
        subqueries = []
        
        # 定义常见方面关键词
        aspects = {
            "定义": ["定义", "是什么", "概念", "含义"],
            "原理": ["原理", "机制", "工作方式", "如何工作"],
            "优势": ["优势", "优点", "好处", "益处"],
            "劣势": ["劣势", "缺点", "不足", "问题"],
            "应用": ["应用", "用途", "使用", "运用"],
            "示例": ["示例", "例子", "实例", "举例"],
            "历史": ["历史", "起源", "发展", "演变"],
            "比较": ["比较", "区别", "对比", "相对于"]
        }
        
        # 检查查询中提到的方面
        mentioned_aspects = []
        for aspect, keywords in aspects.items():
            for keyword in keywords:
                if keyword in query:
                    mentioned_aspects.append(aspect)
                    break
        
        # 如果提到了特定方面，则针对这些方面生成子问题
        if mentioned_aspects:
            # 提取主题（移除方面关键词）
            topic = query
            for aspect, keywords in aspects.items():
                for keyword in keywords:
                    topic = topic.replace(keyword, "")
            topic = topic.strip(" ?？")
            
            for aspect in mentioned_aspects:
                subqueries.append(f"{topic}的{aspect}是什么?")
        else:
            # 否则生成通用方面的问题
            topic = query.rstrip("?？")
            for aspect in ["定义", "原理", "应用"]:
                subqueries.append(f"{topic}的{aspect}是什么?")
        
        return subqueries
    
    def transform_to_subqueries(self, query):
        """
        将查询转换为子问题列表
        
        Args:
            query (str): 输入查询
            
        Returns:
            dict: 包含原始查询和子问题列表的字典
        """
        # 判断查询类型并应用相应分解策略
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["区别", "比较", "不同", "对比", "vs", "versus"]):
            subqueries = self.decompose_comparison_query(query)
            query_type = "比较类查询"
        elif len(self.identify_entities(query)) > 1:
            subqueries = self.decompose_multi_entity_query(query)
            query_type = "多实体查询"
        elif any(word in query_lower for word in ["如何", "怎样", "怎么", "how to", "how do i"]):
            subqueries = self.decompose_how_to_query(query)
            query_type = "操作指导类查询"
        elif any(word in query_lower for word in ["定义", "原理", "优势", "劣势", "应用", "历史"]):
            subqueries = self.decompose_aspect_based_query(query)
            query_type = "多方面查询"
        else:
            # 通用分解方法
            subqueries = [query]
            query_type = "简单查询"
        
        return {
            "original_query": query,
            "query_type": query_type,
            "subqueries": subqueries
        }


def demo_subquery_transformation():
    """
    演示子问题查询转换
    """
    transformer = SubQueryTransformer()
    
    test_queries = [
        "Python和Java的区别",
        "Docker和Kubernetes的比较",
        "如何实现快速排序算法",
        "机器学习和深度学习的不同",
        "React、Vue和Angular的对比",
        "数据库索引的原理和优势",
        "什么是区块链技术"
    ]
    
    print("子问题查询转换演示")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n原始查询: {query}")
        
        # 转换为子问题
        result = transformer.transform_to_subqueries(query)
        
        print(f"查询类型: {result['query_type']}")
        print("分解的子问题:")
        
        for i, subquery in enumerate(result['subqueries'], 1):
            print(f"  {i}. {subquery}")
        
        print("-" * 50)


def interactive_demo():
    """
    交互式演示
    """
    transformer = SubQueryTransformer()
    
    print("\n交互式子问题查询转换演示")
    print("=" * 50)
    print("输入查询来查看如何将其分解为子问题，输入 'quit' 退出")
    
    while True:
        query = input("\n请输入查询: ").strip()
        
        if query.lower() in ['quit', 'exit', '退出']:
            print("再见!")
            break
        
        if not query:
            continue
        
        result = transformer.transform_to_subqueries(query)
        
        print(f"\n查询类型: {result['query_type']}")
        print("分解的子问题:")
        
        for i, subquery in enumerate(result['subqueries'], 1):
            print(f"  {i}. {subquery}")


if __name__ == "__main__":
    # 运行演示
    demo_subquery_transformation()
    
    # 如果需要交互式演示，取消下面一行的注释
    # interactive_demo()