list_form = []

def extensions_switcher(extension):
    global list_form
    list_form.append(extension)
    def decorator(func):
        def wrapper(filename):
            name, file_ext = filename.rsplit('.', 1)
            if file_ext in list_form:
                return f'open {file_ext} file'
            else:
                return "unsupported extension"
        return wrapper
    return decorator