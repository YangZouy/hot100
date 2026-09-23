# 二叉树的直径 递归 与深度有关 左深+右深
def diameter_of_binary_tree(root: "TreeNode | None") -> int:
    ans = 0
    def depth(node):
        nonlocal ans
        if not node:
            return 0
        l = depth(node.left)
        r = depth(node.right)
        ans = max(ans, l+r)
        return 1+max(l,r)
    depth(root)
    return ans

# 有序数组转二叉搜索树 找中点+递归
def sorted_array_to_bst(nums: list[int]) -> "TreeNode | None":
    def dfs(l, r):
        if l>r: return None
        m = (l+r)//2
        node = TreeNode(nums[m])
        node.left = dfs(l,m-1)
        node.right = dfs(m+1,r)
        return node
    return dfs(0,len(nums)-1)

# 搜索插入位置
def search_insert(nums: list[int], target: int) -> int:
    l, r = 0, len(nums)-1
    while l <= r:
        m = (l + r) // 2
        if nums[m] == target:
            return m
        elif nums[m] < target:
            l = m+1
        else:
            r = m-1
    return l

# 有效的括号 失败立即返回 成功需要继续循环 else重要 主要区分左括号和右括号
# if条件中主要找失败的情况
def is_valid(s: str) -> bool:
    stack = []
    mp = {'}': '{', ')': '(', ']': '['}
    for c in s:
        if c in mp:
            if not stack or stack.pop() != mp[c]:
                return False
        else:
            stack.append(c)
    return len(stack) == 0

# 买卖股票的最佳时机 贪心 维护历史最低价和最大利润 注意两者更新的顺序
def max_profit(prices: list[int]) -> int:
    low = float('inf')
    ans = 0
    for p in prices:
        ans = max(ans, p - low)
        low = min(low, p)
    return ans

# 爬楼梯 dp[i] = 爬第i阶的方法数
# dp[i] = dp[i-1] + dp[i-2]
# dp[0] = 1 dp[1] = 1
# i = 0时,a = dp[1] 所以i = n-1时,a = dp[n]
def climb_stairs(n: int) -> int:
    a = b = 1
    for i in range(n):
        a, b = b, a + b
    return a

# 杨辉三角 逐行生成
# 第i行个数: i+1 (i从0开始)
# 中间的值 row[j] = 上一行(正上方 + 左上方)
# 所以res是个二维数组
def generate_pascal(numRows: int) -> list[list[int]]:
    res = []
    for i in range(numRows):
        temp = [1] * (i+1)
        for j in range(1,i):
            temp[j] = res[i-1][j-1] + res[i-1][j]
        res.append(temp)
    return res

# 只出现一次的数字 异或 0与任何 = 任何 任何与本身 = 0
def single_number(nums: list[int]) -> int:
    res = 0
    for num in nums:
        res ^= num
    return res
     
# 多数元素 投票法 给出一个cand 和它的计数 初始值赋值有两种不同的方式 对应不同的写法
def majority_element(nums: list[int]) -> int:
    cand = count = 0
    for num in nums:
        if count == 0:
            cand = num
        if num == cand:
            count += 1
        else:
            count -= 1
    return cand

# 字母异位词分组 字典 键为排序后的str，值为未排序的 新的方式可以直接用defaultdict
# 不用判断是否是新创建的key
def group_anagrams(strs: list[str]) -> list[list[str]]:
    from collections import defaultdict
    d = defaultdict(list)
    for str in strs:
        key = ''.join(sorted(str))
        d[key].append(str)
    return list(d.values())

# 最长连续序列 如果x的前一个没有，说明x就是起点
# 当x为起点时，直接在set中找x+1，set中找O(1)
def longest_consecutive(nums: list[int]) -> int:
    l = set(nums)
    best = 0
    for num in nums:
        if num - 1 not in l:
            y = num
            while y + 1 in l:
                y += 1
            best = max(best, y-num+1)
    return best

# 盛最多水的容器 判断循环条件时l不用=r，因为等于时算出来的面积是0
def max_area(height: list[int]) -> int:
    l, r = 0, len(height)-1
    best = 0
    while l < r:
        best = max(best, (r-l) * min(height[l], height[r]))
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return best




        




            
