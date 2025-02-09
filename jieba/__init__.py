# jieba/__init__.py
print("Using dummy jieba package")

def cut(text, cut_all=False, HMM=True):
    # Dummy implementation: simply split text into characters
    return list(text)

def lcut(text, cut_all=False, HMM=True):
    return list(text)

def set_dictionary(dict_path):
    pass

def load_userdict(f):
    pass
