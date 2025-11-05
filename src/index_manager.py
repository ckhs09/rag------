# src/index_manager.py
import os
from typing import List, Dict
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document

from src.document_loader import load_document, split_document

class IndexManager:
    """
    索引管理器，负责文档的嵌入、向量存储和索引建立
    """
    
    def __init__(self, api_key: str = None, persist_directory: str = "chroma_db"):
        """
        初始化索引管理器
        
        Args:
            api_key: OpenAI API密钥
            persist_directory: 向量数据库持久化目录
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("需要提供OpenAI API密钥")
            
        # 初始化嵌入模型
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        
        # 初始化向量存储
        self.persist_directory = persist_directory
        self.vector_store = None
        
    def create_index_from_preprocessed_docs(self, documents: List[Document]) -> Chroma:
        """
        从预处理过的文档列表中创建索引
        
        Args:
            documents: 预处理过的Document对象列表
            
        Returns:
            Chroma向量存储实例
        """
        # 创建向量存储
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        # 持久化索引
        self.vector_store.persist()
        
        return self.vector_store
    
    def _load_docs_list(self, docs_list_file: str) -> List[str]:
        """
        从文件中加载文档列表
        
        Args:
            docs_list_file: 文档列表文件路径
            
        Returns:
            文档路径列表
        """
        if not os.path.exists(docs_list_file):
            raise FileNotFoundError(f"文档列表文件 {docs_list_file} 不存在")
            
        with open(docs_list_file, 'r', encoding='utf-8') as file:
            docs_list = [line.strip() for line in file if line.strip()]
            
        return docs_list
    
    def _process_local_document(self, file_path: str) -> List[Document]:
        """
        处理本地文档文件
        
        Args:
            file_path: 文档文件路径
            
        Returns:
            Document对象列表
        """
        # 加载文档
        content = load_document(file_path)
        
        # 分割文档
        chunks = split_document(content, chunk_size=500, chunk_overlap=50)
        
        # 创建Document对象列表
        documents = []
        filename = os.path.basename(file_path)
        
        for index, chunk in enumerate(chunks):
            # 创建Document对象，包含元数据
            doc = Document(
                page_content=chunk,
                metadata={
                    "source": filename,
                    "index": index,
                    "id": f"{filename}_{index}"
                }
            )
            documents.append(doc)
            
        return documents
    
    def add_document_to_index(self, file_path: str):
        """
        将单个文档添加到现有索引中
        
        Args:
            file_path: 文档文件路径
        """
        if not self.vector_store:
            raise ValueError("请先创建索引")
            
        # 处理文档
        documents = self._process_local_document(file_path)
        
        # 添加到现有向量存储
        self.vector_store.add_documents(documents)
        
        # 持久化更新
        self.vector_store.persist()
        
    def load_existing_index(self) -> Chroma:
        """
        加载已存在的索引
        
        Returns:
            Chroma向量存储实例
        """
        if not os.path.exists(self.persist_directory):
            raise ValueError("索引目录不存在，请先创建索引")
            
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        
        return self.vector_store
    
    def search_similar_documents(self, query: str, k: int = 4) -> List[Document]:
        """
        搜索相似文档
        
        Args:
            query: 查询文本
            k: 返回结果数量
            
        Returns:
            相似文档列表
        """
        if not self.vector_store:
            raise ValueError("请先加载或创建索引")
            
        return self.vector_store.similarity_search(query, k=k)
