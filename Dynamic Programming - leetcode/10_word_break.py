# DP

def word_break(s, word_dict):
    dp = (len(s)+1) * [False]
    dp[len(s)] = True
    
    for i in range(len(s)-1, -1, -1):
        for w in word_break:
            if (i+len(w) <= len(s)) and s[i:i+len(w)] == w:
                dp[i] = dp[i+len(w)]
            if dp[i]:
                break
    
    return dp[0]
