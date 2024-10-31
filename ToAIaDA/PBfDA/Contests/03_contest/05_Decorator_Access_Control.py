from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if token in logged:
            return func(*args, **kwargs)
        else:
            print("Access denied")
            return None
    return wrapper