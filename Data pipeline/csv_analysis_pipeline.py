#!/usr/bin/env python3
"""
CSV数据分析管道示例
演示了如何构建一个更复杂的数据分析管道，包括数据清洗、转换和聚合操作
"""

import csv
from typing import List, Dict, Any
from collections import defaultdict


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


class CSVLoaderTransformer(Transformer):
    """CSV加载转换器"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def transform(self, _):
        """从CSV文件加载数据"""
        data = []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data


class DataCleanerTransformer(Transformer):
    """数据清洗转换器"""
    
    def transform(self, data: List[Dict[str, Any]]):
        """清洗数据：移除空值，转换数据类型"""
        cleaned_data = []
        for row in data:
            # 只保留非空记录
            if all(row.values()):
                # 转换数值字段
                try:
                    row['quantity'] = int(row['quantity'])
                    row['price'] = float(row['price'])
                    cleaned_data.append(row)
                except ValueError:
                    # 如果转换失败，跳过该记录
                    continue
        return cleaned_data


class CalculateTotalTransformer(Transformer):
    """计算总额转换器"""
    
    def transform(self, data: List[Dict[str, Any]]):
        """为每条记录计算总金额"""
        for row in data:
            row['total'] = row['quantity'] * row['price']
        return data


class GroupByCategoryTransformer(Transformer):
    """按类别分组转换器"""
    
    def transform(self, data: List[Dict[str, Any]]):
        """按产品类别分组并计算统计信息"""
        grouped = defaultdict(list)
        for row in data:
            category = row['category']
            grouped[category].append(row)
        
        # 计算每个类别的统计数据
        result = []
        for category, items in grouped.items():
            total_quantity = sum(item['quantity'] for item in items)
            total_value = sum(item['total'] for item in items)
            avg_price = sum(item['price'] for item in items) / len(items)
            
            result.append({
                'category': category,
                'total_quantity': total_quantity,
                'total_value': round(total_value, 2),
                'average_price': round(avg_price, 2),
                'item_count': len(items)
            })
        
        return result


class CSVSaverTransformer(Transformer):
    """CSV保存转换器"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def transform(self, data: List[Dict[str, Any]]):
        """将数据保存为CSV文件"""
        if not data:
            return data
        
        fieldnames = data[0].keys()
        with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        return data


def create_sample_data():
    """创建示例CSV数据"""
    sample_data = [
        ['product', 'category', 'quantity', 'price'],
        ['笔记本电脑', '电子产品', '10', '5000.00'],
        ['手机', '电子产品', '20', '3000.00'],
        ['书籍', '文化用品', '50', '50.00'],
        ['钢笔', '文化用品', '100', '10.00'],
        ['T恤', '服装', '200', '50.00'],
        ['牛仔裤', '服装', '150', '100.00'],
        ['', '食品', '30', '5.00'],  # 空产品名称，会被清洗掉
        ['苹果', '食品', '100', '3.00'],
    ]
    
    with open('sales.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)


if __name__ == "__main__":
    # 创建示例输入文件
    create_sample_data()
    
    # 构建数据管道：加载数据 -> 清洗数据 -> 计算总额 -> 按类别分组 -> 保存结果
    pipeline = (DataPipeline()
                .add_transformer(CSVLoaderTransformer('sales.csv'))
                .add_transformer(DataCleanerTransformer())
                .add_transformer(CalculateTotalTransformer())
                .add_transformer(GroupByCategoryTransformer())
                .add_transformer(CSVSaverTransformer('summary.csv')))
    
    # 执行管道
    result = pipeline.process(None)
    
    print("CSV分析管道执行完成!")
    print("原始数据条数:", len(result))  # 注意：这里的结果是清洗后的数据
    print("检查 summary.csv 文件查看聚合结果")
    
    # 打印部分结果
    print("\n聚合结果预览:")
    for item in result[:3]:  # 显示前3个结果
        print(f"类别: {item['category']}, 数量: {item['total_quantity']}, 总价值: {item['total_value']}")