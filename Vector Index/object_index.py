"""
Object Index 示例

这个文件演示了如何创建和使用对象索引。
对象索引用于处理结构化数据对象，使其能够被语言模型理解和查询。
对于关系型数据库，对象索引可以用来存储表结构信息和上下文，辅助Text-to-SQL功能。
"""

try:
    from llama_index.core import Document
    from llama_index.core.objects import ObjectIndex, SimpleToolNodeMapping
    from llama_index.core.tools import FunctionTool
    from llama_index.llms.openai import OpenAI
except ImportError:
    print("请安装所需的依赖库: pip install llama-index")

# 定义示例类
class Customer:
    def __init__(self, name: str, email: str, age: int):
        self.name = name
        self.email = email
        self.age = age
    
    def __repr__(self):
        return f"Customer(name='{self.name}', email='{self.email}', age={self.age})"

# 定义工具函数
def get_customer_info(name: str) -> str:
    """根据姓名获取客户信息"""
    # 模拟数据库查询
    customers = {
        "张三": Customer("张三", "zhangsan@example.com", 30),
        "李四": Customer("李四", "lisi@example.com", 25),
    }
    
    customer = customers.get(name)
    if customer:
        return str(customer)
    else:
        return "未找到该客户"

def get_table_info(table_name: str) -> str:
    """获取数据库表信息"""
    # 模拟数据库表信息
    table_schemas = {
        "users": "用户表，包含id(主键), name(用户名), email(邮箱), age(年龄)字段",
        "orders": "订单表，包含id(主键), user_id(用户ID), product_name(产品名), amount(金额)字段",
        "products": "产品表，包含id(主键), name(产品名), price(价格), category(类别)字段"
    }
    
    return table_schemas.get(table_name, "未找到该表信息")

def create_object_index():
    """创建对象索引示例"""
    
    # 创建工具
    customer_tool = FunctionTool.from_defaults(
        fn=get_customer_info,
        name="get_customer_info",
        description="根据客户姓名获取客户信息"
    )
    
    table_tool = FunctionTool.from_defaults(
        fn=get_table_info,
        name="get_table_info",
        description="获取数据库表的结构信息"
    )
    
    # 创建映射
    mapping = SimpleToolNodeMapping.from_objects([customer_tool, table_tool])
    
    # 创建对象索引
    object_index = ObjectIndex.from_objects(
        [customer_tool, table_tool],
        mapping
    )
    
    return object_index

def query_object_index(index):
    """查询对象索引"""
    
    # 创建查询引擎
    query_engine = index.as_query_engine()
    
    # 查询示例
    response = query_engine.query("告诉我张三的信息")
    print(f"问题: 告诉我张三的信息")
    print(f"回答: {response}\n")
    
    response = query_engine.query("users表包含哪些字段")
    print(f"问题: users表包含哪些字段")
    print(f"回答: {response}\n")

if __name__ == "__main__":
    print("=== 对象索引示例 ===\n")
    
    # 创建索引
    object_index = create_object_index()
    
    # 查询索引
    query_object_index(object_index)