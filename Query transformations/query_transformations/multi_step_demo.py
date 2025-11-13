"""
多步查询转换演示

多步查询转换是一种将复杂查询分解为一系列简单步骤的技术，
通过逐步推理来获取更准确的答案。
"""

class MultiStepQueryTransformer:
    """
    多步查询转换器
    """
    
    def __init__(self):
        pass
    
    def analyze_query_type(self, query):
        """
        分析查询类型
        
        Args:
            query (str): 输入查询
            
        Returns:
            str: 查询类型
        """
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in ["如何", "怎样", "怎么", "how to", "how do i"]):
            return "how_to"
        elif any(keyword in query_lower for keyword in ["是什么", "什么是", "what is", "definition"]):
            return "definition"
        elif any(keyword in query_lower for keyword in ["区别", "比较", "different", "comparison", "vs", "versus"]):
            return "comparison"
        elif any(keyword in query_lower for keyword in ["优势", "劣势", "优点", "缺点", "pros", "cons"]):
            return "pros_cons"
        elif any(keyword in query_lower for keyword in ["历史", "发展", "演变", "history", "evolution"]):
            return "history"
        else:
            return "general"
    
    def decompose_how_to_query(self, query):
        """
        分解"How to"类型的查询
        
        Args:
            query (str): "How to"类型查询
            
        Returns:
            list: 分解后的步骤
        """
        steps = []
        
        # 步骤1: 理解概念
        concept = query
        if query.startswith("如何"):
            concept = "什么是" + query[2:]
        elif query.lower().startswith("how to"):
            concept = "What is " + query[7:] + "?"
            
        steps.append({
            "step": 1,
            "query": concept,
            "type": "concept_understanding",
            "description": "理解基础概念"
        })
        
        # 步骤2: 识别前提条件
        steps.append({
            "step": 2,
            "query": f"{query}需要什么前提条件?",
            "type": "prerequisites",
            "description": "确定执行任务所需的准备工作"
        })
        
        # 步骤3: 列出主要步骤
        steps.append({
            "step": 3,
            "query": f"{query}的主要步骤有哪些?",
            "type": "main_steps",
            "description": "分解任务的核心步骤"
        })
        
        # 步骤4: 详细说明每一步
        steps.append({
            "step": 4,
            "query": f"{query}第一步详细说明",
            "type": "detailed_steps",
            "description": "详细解释每个步骤的操作方法"
        })
        
        # 步骤5: 注意事项和常见错误
        steps.append({
            "step": 5,
            "query": f"{query}需要注意什么?有哪些常见错误?",
            "type": "warnings",
            "description": "识别潜在问题和避免常见错误"
        })
        
        # 步骤6: 实际示例
        steps.append({
            "step": 6,
            "query": f"{query}的实际示例",
            "type": "examples",
            "description": "提供具体的实践案例"
        })
        
        return steps
    
    def decompose_definition_query(self, query):
        """
        分解定义类查询
        
        Args:
            query (str): 定义类查询
            
        Returns:
            list: 分解后的步骤
        """
        steps = []
        
        # 步骤1: 核心定义
        steps.append({
            "step": 1,
            "query": query,
            "type": "core_definition",
            "description": "获取概念的核心定义"
        })
        
        # 步骤2: 起源和背景
        subject = query
        if query.startswith("什么是"):
            subject = query[3:].strip('？?')
        elif query.lower().startswith("what is"):
            subject = query[7:].strip('？?')
            
        steps.append({
            "step": 2,
            "query": f"{subject}的起源和背景是什么?",
            "type": "origin_background",
            "description": "了解概念的历史和发展背景"
        })
        
        # 步骤3: 主要特征
        steps.append({
            "step": 3,
            "query": f"{subject}的主要特征有哪些?",
            "type": "characteristics",
            "description": "分析概念的关键特性和属性"
        })
        
        # 步骤4: 应用场景
        steps.append({
            "step": 4,
            "query": f"{subject}在哪些场景中应用?",
            "type": "applications",
            "description": "探索概念的实际应用场景"
        })
        
        # 步骤5: 相关概念
        steps.append({
            "step": 5,
            "query": f"{subject}相关概念有哪些?",
            "type": "related_concepts",
            "description": "了解与之相关的其他概念"
        })
        
        return steps
    
    def decompose_comparison_query(self, query):
        """
        分解比较类查询
        
        Args:
            query (str): 比较类查询
            
        Returns:
            list: 分解后的步骤
        """
        steps = []
        
        # 识别比较对象
        items = self._extract_comparison_items(query)
        
        # 步骤1: 第一个对象的介绍
        steps.append({
            "step": 1,
            "query": f"{items[0]}是什么?",
            "type": "item_introduction",
            "description": f"了解{items[0]}的基本概念"
        })
        
        # 步骤2: 第二个对象的介绍
        steps.append({
            "step": 2,
            "query": f"{items[1]}是什么?",
            "type": "item_introduction",
            "description": f"了解{items[1]}的基本概念"
        })
        
        # 步骤3: 核心差异
        steps.append({
            "step": 3,
            "query": f"{items[0]}和{items[1]}的核心差异是什么?",
            "type": "core_differences",
            "description": "分析两者最主要的区别"
        })
        
        # 步骤4: 优缺点对比
        steps.append({
            "step": 4,
            "query": f"{items[0]}和{items[1]}各自的优缺点是什么?",
            "type": "pros_cons",
            "description": "比较两者的优劣"
        })
        
        # 步骤5: 应用场景对比
        steps.append({
            "step": 5,
            "query": f"{items[0]}和{items[1]}在不同场景下的适用性?",
            "type": "use_cases",
            "description": "分析在不同情况下的选择建议"
        })
        
        return steps
    
    def _extract_comparison_items(self, query):
        """
        从比较类查询中提取比较对象
        
        Args:
            query (str): 比较类查询
            
        Returns:
            list: 比较对象列表
        """
        # 简单的关键词分割方法
        separators = ["和", "与", "vs", "versus", " compared to ", " compared with "]
        
        items = [query]
        for sep in separators:
            if sep in query:
                items = query.split(sep)
                break
        
        # 清理项目名称
        cleaned_items = []
        for item in items:
            # 移除比较相关的词汇
            item = item.replace("区别", "").replace("比较", "").replace("对比", "")
            item = item.strip('？? \t\n')
            if item:
                cleaned_items.append(item)
        
        # 如果只找到一个项目，尝试进一步拆分
        if len(cleaned_items) < 2:
            # 基于"和"、"与"等词之前的词语进行推测
            for sep in ["和", "与"]:
                if sep in query:
                    pos = query.find(sep)
                    item1 = query[:pos].strip()
                    item2 = query[pos+1:].replace("的区别", "").replace("的比较", "").strip()
                    cleaned_items = [item1, item2]
                    break
        
        return cleaned_items if len(cleaned_items) >= 2 else ["项目A", "项目B"]
    
    def transform_query_to_steps(self, query):
        """
        将查询转换为多步执行计划
        
        Args:
            query (str): 输入查询
            
        Returns:
            dict: 包含原始查询和执行步骤的字典
        """
        query_type = self.analyze_query_type(query)
        
        if query_type == "how_to":
            steps = self.decompose_how_to_query(query)
        elif query_type == "definition":
            steps = self.decompose_definition_query(query)
        elif query_type == "comparison":
            steps = self.decompose_comparison_query(query)
        else:
            # 对于一般查询，使用通用分解方法
            steps = self._decompose_general_query(query)
        
        return {
            "original_query": query,
            "query_type": query_type,
            "steps": steps
        }
    
    def _decompose_general_query(self, query):
        """
        分解一般查询
        
        Args:
            query (str): 一般查询
            
        Returns:
            list: 分解后的步骤
        """
        steps = []
        
        # 步骤1: 定义和概念
        steps.append({
            "step": 1,
            "query": f"什么是{query}?" if not query.startswith("什么是") else query,
            "type": "definition",
            "description": "理解基本概念"
        })
        
        # 步骤2: 重要性或意义
        steps.append({
            "step": 2,
            "query": f"为什么{query}很重要?",
            "type": "importance",
            "description": "了解重要性和价值"
        })
        
        # 步骤3: 实际应用
        steps.append({
            "step": 3,
            "query": f"{query}如何应用在实际中?",
            "type": "application",
            "description": "探索实际应用场景"
        })
        
        # 步骤4: 发展趋势
        steps.append({
            "step": 4,
            "query": f"{query}的发展趋势是什么?",
            "type": "trends",
            "description": "了解未来发展方向"
        })
        
        return steps


def demo_multi_step_transformation():
    """
    演示多步查询转换
    """
    transformer = MultiStepQueryTransformer()
    
    test_queries = [
        "如何实现快速排序算法",
        "什么是机器学习",
        "React和Vue的区别",
        "区块链技术的优势和劣势"
    ]
    
    print("多步查询转换演示")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n原始查询: {query}")
        
        # 分析查询类型
        query_type = transformer.analyze_query_type(query)
        type_names = {
            "how_to": "操作指导型",
            "definition": "定义解释型",
            "comparison": "比较分析型",
            "pros_cons": "优劣分析型",
            "history": "历史发展型",
            "general": "一般查询型"
        }
        print(f"查询类型: {type_names.get(query_type, '未知类型')}")
        
        # 转换为多步执行计划
        result = transformer.transform_query_to_steps(query)
        
        print("执行步骤:")
        for step in result['steps']:
            print(f"  步骤 {step['step']}: {step['query']}")
            print(f"    类型: {step['type']}")
            print(f"    说明: {step['description']}")
            print()
        
        print("-" * 50)


if __name__ == "__main__":
    demo_multi_step_transformation()