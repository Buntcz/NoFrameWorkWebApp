route_table = {}

def route(path,methods=['GET']):
    def decorator(func):
        if path not in route_table:
            route_table[path] = {}
        for method in methods:
            route_table[path][method] = func
        return func
    return decorator
