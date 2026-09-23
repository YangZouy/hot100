# 最长回文字串 中心扩展法
def longest_palindrome(s: str) -> str:
    def expand(l, r):
        while l>=0 and r<len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return s[l+1:r]
    best = ''
    for i in range(len(s)):
        for cand in [expand(i,i), expand(i,i+1)]:
            best = best if len(best) >= len(cand) else cand
    return best

# 最长公共子序列
# dp[i][j]表示text1的前i个字符和text2的前j个字符的最长公共子序列的长度
# dp[0][j]以及dp[i][0] = 0
# 状态转移：
# dp[i][j] = dp[i-1][j-1]+1 或者dp[i-1][j]或者dp[i][j-1]的较大者
def longest_common_subsequence(t1: str, t2: str) -> int:
    m,n = len(t1), len(t2)
    dp = [[0] * (n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if t1[i-1] == t2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# 颜色分类 三指针 p0 cur p2
def sort_colors(nums: list[int]) -> None:
    p0 = cur = 0
    p2 = len(nums) - 1
    while cur <= p2:
        if nums[cur] == 0:
            nums[p0], nums[cur] = nums[cur], nums[p0]
            cur += 1
            p0 += 1
        elif nums[cur] == 2:
            nums[p2], nums[cur] = nums[cur], nums[p2]
            p2 -= 1
        else:
            cur += 1

# 下一个排列 
# 从右往左找第一个下降位，右侧全部是升序，找到右侧中比下降位大的最小值，然后交换
# 右侧重新排序
# 注意判断下降位的条件
def next_permutation(nums: list[int]) -> None:
    n = len(nums)
    i = n - 2
    while i >=0 and nums[i] >= nums[i+1]:
        i -= 1
    if i>=0:
        j = n-1
        while j > i:
            if nums[j] > nums[i]:
                nums[j], nums[i] = nums[i], nums[j]
                break
            j -= 1
    nums[i+1:] = nums[i+1:][::-1]

# 寻找重复数 数值当成指向的下一个数，如果有重复数，说明他们指向同一个位置
# 有环，环的入口就是重复数
# 快慢指针
def find_duplicate(nums: list[int]) -> int:
    fast = slow = 0
    while True:
        fast = nums[nums[fast]]
        slow = nums[slow]
        if fast == slow:
            break
    p = 0
    while p!=slow:
        p = nums[p]
        slow = nums[slow]
    return slow

# 两数之和 map记录值和下标 边记边找
def two_sum(nums: list[int], target: int) -> list[int]:
    mp = {}
    res = []
    for i, num in enumerate(nums):
        find = target - num
        if find in mp:
            res.append(mp[find])
            res.append(i)
        else:
            mp[num] = i
    return res







        
        

    




