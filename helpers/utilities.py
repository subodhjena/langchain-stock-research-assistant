# checks if a file exists in the given path
def file_exists(path):
    try:
        open(path, 'r')
        return True
    except FileNotFoundError:
        return False
    