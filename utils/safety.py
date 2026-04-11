def is_safe_query(query):
    forbidden = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER"]
    return not any(word in query.upper() for word in forbidden)