# 三数之和 排序 + 固定一个数 + 双指针
# 注意去重
# 注意自加自减在相等的时候也需要判断
def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    n = len(nums)
    res = []
    for i in range(n-2):
        if nums[i] > 0:
            break
        # 注意去重
        if i > 0 and nums[i] == nums[i-1]:
            continue
        target = 0 - nums[i]
        l, r = i+1, n-1
        while l < r:
            if nums[l] + nums[r] == target:
                res.append([nums[i], nums[l], nums[r]])
                # 注意去重
                while l<r and nums[l] == nums[l+1]: l+=1
                while l<r and nums[r] == nums[r-1]: r-=1
                # 注意移动指针
                l += 1
                r -= 1
            elif nums[l] + nums[r] < target:
                l += 1
            else:
                r -= 1
    return res

# 无重复字符的最长子串 滑动窗口 用一个last字典记录每个字符最后出现的位置
# left表示滑动窗口的开始 for循环表示滑动窗口的右侧，不断移动
def length_of_longest_substring(s: str) -> int:
    left = 0
    last = {}
    ans = 0
    for i, c in enumerate(s):
        # 窗口内已有该字符
        if c in last and last[c] >= left:
            left = last[c] + 1
        # 窗口内没有该字符
        last[c] = i
        ans = max(ans, i-left+1)
    return ans

# 找到字符串中所有字母异位词 定长的滑动窗口
# 右边界还是采用for循环 左侧使用left指针 需要维护滑动窗口的长度
# p经过排序与s滑动窗口字符串的排序比较 相等返回left

# 上述方式也可行，但是排序耗时较长，不如Counter计数快速
# 循环时最开始就扩展 当window本来就是要求长度时，后面要收缩

# 这道题需要重点注意
from collections import Counter
def find_anagrams(s: str, p: str) -> list[int]:
    res = []
    d = Counter(p)
    window = Counter()
    k = len(p)
    for i, c in enumerate(s):
        window[c] += 1
        left = i - k + 1
        # 后续情况都是window已经满的情况，需要收缩
        if left >= 0:
            if window == d:
                res.append(left)
            window[s[left]] -= 1
            if window[s[left]] == 0:
                del window[s[left]]
    return res

# 和为K的子数组
# pre[j] = 0...j的前缀和
# pre[i ... j]的路径和 = pre[j] - pre[i-1]
# 遍历每个数j，如果当前数的前缀和pre[j] - 前面某个数的前缀和pre[i] = k
# 那么从i到j这条连续子数组就是要的一组
# 所以在pre[j]时，看前面是否有pre[i] = pre[j] - k
def subarray_sum(nums: list[int], k: int) -> int:
    # 记录前缀和 key：和 value：个数
    d = {0:1}
    presum = 0
    ans = 0
    for num in nums:
        presum += num
        ans += d.get(presum-k, 0)
        d[presum] = d.get(presum, 0) + 1
    return ans




            
            
        




        
