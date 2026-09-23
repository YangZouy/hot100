# 完全平方数
# d[i]：组成i的最少完全平方数有哪些
# 初始化：dp[0] = 0, dp[i] = inf
# 状态转移：df[i] = min(dp[i], dp[i-k*k]+1)
def num_squares(n: int) -> int:
    dp = [float('inf')] * (n+1)
    dp[0] = 0
    for i in range(1,n+1):
        k = 1
        while k*k <= i:
            dp[i] = min(dp[i], dp[i-k*k])
            k+=1
    return dp[n]

# 零钱兑换
# dp[i] 凑成金额i的
# dp[0] = 0 dp[i] = inf
# 对每个i枚举硬币 c<=i:dp[i] = min(dp[i], dp[i-c] + 1)
# 最后 dp[amount] 仍为 inf 则不可达返回 -1。

def coin_change(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount+1)
    dp[0] = 0
    for i in range(1,amount+1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i], dp[i-c]+1)
    return dp[amount] if dp[amount] != float('inf') else -1

# 单词拆分
# dp[i] = s[:i] s前i个字符是否能够被拼出来
# dp[0] = True dp[i] = False 空字符串可以被拼出来，其他的表示不可达
# dp[i] = dp[j] and s[j:i] in word 遍历前i个字符中的每个，进行截断
# 当前j个可以被拼出，且最后的s[j:i]也能在word中找到
# 使用set是因为查找更快（hash）
def word_break(s: str, word_dict: list[str]) -> bool:
    word = set(word_dict)
    dp = [False] * (len(s)+1)
    dp[0] = True
    for i in range(1, len(s)+1):
        for j in range(i):
            if dp[j] and s[j:i] in word:
                dp[i] = True
                break
    return dp[len(s)]

# 最长递增子序列
# dp[i] = 以 nums[i] 结尾的 LIS 长度。
# 对每个 i，看所有 j<i：若 nums[j] < nums[i] 则可接上，
# dp[i]=max(dp[i], dp[j]+1)。
# 答案是 dp 数组的最大值（不一定是 dp[n-1]）。
def length_of_lis(nums: list[int]) -> int:
    dp = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)



