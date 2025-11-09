"""
SQL Database Example

这个文件演示了如何在LlamaIndex中处理关系型数据库。
对于关系型数据库，最适合的索引类型是对象索引(Object Index)，它可以存储表结构信息，
辅助Text-to-SQL功能，帮助LLM更好地理解数据库结构并生成准确的SQL查询。
"""

try:
    # 注意：实际使用中需要安装相应的依赖
    # pip install llama-index sqlalchemy
    from llama_index.core.objects import ObjectIndex, SQLTableSchema, SQLTableNodeMapping
    from llama_index.core import SQLDatabase, VectorStoreIndex
    from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
except ImportError as e:
    print(f"缺少依赖: {e}")
    print("请安装所需的依赖库: pip install llama-index sqlalchemy")

def demonstrate_sql_database_indexing():
    """
    演示如何为关系型数据库创建索引
    
    对于关系型数据库，推荐使用对象索引(Object Index)来:
    1. 存储表结构(schema)信息
    2. 提供表的上下文描述
    3. 辅助Text-to-SQL功能，提高SQL生成准确性
    """
    
    print("=== 关系型数据库索引示例 ===\n")
    
    # 模拟数据库表信息
    # 在实际应用中，这些信息会从真实的数据库中获取
    table_infos = [
        {
            "table_name": "users", 
            "table_summary": "用户表，存储用户基本信息，包括用户ID、姓名、邮箱和年龄"
        },
        {
            "table_name": "orders", 
            "table_summary": "订单表，存储用户订单信息，包括订单ID、用户ID、产品名称和金额"
        },
        {
            "table_name": "products", 
            "table_summary": "产品表，存储产品信息，包括产品ID、名称、价格和类别"
        }
    ]
    
    print("数据库表结构信息:")
    for table_info in table_infos:
        print(f"- 表名: {table_info['table_name']}")
        print(f"  描述: {table_info['table_summary']}")
    print()
    
    # 创建表模式对象
    table_schema_objs = [
        SQLTableSchema(
            table_name=t["table_name"], 
            context_str=t["table_summary"]
        )
        for t in table_infos
    ]
    
    print("在LlamaIndex中处理关系型数据库的最佳实践:")
    print("1. 使用ObjectIndex存储表结构信息和上下文描述")
    print("2. 为每个表提供清晰的自然语言描述，帮助LLM理解表的用途")
    print("3. 使用SQLTableSchema定义表结构")
    print("4. 结合VectorStoreIndex进行语义检索")
    print("5. 使用SQLDatabase接口与真实数据库交互\n")
    
    print("这种方法的优势:")
    print("- 帮助LLM理解数据库结构，提高Text-to-SQL准确性")
    print("- 支持复杂的多表关联查询")
    print("- 可以根据查询语义检索相关表")
    print("- 提供可扩展的数据库上下文管理")

def main():
    """主函数"""
    demonstrate_sql_database_indexing()

if __name__ == "__main__":
    main()