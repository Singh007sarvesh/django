def rec(str1):
    if len(str1)==0:
        return str1
    return rec(str1[1:])+str1[0]
