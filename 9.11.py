# 乘积最大子数组
# dp[i] 到数组第i位的最大乘积
# dp[i] = max{dp[i-1] * nums[i], nums[i]}
def max_product(nums: list[int]) -> int:
    n = len(nums)
    mx = [0] * n
    mn = [0] * n
    mx[0] = mn[0] = nums[0]
    for i in range(1,n):
        mx[i] = max(nums[i], nums[i]*mx[i-1], nums[i]*mn[i-1])
        mn[i] = min(nums[i], nums[i]*mx[i-1], nums[i]*mn[i-1])
    return max(mx)

# 分割等和子集
# 0/1背包：有一个容量为 C 的背包，和 n 个物品。第 i 个物品重 w[i]、价值 v[i]。每个物品最多选一次，求能装下的最大总价值。
# 标准二维DP是
# dp[i][j] = 前i个物品，能否凑出容量j
# dp[i][j] = max(dp[i-1][j], // 不选第i个物品
#               dp[i-1][j-w[i]]+v[i]])  // 选第i个物品
# dp[i][j]只依赖dp[i-1]上一行
# 用一个一维数组滚动就可以了
def can_partition(nums: list[int]) -> bool:
    s = sum(nums)
    if s % 2:
        return False
    target = s // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for j in range(target, x-1, -1):
            dp[j] = dp[j] or dp[j - x]
    return dp[target]

# 不同路径
# dp[i][j]表示到第i行第j列有的路径数量
# dp[i][j] = dp[i-1][j] + dp[i][j-1]
# dp[0][j] = 1
# dp[i][0] = 1
# 注意循环的开始范围
def unique_paths(m: int, n: int) -> int:
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]

# 最小路径和
# - 状态：dp[i][j] = 到达 (i, j) 的最小路径和
#   - 转移：dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
#   - 边界要单独处理：
#       最上行只能从「左边」累加过来，dp[0][j] = dp[0][j-1] + grid[0][j]
#       最左列只能从「上方」累加过来，dp[i][0] = dp[i-1][0] + grid[i][0]
def min_path_sum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for i in range(1,m):
        dp[i][0] = dp[i-1][0] + grid[i][0]
    for j in range(1,n):
        dp[0][j] = dp[0][j-1] + grid[0][j]
    for i in range(1,m):
        for j in range(1,n):
            dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j]
    return dp[m-1][n-1]





