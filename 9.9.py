# 完全平方数
# d[i]：组成i的最少完全平方数有哪些
# 初始化：
# 状态转移：
def num_squares(n: int) -> int:
    dp = [float('inf')] * (n+1)
    dp[0] = 0
    for i in range(1,n+1):
        k = 1
        while k*k <= i:
            dp[i] = min(dp[i], dp[i-k*k])
            k+=1
    return dp[n]


