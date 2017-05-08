import hashlib
def get_md5(url):
    if isinstance(url, str): #因为python3中的字符串都为unicode
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()