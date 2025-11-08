#!/usr/bin/env python3
"""
JSON数据处理管道示例
演示了如何构建处理结构化数据的管道
"""

import json
from typing import List, Dict, Any


class DataPipeline:
    """数据管道基类"""
    
    def __init__(self):
        self.transformers = []
    
    def add_transformer(self, transformer):
        """向管道添加转换器"""
        self.transformers.append(transformer)
        return self  # 支持链式调用
    
    def process(self, data):
        """通过所有转换器处理数据"""
        result = data
        for transformer in self.transformers:
            result = transformer.transform(result)
        return result


class Transformer:
    """转换器基类"""
    
    def transform(self, data):
        """转换数据"""
        raise NotImplementedError


class JSONLoaderTransformer(Transformer):
    """JSON加载转换器"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def transform(self, _):
        """从文件加载JSON数据"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)


class FilterByAgeTransformer(Transformer):
    """按年龄过滤转换器"""
    
    def __init__(self, min_age: int):
        self.min_age = min_age
    
    def transform(self, data: List[Dict[str, Any]]):
        """过滤年龄大于等于指定值的记录"""
        return [record for record in data if record.get('age', 0) >= self.min_age]


class AddFullNameTransformer(Transformer):
    """添加全名字段转换器"""
    
    def transform(self, data: List[Dict[str, Any]]):
        """为每条记录添加全名字段"""
        for record in data:
            record['full_name'] = f"{record.get('first_name', '')} {record.get('last_name', '')}".strip()
        return data


class SelectFieldsTransformer(Transformer):
    """字段选择转换器"""
    
    def __init__(self, fields: List[str]):
        self.fields = fields
    
    def transform(self, data: List[Dict[str, Any]]):
        """只保留指定字段"""
        return [{field: record.get(field) for field in self.fields} for record in data]


class JSONSaverTransformer(Transformer):
    """JSON保存转换器"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def transform(self, data):
        """将数据保存为JSON文件"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return data


def create_sample_data():
    """创建示例JSON数据"""
    sample_data = [
        {"first_name": "张", "last_name": "三", "age": 25, "city": "北京"},
        {"first_name": "李", "last_name": "四", "age": 17, "city": "上海"},
        {"first_name": "王", "last_name": "五", "age": 30, "city": "广州"},
        {"first_name": "赵", "last_name": "六", "age": 22, "city": "深圳"}
    ]
    
    with open('people.json', 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # 创建示例输入文件
    create_sample_data()
    
    # 构建数据管道：加载数据 -> 过滤年龄>=18的记录 -> 添加全名 -> 只保留姓名和年龄 -> 保存结果
    pipeline = (DataPipeline()
                .add_transformer(JSONLoaderTransformer('people.json'))
                .add_transformer(FilterByAgeTransformer(18))
                .add_transformer(AddFullNameTransformer())
                .add_transformer(SelectFieldsTransformer(['full_name', 'age']))
                .add_transformer(JSONSaverTransformer('adults.json')))
    
    # 执行管道
    result = pipeline.process(None)
    
    print("JSON处理管道执行完成!")
    print("检查 adults.json 文件查看结果")