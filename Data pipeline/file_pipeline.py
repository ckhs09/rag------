#!/usr/bin/env python3
"""
文件处理数据管道示例
演示了如何构建一个简单的数据摄取管道，从文件读取数据并通过多个转换步骤处理
"""

import json
import csv
from typing import List, Any, Generator


class DataPipeline:
    """数据管道基类"""
    
    def __init__(self):
        self.transformers: List[Transformer] = []
    
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


class FileReaderTransformer(Transformer):
    """文件读取转换器"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def transform(self, _):
        """读取文件内容"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.read()


class LineSplitterTransformer(Transformer):
    """行分割转换器"""
    
    def transform(self, data: str):
        """将文本按行分割"""
        return data.split('\n')


class FilterEmptyLinesTransformer(Transformer):
    """过滤空行转换器"""
    
    def transform(self, data: List[str]):
        """过滤掉空行"""
        return [line for line in data if line.strip()]


class ToUppercaseTransformer(Transformer):
    """转大写转换器"""
    
    def transform(self, data: List[str]):
        """将所有行转换为大写"""
        return [line.upper() for line in data]


class DataWriterTransformer(Transformer):
    """数据写入转换器"""
    
    def __init__(self, output_file: str):
        self.output_file = output_file
    
    def transform(self, data: List[str]):
        """将数据写入文件"""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(f"{item}\n")
        return data


def create_sample_data():
    """创建示例数据文件"""
    sample_data = """hello world
this is a test
data pipeline example
python is awesome

empty line above
last line"""
    
    with open('input.txt', 'w', encoding='utf-8') as f:
        f.write(sample_data)


if __name__ == "__main__":
    # 创建示例输入文件
    create_sample_data()
    
    # 构建数据管道
    pipeline = (DataPipeline()
                .add_transformer(FileReaderTransformer('input.txt'))
                .add_transformer(LineSplitterTransformer())
                .add_transformer(FilterEmptyLinesTransformer())
                .add_transformer(ToUppercaseTransformer())
                .add_transformer(DataWriterTransformer('output.txt')))
    
    # 执行管道
    result = pipeline.process(None)
    
    print("文件处理管道执行完成!")
    print("检查 output.txt 文件查看结果")