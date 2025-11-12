"""
Query Expansion 示例
对输入问题进行语义丰富与扩展，有利于从数据中生成更全面与更准确的答案
"""

def expand_with_synonyms(query):
    """
    使用同义词扩展查询
    """
    synonym_map = {
        "car": ["automobile", "vehicle", "motorcar"],
        "buy": ["purchase", "acquire", "obtain"],
        "fast": ["quick", "rapid", "speedy", "swift"],
        "good": ["excellent", "great", "fine", "superior"],
        "big": ["large", "huge", "enormous", "massive"],
        "small": ["little", "tiny", "miniature"],
        "computer": ["PC", "machine", "device"],
        "help": ["assist", "support", "aid"],
        "problem": ["issue", "difficulty", "trouble"],
        "programming": ["coding", "software development", "scripting"]
    }
    
    expanded_terms = [query]  # 包含原始查询
    
    # 查找可以扩展的词
    words = query.lower().split()
    for i, word in enumerate(words):
        # 移除常见标点符号
        clean_word = word.strip('.,?!;:"')
        if clean_word in synonym_map:
            # 为每个同义词创建一个新的查询版本
            for synonym in synonym_map[clean_word]:
                new_words = words.copy()
                new_words[i] = synonym
                expanded_terms.append(" ".join(new_words))
    
    return expanded_terms

def expand_with_context(query):
    """
    添加上下文信息扩展查询
    """
    context_expansions = []
    
    # 基础扩展
    context_expansions.append(query)
    
    # 技术上下文扩展
    if any(word in query.lower() for word in ["python", "java", "javascript", "react", "vue", "angular"]):
        expanded = f"{query} programming tutorial example"
        context_expansions.append(expanded)
        
        expanded = f"{query} best practices"
        context_expansions.append(expanded)
        
        expanded = f"{query} beginner guide"
        context_expansions.append(expanded)
    
    # 健康相关扩展
    if any(word in query.lower() for word in ["health", "exercise", "diet", "nutrition", "fitness"]):
        expanded = f"{query} benefits research study"
        context_expansions.append(expanded)
        
        expanded = f"{query} tips for beginners"
        context_expansions.append(expanded)
        
        expanded = f"{query} latest guidelines"
        context_expansions.append(expanded)
    
    return context_expansions

def expand_with_hyde(query):
    """
    使用HyDE（ Hypothetical Document Embeddings）方法扩展查询
    创建一个假设的理想答案，然后提取关键词进行扩展
    """
    # 这里模拟一个简单的HyDE实现
    hypothetical_answers = {
        "what is machine learning": "Machine learning is a subset of artificial intelligence that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. It focuses on the development of computer programs that can access data and use it to learn for themselves.",
        "how to use python decorators": "Python decorators are a powerful feature that allows you to modify the behavior of functions or classes. They provide a way to extend or alter the behavior of functions or methods without permanently modifying the function's code itself.",
        "benefits of exercise": "Regular exercise provides numerous health benefits including improved cardiovascular health, increased muscle strength, better mental health, weight management, stronger bones, and reduced risk of chronic diseases."
    }
    
    expansions = [query]
    
    # 生成假设答案
    for key, hypo_answer in hypothetical_answers.items():
        if key in query.lower():
            # 从假设答案中提取关键词进行扩展
            key_phrases = extract_key_phrases(hypo_answer)
            for phrase in key_phrases:
                expansions.append(f"{query} {phrase}")
            break
    
    # 如果没有匹配的模板，使用通用扩展
    if len(expansions) == 1:
        generic_expansions = [
            f"{query} definition",
            f"{query} explanation",
            f"{query} examples",
            f"what is {query}",
            f"how to {query}" if 'how' not in query.lower() else query
        ]
        expansions.extend(generic_expansions)
    
    return expansions

def extract_key_phrases(text):
    """
    从文本中提取关键短语（简化版实现）
    """
    # 简化的关键词提取逻辑
    phrases = []
    sentences = text.split('.')
    for sentence in sentences[:2]:  # 只处理前两句话
        words = sentence.strip().split()
        if len(words) > 3:
            # 提取句子的前3-5个词作为关键短语
            phrase_length = min(5, len(words))
            phrases.append(" ".join(words[:phrase_length]))
    return phrases

# 示例使用
if __name__ == "__main__":
    test_queries = [
        "what is machine learning",
        "how to use python decorators",
        "benefits of exercise",
        "car maintenance tips"
    ]
    
    print("=== 同义词扩展示例 ===")
    for query in test_queries[:2]:
        print(f"原始查询: {query}")
        synonyms = expand_with_synonyms(query)
        for syn in synonyms:
            print(f"  扩展版本: {syn}")
        print()
    
    print("=== 上下文扩展示例 ===")
    for query in test_queries:
        print(f"原始查询: {query}")
        context_exp = expand_with_context(query)
        for ctx in context_exp:
            print(f"  扩展版本: {ctx}")
        print()
    
    print("=== HyDE扩展示例 ===")
    for query in test_queries[:2]:
        print(f"原始查询: {query}")
        hyde_exp = expand_with_hyde(query)
        for hyde in hyde_exp:
            print(f"  扩展版本: {hyde}")
        print()