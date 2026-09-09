# 搜索旋转排序数组 无重复有序数组 二分判断哪半段有序
def search(nums: list[int], target: int) -> int:
    l, r = 0, len(nums)-1
    while l <= r:
        mid = (l + r) // 2
        if target == nums[mid]:
            return mid
        if nums[l] <= nums[mid]:
            if nums[l] <= target < nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
        else:
            if nums[mid] < target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1
    return -1

# 旋转排序数组最小值 有序数组无重复 找最小值
# 二分比较mid与右端
# nums[mid] > nums[r] 最小值肯定在右端 l = m+1
# 否则 最小值肯定在左端 （包含mid）r = m
# 循环到 l==r 时 nums[l] 即最小。
def find_min(nums: list[int]) -> int:
    l, r = 0, len(nums)-1
    while l<r:
        mid = (l+r)//2
        if nums[mid] > nums[r]:
            l = mid + 1
        else:
            r = mid
    return nums[l]

# 最小栈 辅助栈（维护栈顶为当前主栈的最小值）
# push: 与辅助栈栈顶比较，如果小于等于，进栈
# pop：与辅助栈栈顶比较，如果等于，出栈
# top：
# getMin：
class MinStack:
    def __init__(self):
        self.min = []
        self.main = []
    def push(self, value:int):
        self.main.append(value)
        if not self.min or value <= self.min[-1]:
            self.min.append(value)
    def pop(self):
        x = self.main.pop()
        if self.min[-1] == x:
            self.min.pop()
        return x
    def top(self):
        return self.main[-1]
    def getMin(self):
        return self.min[-1]

# 字符串解码 栈 cur是最后输出的字符串
# 遍历字符遇到数字，累计到num
# 字母 追加到当前串cur
# 【 把cur和num入栈
# 】弹出，cur = prev + cur*k
def decode_string(s: str) -> str:
    stack = []
    cur = ''
    num = 0
    for c in s:
        if c.isdigit():
            num = num *10 + int(c)
        if c == '[':
            stack.append((num, cur))
            cur = ''
            num = 0
        if c == ']':
            k, prev = stack.pop()
            cur = prev + k * cur
        else:
            cur += c
    return cur

# 每日温度 维持单调递减栈
# 栈保存的是温度+下标 注意是循环而不是一次性判断
def daily_temperatures(t: list[int]) -> list[int]:
    stack = []
    ans = [0] * len(t)
    for i, te in enumerate(t):
        while stack and stack[-1][1] < te:
            idx, x = stack.pop()
            ans[idx] = i - idx
        stack.append((i,te))
    return ans

# 数组中的第 K 个最大元素
def find_kth_largest(nums: list[int], k: int) -> int:
    return sorted(nums, reverse=True)[k-1]

# 前 K 个高频元素
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    from collections import Counter
    d = Counter(nums)
    temp = sorted(d, key=d.get, reverse=True)
    return temp[:k]

# 跳跃游戏 贪心 最远可达 记住不可达的判断条件 更新最远距离的方法
def can_jump(nums: list[int]) -> bool:
    far = 0
    for i, num in enumerate(nums):
        if i > far:
            return False
        far = max(far, i+num)
    return True

# 跳跃游戏Ⅱ end表示该次跳跃能够覆盖的范围
# far表示覆盖范围内能够达到的最远距离
# 从而找到下次跳跃覆盖的范围
def jump(nums: list[int]) -> int:
    end = far = jump = 0
    n = len(nums)
    for i in range(n-1):
        far = max(far, i + nums[i])
        if i == end:
            end = far
            jump += 1
    return jump

# 划分字母区间 两次遍历 返回的是每段的长度，而不是下标
# end表示当前段能延伸的最远边界
# 虽然移动i的过程中end再一直变动，当end在某一段移动中都不再变动时
# 说明之后的字母与前段的字母不相同了
def partition_labels(s: str) -> list[int]:
    last = {c:i for i,c in enumerate(s)}
    start = end = 0
    res = []
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            res.append(end - start + 1)
            start = i+1
    return res

# 打家劫舍 动态规划 dp[i]表示抢劫到第i间的最大总金额 = max(dp[i-1], dp[i-2] + nums[i])
def rob(nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])

    for i in range(2, len(nums)):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    return dp[len(nums) - 1]
    

    
        




            
            


