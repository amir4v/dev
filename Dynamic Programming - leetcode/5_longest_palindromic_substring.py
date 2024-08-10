def longest_palindromic_substring(s):
    res = ''
    
    for i in range(len(s)):
        # odd length
        l, r = i, i
        while (l >= 0 and r < len(s) and s[l]==s[r]):
            if len(s[l:r+1]) > len(res):
                res = s[l:r+1]
            l -= 1
            r += 1
        
        # even length
        l, r = i, i+1
        while (l >= 0 and r < len(s) and s[l]==s[r]):
            if len(s[l:r+1]) > len(res):
                res = s[l:r+1]
            l -= 1
            r += 1
    
    return res
