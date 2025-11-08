#!/usr/bin/env python3
"""
灵活的数据管道框架示例
演示了一个更通用和灵活的数据管道实现，支持异步处理和条件分支
"""

from typing import List, Any, Callable, Optional
from abc import ABC, abstractmethod
import asyncio
import time


class DataPipeline:
    """灵活的数据管道类"""
    
    def __init__(self):
        self.steps: List[PipelineStep] = []
    
    def add_step(self, step):
        """向管道添加步骤"""
        self.steps.append(step)
        return self  # 支持链式调用
    
    def process(self, data):
        """顺序处理数据"""
        result = data
        for step in self.steps:
            print(f"执行步骤: {step.name}")
            result = step.execute(result)
        return result
    
    async def process_async(self, data):
        """异步处理数据"""
        result = data
        for step in self.steps:
            print(f"异步执行步骤: {step.name}")
            result = await step.execute_async(result)
        return result


class PipelineStep(ABC):
    """管道步骤抽象基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def execute(self, data: Any) -> Any:
        """执行步骤"""
        pass
    
    async def execute_async(self, data: Any) -> Any:
        """异步执行步骤"""
        # 默认实现为同步执行
        return self.execute(data)


class DataSourceStep(PipelineStep):
    """数据源步骤"""
    
    def __init__(self, name: str, source_func: Callable):
        super().__init__(name)
        self.source_func = source_func
    
    def execute(self, _):
        """从数据源获取数据"""
        return self.source_func()


class DataTransformerStep(PipelineStep):
    """数据转换步骤"""
    
    def __init__(self, name: str, transform_func: Callable):
        super().__init__(name)
        self.transform_func = transform_func
    
    def execute(self, data: Any) -> Any:
        """转换数据"""
        return self.transform_func(data)


class DataFilterStep(PipelineStep):
    """数据过滤步骤"""
    
    def __init__(self, name: str, filter_func: Callable):
        super().__init__(name)
        self.filter_func = filter_func
    
    def execute(self, data: List[Any]) -> List[Any]:
        """过滤数据"""
        if isinstance(data, list):
            return [item for item in data if self.filter_func(item)]
        return data


class DataAggregatorStep(PipelineStep):
    """数据聚合步骤"""
    
    def __init__(self, name: str, agg_func: Callable):
        super().__init__(name)
        self.agg_func = agg_func
    
    def execute(self, data: List[Any]) -> Any:
        """聚合数据"""
        return self.agg_func(data)


class ConditionalBranchStep(PipelineStep):
    """条件分支步骤"""
    
    def __init__(self, name: str, condition_func: Callable, 
                 true_branch: 'DataPipeline', false_branch: Optional['DataPipeline'] = None):
        super().__init__(name)
        self.condition_func = condition_func
        self.true_branch = true_branch
        self.false_branch = false_branch
    
    def execute(self, data: Any) -> Any:
        """根据条件执行不同分支"""
        if self.condition_func(data):
            print(f"条件为真，执行分支: {self.true_branch}")
            return self.true_branch.process(data)
        elif self.false_branch:
            print(f"条件为假，执行分支: {self.false_branch}")
            return self.false_branch.process(data)
        else:
            return data


class DelayStep(PipelineStep):
    """延迟步骤（模拟耗时操作）"""
    
    def __init__(self, name: str, delay_seconds: int):
        super().__init__(name)
        self.delay_seconds = delay_seconds
    
    def execute(self, data: Any) -> Any:
        """延迟执行"""
        print(f"步骤 '{self.name}' 延迟 {self.delay_seconds} 秒...")
        time.sleep(self.delay_seconds)
        return data
    
    async def execute_async(self, data: Any) -> Any:
        """异步延迟执行"""
        print(f"步骤 '{self.name}' 异步延迟 {self.delay_seconds} 秒...")
        await asyncio.sleep(self.delay_seconds)
        return data


# 示例数据源函数
def get_sample_data():
    """获取示例数据"""
    return [
        {'name': '产品A', 'category': '电子', 'price': 100, 'stock': 50},
        {'name': '产品B', 'category': '服装', 'price': 50, 'stock': 100},
        {'name': '产品C', 'category': '电子', 'price': 200, 'stock': 30},
        {'name': '产品D', 'category': '家居', 'price': 80, 'stock': 70},
        {'name': '产品E', 'category': '服装', 'price': 120, 'stock': 60},
    ]


# 示例转换函数
def add_discount(data):
    """为高价值商品添加折扣标记"""
    for item in data:
        item['has_discount'] = item['price'] > 100
    return data


def calculate_total_value(data):
    """计算总价值"""
    return sum(item['price'] * item['stock'] for item in data)


# 示例过滤函数
def is_electronic_category(item):
    """判断是否为电子类产品"""
    return item['category'] == '电子'


def is_high_value(item):
    """判断是否为高价值商品"""
    return item['price'] > 90


# 示例聚合函数
def count_by_category(data):
    """按类别计数"""
    category_count = {}
    for item in data:
        category = item['category']
        category_count[category] = category_count.get(category, 0) + 1
    return category_count


async def main():
    """主函数，演示各种类型的管道"""
    
    print("=" * 50)
    print("1. 基本数据管道示例")
    print("=" * 50)
    
    # 创建基本管道
    basic_pipeline = (DataPipeline()
                      .add_step(DataSourceStep("获取数据", get_sample_data))
                      .add_step(DataTransformerStep("添加折扣信息", add_discount))
                      .add_step(DataFilterStep("筛选电子类产品", is_electronic_category)))
    
    result1 = basic_pipeline.process(None)
    print("基本管道结果:")
    for item in result1:
        print(f"  {item}")
    
    print("\n" + "=" * 50)
    print("2. 聚合管道示例")
    print("=" * 50)
    
    # 创建聚合管道
    aggregation_pipeline = (DataPipeline()
                            .add_step(DataSourceStep("获取数据", get_sample_data))
                            .add_step(DataAggregatorStep("计算总价值", calculate_total_value)))
    
    result2 = aggregation_pipeline.process(None)
    print(f"聚合管道结果: 总价值 = {result2}")
    
    print("\n" + "=" * 50)
    print("3. 条件分支管道示例")
    print("=" * 50)
    
    # 创建条件分支管道
    high_value_branch = (DataPipeline()
                         .add_step(DataTransformerStep("高价值处理", lambda data: [dict(item, **{'tag': 'premium'}) for item in data])))
    
    low_value_branch = (DataPipeline()
                        .add_step(DataTransformerStep("低价值处理", lambda data: [dict(item, **{'tag': 'standard'}) for item in data])))
    
    conditional_pipeline = (DataPipeline()
                            .add_step(DataSourceStep("获取数据", get_sample_data))
                            .add_step(ConditionalBranchStep(
                                "按价值分类",
                                lambda data: any(item['price'] > 100 for item in data),
                                high_value_branch,
                                low_value_branch)))
    
    result3 = conditional_pipeline.process(None)
    print("条件分支管道结果:")
    for item in result3[:2]:  # 只显示前两个
        print(f"  {item}")
    
    print("\n" + "=" * 50)
    print("4. 异步管道示例")
    print("=" * 50)
    
    # 创建异步管道
    async_pipeline = (DataPipeline()
                      .add_step(DataSourceStep("获取数据", get_sample_data))
                      .add_step(DelayStep("模拟网络延迟", 1))
                      .add_step(DataTransformerStep("添加分类计数", 
                                                  lambda data: dict(
                                                      items=data,
                                                      category_count=count_by_category(data)))))
    
    result4 = await async_pipeline.process_async(None)
    print("异步管道结果:")
    print(f"  商品数量: {len(result4['items'])}")
    print(f"  分类统计: {result4['category_count']}")


if __name__ == "__main__":
    asyncio.run(main())