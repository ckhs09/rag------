#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RAG应用测试文件
用于测试各个模块的功能
"""

import sys
import os
import unittest

# 添加src目录到Python路径中
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.document_loader import load_document, split_document


class TestRAG(unittest.TestCase):
    """RAG应用测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.test_file = "data/sample.txt"
    
    def test_document_loading(self):
        """测试文档加载功能"""
        if os.path.exists(self.test_file):
            documents = load_document(self.test_file)
            self.assertIsInstance(documents, list)
            self.assertGreater(len(documents), 0)
    
    def test_document_splitting(self):
        """测试文档分割功能"""
        if os.path.exists(self.test_file):
            documents = load_document(self.test_file)
            texts = split_document(documents, chunk_size=500, chunk_overlap=100)
            self.assertIsInstance(texts, list)
            self.assertGreater(len(texts), 0)


if __name__ == "__main__":
    unittest.main()