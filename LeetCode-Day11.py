"""
LeetCode 必刷100题 · Day 11（2026-07-27）
========================================
面试方向：AI 应用 / Agent 开发
今日题目（共 10 道，对应必刷表 #29–#38，#34 与 Day9 重复已跳过）：
  - 第 29 题：颜色分类                     LeetCode 75    中等   频率 ⭐⭐⭐⭐⭐  （双指针 / 荷兰国旗）
  - 第 30 题：最小覆盖子串                 LeetCode 76    困难   频率 ⭐⭐⭐⭐⭐  （滑动窗口）
  - 第 31 题：长度最小的子数组             LeetCode 209   中等   频率 ⭐⭐⭐⭐    （滑动窗口）
  - 第 32 题：替换后的最长重复字符         LeetCode 424   中等   频率 ⭐⭐⭐⭐    （滑动窗口）
  - 第 33 题：最大连续 1 的个数 III         LeetCode 1004  中等   频率 ⭐⭐⭐⭐    （滑动窗口）
  - 第 34 题：子数组最大平均数 I            LeetCode 643   简单   频率 ⭐⭐⭐     （定长滑动窗口）
  - 第 35 题：第一个错误的版本             LeetCode 278   简单   频率 ⭐⭐⭐⭐    （二分查找）
  - 第 36 题：寻找峰值                     LeetCode 162   中等   频率 ⭐⭐⭐⭐    （二分查找）
  - 第 37 题：寻找旋转排序数组中的最小值    LeetCode 153   中等   频率 ⭐⭐⭐⭐⭐  （二分查找）
  - 第 38 题：数组中的第 K 个最大元素       LeetCode 215   中等   频率 ⭐⭐⭐⭐⭐  （快速选择 / 堆）

运行方式：
    python LeetCode-Day11.py
会自动执行所有测试用例并打印 PASS / FAIL，全部通过即说明代码正确。

每个题目都包含：① 思路讲解 ② 流程示意图（ASCII）③ 可运行代码 ④ 复杂度分析 ⑤ 面试易错点。
只给一种「通用解法」，方便记忆和手撕。

今日主题：滑动窗口三连击 + 二分查找收尾 + 一个快速选择。
滑动窗口是面试手撕里性价比最高的套路——「连续子串/子数组 + 满足某条件的最小/最大长度」几乎都先想它。
二分查找在有序/有单调性数组上能 O(log n) 秒杀。今天把这两类模板彻底焊死。
"""

from collections import Counter, defaultdict


# ============================================================
# 第 29 题：颜色分类（LeetCode 75）
# ============================================================
"""
题目描述
--------
给定一个数组 nums，里面只有 0、1、2 三种值，要求「原地」把它排成
[所有 0][所有 1][所有 2] 的顺序。即 0 在最前，1 在中间，2 在最后。
要求只用常数额外空间，且只遍历一趟（one pass）最稳。

输入：nums = [2,0,2,1,1,0]  → [0,0,1,1,2,2]
输入：nums = [2,0,1]        → [0,1,2]

通用解法（荷兰国旗 / 三指针，最优且最经典）
------------------------------------------
用三个指针把数组切成四段：
    [0, left)      ：已经排好的 0
    [left, mid)    ：已经排好的 1
    [mid, right]   ：还没处理的区间（mid 正在扫）
    (right, n-1]   ：已经排好的 2
初始 left = mid = 0，right = n-1。mid 从左往右扫：
  - nums[mid] == 0：把它换到 left 的位置（left 是下一个该放 0 的坑），left++、mid++。
  - nums[mid] == 1：它本来就该待在中间段，啥也不做，mid++。
  - nums[mid] == 2：把它换到 right 的位置（right 是下一个该放 2 的坑），right--。
                    ⚠️ 注意：换过来的数还没检查过，所以 mid 不能 ++，留着下一轮再判断。
循环条件：while mid <= right（mid 越过 right 就说明 2 段之前的全处理完了）。

流程示意（nums = [2,0,2,1,1,0]，n=6）
--------------------------------------------------------------------------------
初始  left=0 mid=0 right=5   [0|0..5|5]  待处理全段
mid=0: nums[0]=2 → 换到 right(5): [0,0,2,1,1,2] right=4   mid 不动
mid=0: nums[0]=0 → 换到 left(0): 不变            left=1 mid=1
mid=1: nums[1]=0 → 换到 left(1): 不变            left=2 mid=2
mid=2: nums[2]=2 → 换到 right(4): [0,0,1,1,2,2] right=3   mid 不动
mid=2: nums[2]=1 → 中段，不动                    mid=3
mid=3: nums[3]=1 → 中段，不动                    mid=4
mid=4: 此时 mid=4 > right=3，循环结束
结果 [0,0,1,1,2,2]  ✓（left=2 之前是 0 段，left..right 是 1 段，之后是 2 段）

复杂度：
  时间 O(n)（每个元素最多被交换/访问常数次，mid 单向推进）
  空间 O(1)（原地，只用了几个指针）
面试易错点：
  - 遇到 2 换过来后「mid 不能 ++」，这是唯一最容易写错的点（换进来的数没验过）。
  - 循环条件是 mid <= right，不是 mid < right；否则会漏掉 right 位置的最后一个数。
  - 若只要「简单通用」不想记三指针，也可用计数法：扫一遍数出 0/1/2 个数，再原地覆盖。
    那是两趟、但不是「一趟」，面试里荷兰国旗更加分。
"""


def sort_colors(nums: list[int]) -> None:
    """原地排序 0/1/2（荷兰国旗三指针）。LeetCode 要求无返回值，直接改 nums。"""
    left = mid = 0
    right = len(nums) - 1
    while mid <= right:
        if nums[mid] == 0:
            nums[left], nums[mid] = nums[mid], nums[left]
            left += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[right] = nums[right], nums[mid]
            right -= 1
            # 注意：这里 mid 不前进，换过来的数下一轮再判断


# ============================================================
# 第 30 题：最小覆盖子串（LeetCode 76）
# ============================================================
"""
题目描述
--------
给定字符串 s 和 t，找出 s 中「包含 t 中所有字符（含重复次数）」的最短子串。
若不含则返回空串 ""。

输入：s = "ADOBECODEBANC", t = "ABC"   → "BANC"
输入：s = "a", t = "a"                 → "a"
输入：s = "a", t = "aa"                → ""（t 比 s 长，不可能）
输入：s = "aab", t = "ab"             → "ab"

通用解法（不定长滑动窗口 + 计数）
------------------------------------------
核心思想：用两个计数器，need 记「t 还需要多少」，window 记「当前窗口里有多少」。
  - need = Counter(t)：每种字符的目标次数（如 t="AAB" → A:2, B:1）。
  - 用 valid 记录「已经满足需求的字符种类数」；只有当 window[c] == need[c] 时才算这一
    类满足。valid == len(need) 时，窗口就「合法」了（包含了全部所需字符）。
  - right 向右扩张窗口；一旦合法，就尝试用 left 向右收缩，每缩一次都更新最短记录。
  - 收缩到不合法为止，再继续扩 right。这样 right 每到一个合法位置，left 都尽量贴着它。

流程示意（s="ADOBECODEBANC", t="ABC" → need={A:1,B:1,C:1}）
--------------------------------------------------------------------------------
right 扩到 'A'：window{A:1}            valid=1（A 满）
right 扩到 'AD'：window{A:1,D:1}       valid=1
right 扩到 'ADO'：valid=1
right 扩到 'ADOB'：window{A:1,B:1}     valid=2（A、B 满）
right 扩到 'ADOBE'：valid=2
right 扩到 'ADOBEC'：window{A:1,B:1,C:1} valid=3 == len(need) ★合法！
   记录窗口 "ADOBEC"(len=6)；收缩 left：出'A'→window{A:0} valid 掉到 2，停。
right 继续扩到 ... 'ADOBECODEBA'：window 里 A/B/C 又满（valid=3）★合法！
   记录窗口，收缩 left 直到不合法，最终 left 停在 'B'（索引 9）。
right 扩到末尾 'ADOBECODEBANC'：再次出现合法窗口，收缩 left 到 'BANC'(索引 9..12)。
   最终最短 = "BANC"(len=4)  ✓

复杂度：
  时间 O(|s| + |t|)（每个字符最多进窗口一次、出窗口一次）
  空间 O(|字符集|)（need 和 window 两个计数器，规模与字符种类有关，与长度无关）
面试易错点：
  - 用 Counter 时，t 里重复的字符（如 "AAB" 要 2 个 A）必须算够次数，不能只算种类。
  - 收缩窗口时，要先判断「要删的字符是不是 need 里的」，是才动 valid 和 window。
  - 返回前判断 min_len 是否还是初值（没找到任何合法窗口），没找到返回 ""。
"""


def min_window(s: str, t: str) -> str:
    """返回 s 中包含 t 全部字符的最短子串。滑动窗口 + 计数，O(|s|+|t|)。"""
    if not s or not t or len(t) > len(s):
        return ""
    need = Counter(t)
    window = defaultdict(int)
    valid = 0          # 已满足需求的字符种类数
    left = right = 0
    start = 0
    min_len = len(s) + 1

    while right < len(s):
        c = s[right]
        right += 1
        if c in need:
            window[c] += 1
            if window[c] == need[c]:      # 这种字符刚刚满足需求
                valid += 1
        # 窗口合法就尽可能地收缩 left
        while valid == len(need):
            if right - left < min_len:    # 更新最短窗口
                min_len = right - left
                start = left
            d = s[left]
            left += 1
            if d in need:
                if window[d] == need[d]:  # 删掉后这种字符不再满足需求
                    valid -= 1
                window[d] -= 1
    return "" if min_len == len(s) + 1 else s[start:start + min_len]


# ============================================================
# 第 31 题：长度最小的子数组（LeetCode 209）
# ============================================================
"""
题目描述
--------
给定一个正整数数组 nums 和一个整数 target，找出「和 >= target」的「最短连续子数组」的长度。
如果不存在返回 0。

输入：target = 7,  nums = [2,3,1,2,4,3]   → 2（子数组 [4,3] 和为 7，长度 2）
输入：target = 4,  nums = [1,4,4]         → 1（[4] 即可）
输入：target = 11, nums = [1,1,1,1,1,1,1,1] → 0（凑不出 11）

通用解法（滑动窗口，正数数组专用）
------------------------------------------
因为数组全是正整数，窗口里的和随 right 右移只增不减，随 left 右移只减不增——有单调性，
所以可以用滑动窗口：
  - right 向右走，把 nums[right] 加进窗口和 ssum；
  - 只要 ssum >= target，就记录当前长度，并尽量右移 left 缩小窗口（同时减去 nums[left]）；
  - 这样每个右端点对应「以它结尾的最短合法窗口」。

流程示意（target=7, nums=[2,3,1,2,4,3]）
--------------------------------------------------------------------------------
right=0 加 2   ssum=2   <7
right=1 加 3   ssum=5   <7
right=2 加 1   ssum=6   <7
right=3 加 2   ssum=8   >=7 → 记 len=4([2,3,1,2])；缩 left: 出2 ssum=6 <7 停
right=4 加 4   ssum=10  >=7 → 记 len=4([3,1,2,4])；缩: 出3 ssum=7 记 len=3([1,2,4]); 出1 ssum=6 <7 停
right=5 加 3   ssum=9   >=7 → 记 len=3([2,4,3]); 缩: 出2 ssum=7 记 len=2([4,3]); 出4 ssum=3 <7 停
最短长度 = 2  ✓

复杂度：
  时间 O(n)（right、left 各单向遍历一遍）
  空间 O(1)
面试易错点：
  - 数组是「正整数」才有单调性；若含负数/0，滑动窗口会失效，要换前缀和 + 有序结构。
  - 收缩时先判断 ssum >= target 再缩，别在 ssum < target 时也缩。
  - 初始 min_len 设为 n+1，最后若还是 n+1 说明没找到，返回 0。
"""


def min_sub_array_len(target: int, nums: list[int]) -> int:
    """返回和 >= target 的最短连续子数组长度；不存在返回 0。O(n)。"""
    left = 0
    ssum = 0
    min_len = len(nums) + 1
    for right in range(len(nums)):
        ssum += nums[right]
        while ssum >= target:
            min_len = min(min_len, right - left + 1)
            ssum -= nums[left]
            left += 1
    return 0 if min_len == len(nums) + 1 else min_len


# ============================================================
# 第 32 题：替换后的最长重复字符（LeetCode 424）
# ============================================================
"""
题目描述
--------
给你字符串 s 和整数 k，你可以把其中「最多 k 个」字符替换成任意字符。
求替换后能得到的最长「全由同一字符组成」的子串长度。

输入：s = "ABAB", k = 2          → 4（把两个 B 换成 A，得 "AAAA"）
输入：s = "AABABBA", k = 1       → 4（"AABA" 把中间的 B 换成 A 得 "AAAA"）
输入：s = "AAAA", k = 2          → 4（不用换）

通用解法（滑动窗口 + 记录窗口内最高频字符）
------------------------------------------
窗口内若「最长重复字符」出现 freq 次，那要把窗口变成全同字符，需要替换
(window_len - freq) 个字符。只要 (window_len - max_freq) <= k，窗口就合法（可全同）。
  - 用计数数组 counts 记窗口内各字母次数，max_freq 记其中最大值；
  - right 扩张；每次更新 max_freq；
  - 若 (right-left+1 - max_freq) > k，说明要替换的太多，右移 left 缩小窗口；
  - 每轮用当前窗口长度更新答案（窗口合法时长度即「可全同的最长长度」）。

流程示意（s="ABAB", k=2，max_freq 用历史最大值）
--------------------------------------------------------------------------------
right=0 'A': counts A=1 maxf=1  len=1  1-1=0<=2 → res=1
right=1 'B': counts B=1 maxf=1  len=2  2-1=1<=2 → res=2
right=2 'A': counts A=2 maxf=2  len=3  3-2=1<=2 → res=3
right=3 'B': counts B=2 maxf=2  len=4  4-2=2<=2 → res=4
答案 = 4  ✓（把两个 B 换成 A 即得 "AAAA"）

流程示意（s="AABABBA", k=1）
--------------------------------------------------------------------------------
right=0 'A': A=1 maxf=1 len=1 1-1=0<=1 res=1
right=1 'A': A=2 maxf=2 len=2 2-2=0<=1 res=2
right=2 'B': B=1 maxf=2 len=3 3-2=1<=1 res=3
right=3 'A': A=3 maxf=3 len=4 4-3=1<=1 res=4
right=4 'B': B=2 maxf=3 len=5 5-3=2>1 → 缩 left(出'A'): A=2,len=4 4-3=1<=1 res=4
right=5 'B': B=3 maxf=3 len=5 5-3=2>1 → 缩 left(出'A'): A=1,len=4 4-3=1<=1 res=4
right=6 'A': A=2 maxf=3 len=5 5-3=2>1 → 缩 left(出'B'): B=2,len=4 4-3=1<=1 res=4
答案 = 4  ✓

复杂度：
  时间 O(n)（right 单向遍历，left 也只右移；counts 是定长 26）
  空间 O(1)（长度 26 的计数数组）
面试易错点：
  - max_freq 取「历史最大值」不回退是常规写法（LC 测试下正确且简洁）；原理是答案只看最长合法窗口。
  - 判断条件用 (len - max_freq) > k；left 出窗口时记得 counts[出字符]--。
  - 题目保证大写英文字母，用 ord(ch)-65 映射下标即可；若含小写/其他要先 .upper() 归一化。
"""


def character_replacement(s: str, k: int) -> int:
    """最多替换 k 个字符后，能得到的全同字符最长子串长度。O(n)。"""
    left = 0
    counts = [0] * 26
    max_freq = 0
    res = 0
    for right in range(len(s)):
        # LeetCode 424 保证 s 只含大写英文字母，用 ord(ch)-65 映射到 0..25
        idx = ord(s[right]) - 65
        counts[idx] += 1
        max_freq = max(max_freq, counts[idx])
        # 需要替换的字符数 = 窗口长度 - 最高频字符数；超过 k 就缩窗口
        while right - left + 1 - max_freq > k:
            counts[ord(s[left]) - 65] -= 1
            left += 1
        res = max(res, right - left + 1)
    return res


# ============================================================
# 第 33 题：最大连续 1 的个数 III（LeetCode 1004）
# ============================================================
"""
题目描述
--------
二进制数组 nums（只含 0 和 1），你可以把「最多 k 个 0」翻转为 1。
求翻转后最长「全 1 连续子数组」的长度。

输入：nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2   → 6
输入：nums = [0,0,1,1,1,0,0], k = 0           → 3（不能翻，取最长原生 1 段）
输入：nums = [1,1,1,1,1], k = 1               → 5

通用解法（滑动窗口，本质是「窗口内 0 的个数 <= k」）
------------------------------------------
这是第 32 题在「只有 0/1」情形下的简化版：窗口内允许最多 k 个 0。
  - right 扩张，遇到 0 就把 zeros 计数 +1；
  - 一旦 zeros > k，右移 left 收缩，left 遇到 0 就把 zeros -1；
  - 每轮用当前窗口长度更新答案（此时窗口内 0 数一定 <= k，即「翻完能全 1」）。

流程示意（nums=[1,1,1,0,0,0,1,1,1,1,0], k=2，下标 0..10；零在 3,4,5,10）
--------------------------------------------------------------------------------
right=0..2 遇 1 不计数，zeros=0，窗口 0..2 len=3 res=3
right=3 '0': zeros=1 <=2 窗口 0..3 len=4 res=4
right=4 '0': zeros=2 <=2 窗口 0..4 len=5 res=5
right=5 '0': zeros=3 >2 → 缩 left: 出 nums[0]=1(zeros不变) left=1;
                         出 nums[1]=1 left=2; 出 nums[2]=1 left=3;
                         出 nums[3]=0 → zeros=2 left=4; 窗口 4..5 len=2
right=6 '1': zeros=2 窗口 4..6 len=3
right=7 '1': zeros=2 窗口 4..7 len=4
right=8 '1': zeros=2 窗口 4..8 len=5
right=9 '1': zeros=2 窗口 4..9 len=6 res=6
right=10 '0': zeros=3 >2 → 缩 left: 出 nums[4]=0 → zeros=2 left=5; 窗口 5..10 len=6
最终 res = 6  ✓（窗口 [4..9] = 0,0,1,1,1,1，翻两个 0 得六个 1）

复杂度：
  时间 O(n)（双指针单向）
  空间 O(1)
面试易错点：
  - 收缩时只有当 nums[left]==0 才把 zeros--，别无脑减（漏减会误判窗口非法）。
  - 第 32 题是本题的「通用升级版」（任意字符、不限 0/1），思路完全相通。
"""


def longest_ones(nums: list[int], k: int) -> int:
    """最多翻转 k 个 0 后，最长全 1 连续子数组长度。O(n)。"""
    left = 0
    zeros = 0
    res = 0
    for right in range(len(nums)):
        if nums[right] == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        res = max(res, right - left + 1)
    return res


# ============================================================
# 第 34 题：子数组最大平均数 I（LeetCode 643）
# ============================================================
"""
题目描述
--------
给定数组 nums 和整数 k，找一个「长度恰好为 k 的连续子数组」，使其平均数最大，返回该平均数。

输入：nums = [1,12,-5,-6,50,3], k = 3   → 15.66667（窗口 [50,3 前面的?] 实际是 [-6,50,3] 平均 47/3）
                                          （窗口分别是 [1,12,-5]=8、[12,-5,-6]=1、[-5,-6,50]=39、[-6,50,3]=47 → 最大 47/3≈15.67）
输入：nums = [5], k = 1                  → 5.0

通用解法（定长滑动窗口 + 维护窗口和）
------------------------------------------
长度固定为 k，滑动时「进一个新数、出一个旧数」即可在 O(1) 内更新窗口和：
  - 先算前 k 个的和 window_sum；
  - 从 i=k 开始，每步 window_sum += nums[i] - nums[i-k]（进 nums[i]、出 nums[i-k]）；
  - 用 window_sum 更新最大和，最后 /k 即最大平均数。
（平均数最大 ⇔ 和最大，因为长度固定。）

流程示意（nums=[1,12,-5,-6,50,3], k=3）
--------------------------------------------------------------------------------
初始窗口 [1,12,-5]  sum=8     max_sum=8
i=3 进 -6 出 1: sum=8-1+(-6)=1      max=8
i=4 进 50 出 12: sum=1-12+50=39     max=39
i=5 进 3  出 -5: sum=39-(-5)+3=47   max=47
最大平均 = 47/3 ≈ 15.66667  ✓

复杂度：
  时间 O(n)（只遍历一遍，窗口和更新 O(1)）
  空间 O(1)
面试易错点：
  - 平均 = 和 / k，不用每步都除（保留整数和最后除，避免浮点误差累积）。
  - 初始窗口和用 sum(nums[:k])，注意 k 可能等于 n（窗口就是整个数组）。
  - 返回浮点数，测试时用 abs(实际 - 期望) < 1e-6 比较。
"""


def find_max_average(nums: list[int], k: int) -> float:
    """返回长度恰为 k 的连续子数组中最大平均数。O(n)。"""
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]   # 进 nums[i]，出 nums[i-k]
        if window_sum > max_sum:
            max_sum = window_sum
    return max_sum / k


# ============================================================
# 第 35 题：第一个错误的版本（LeetCode 278）
# ============================================================
"""
题目描述
--------
有 n 个版本，编号 1..n。某个版本之后「全部」都是错误的（错误具有传递性）。
给一个 API isBadVersion(version) 返回该版本是否错误，请找出「第一个」错误的版本。
要求调用 isBadVersion 的次数尽可能少（O(log n)）。

输入：n = 5, 第一个错误版本 = 4   → 4（版本 1,2,3 正确，4,5 错误）
输入：n = 2, 第一个错误版本 = 2   → 2
输入：n = 1, 第一个错误版本 = 1   → 1

通用解法（二分查找，找「左边界」）
------------------------------------------
数组可看成 [F,F,F,T,T,T]，要找第一个 T 的下标。标准二分：
  - left=1, right=n；当 left < right 时：mid = (left+right)//2；
  - 若 isBadVersion(mid) 为 True，说明第一个错误版本在 mid 或它左边 → right=mid；
  - 否则 mid 还是好的，第一个错误版本在 mid 右边 → left=mid+1；
  - 退出时 left==right，就是答案。
（这里 mid 用 // 向下取整，配合 right=mid 不 +1，能避免死循环。）

流程示意（n=5, 错误从 4 开始；isBad: 1,2,3=F  4,5=T）
--------------------------------------------------------------------------------
left=1 right=5  mid=3 → isBad(3)=F → left=4
left=4 right=5  mid=4 → isBad(4)=T → right=4
left=4 right=4  退出，返回 4  ✓

复杂度：
  时间 O(log n)（每次砍一半）
  空间 O(1)
面试易错点：
  - mid = (left+right)//2（向下取整）；若写 (left+right+1)//2 配合 left=mid 会死循环，二选一要一致。
  - 当 mid 是错误版本时，让 right=mid（不能 right=mid-1，否则可能跳过真正的第一个）。
  - LeetCode 上 isBadVersion 是全局 API；本文件为了可运行，把它作为参数传进来（见测试）。
"""


def first_bad_version(n: int, is_bad) -> int:
    """给定 n 与 isBadVersion 判断函数，返回第一个错误版本编号。O(log n)。"""
    left, right = 1, n
    while left < right:
        mid = (left + right) // 2
        if is_bad(mid):
            right = mid
        else:
            left = mid + 1
    return left


# ============================================================
# 第 36 题：寻找峰值（LeetCode 162）
# ============================================================
"""
题目描述
--------
数组 nums 相邻元素互不相等。峰值元素指「比左右邻居都大」的元素，返回它的任意一个下标。
（数组两端视为负无穷，所以端点也可能成为峰值。）

输入：nums = [1,2,3,1]            → 2（nums[2]=3 比两边大）
输入：nums = [1,2,1,3,5,6,4]      → 1 或 5（值为 2 或 6 都行）
输入：nums = [1]                  → 0

通用解法（二分查找，O(log n)）
------------------------------------------
虽然数组整体无序，但有单调性可利用：比较 nums[mid] 与 nums[mid+1]。
  - 若 nums[mid] < nums[mid+1]：说明 mid 在「上坡」，峰值一定在右边（要么一直上到端点，
    端点即峰值；要么中途下坡形成峰）。→ left = mid + 1。
  - 否则（nums[mid] >= nums[mid+1]）：峰值在 mid 或 mid 左边。→ right = mid。
  - 退出时 left==right 即为一个峰值下标。

流程示意（nums=[1,2,1,3,5,6,4]）
--------------------------------------------------------------------------------
left=0 right=6  mid=3: nums[3]=3 < nums[4]=5 → 上坡，left=4
left=4 right=6  mid=5: nums[5]=6 > nums[6]=4 → 下坡，right=5
left=4 right=5  mid=4: nums[4]=5 < nums[5]=6 → 上坡，left=5
left=5 right=5  退出，返回 5（nums[5]=6 是峰值）✓

复杂度：
  时间 O(log n)
  空间 O(1)
面试易错点：
  - 这是「找任意一个峰值」，不是最大峰值，所以二分收敛到哪都合法。
  - 比较用 nums[mid] 和 nums[mid+1]（不是 mid-1），保证 mid+1 不越界（right 初始 n-1）。
  - 别写成找最大值的线性扫描——那是 O(n)，丢了二分的精髓。
"""


def find_peak(nums: list[int]) -> int:
    """返回数组任一峰值元素下标。O(log n)。"""
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < nums[mid + 1]:
            left = mid + 1        # 上坡，峰值在右边
        else:
            right = mid           # 下坡，峰值在 mid 或左边
    return left


# ============================================================
# 第 37 题：寻找旋转排序数组中的最小值（LeetCode 153）
# ============================================================
"""
题目描述
--------
一个「升序」数组在某个点被旋转了（如 [0,1,2,4,5,6,7] 旋成 [4,5,6,7,0,1,2]）。
数组里无重复元素。请找出其中的最小值。要求 O(log n)。

输入：nums = [3,4,5,1,2]          → 1
输入：nums = [4,5,6,7,0,1,2]      → 0
输入：nums = [11,13,15,17]        → 11（没旋转，最小值在开头）
输入：nums = [2,1]                → 1

通用解法（二分查找，利用「旋转点把数组分成两段升序」）
------------------------------------------
关键性质：以 nums[right] 为参照。
  - 若 nums[mid] > nums[right]：说明 mid 落在「左半段升序」上，而最小值（旋转点）一定在
    mid 右边。→ left = mid + 1。
  - 否则 nums[mid] <= nums[right]：最小值在 mid 或 mid 左边。→ right = mid。
  - 退出时 left==right 即最小值下标。

流程示意（nums=[4,5,6,7,0,1,2]）
--------------------------------------------------------------------------------
left=0 right=6  mid=3: nums[3]=7 > nums[6]=2 → 旋转点在右，left=4
left=4 right=6  mid=5: nums[5]=1 <= nums[6]=2 → 在左，right=5
left=4 right=5  mid=4: nums[4]=0 <= nums[5]=1 → 在左，right=4
left=4 right=4  退出，nums[4]=0 是最小值  ✓

复杂度：
  时间 O(log n)
  空间 O(1)
面试易错点：
  - 用 nums[right] 作参照（不是 nums[left]），这样能正确处理「没旋转」的情况。
  - 有重复元素时（LeetCode 154）要加 `nums[mid]==nums[right]` 时 right-=1 的退化处理；本题无重复，直接 <= 即可。
  - 这是二分里「找旋转点/最小值」的模板，和 36 题思路同源：用 mid 与某端比较决定收缩方向。
"""


def find_min(nums: list[int]) -> int:
    """返回旋转升序数组中的最小值。O(log n)。"""
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1       # 最小值在右半
        else:
            right = mid          # 最小值在 mid 或左半
    return nums[left]


# ============================================================
# 第 38 题：数组中的第 K 个最大元素（LeetCode 215）
# ============================================================
"""
题目描述
--------
给定整数数组 nums 和 k，返回「第 k 个最大」的元素（不是去重后的第 k 大，按排序后位置算；
如 [3,2,1,5,6,4] 降序是 6,5,4,3,2,1，第 2 大是 5）。要求平均 O(n)。

输入：nums = [3,2,1,5,6,4], k = 2              → 5
输入：nums = [3,2,3,1,2,4,5,5,6], k = 4        → 4
输入：nums = [1], k = 1                        → 1

通用解法（快速选择 Quickselect，平均 O(n)）
------------------------------------------
第 k 大 ⇔ 升序排列后「第 (n-k) 小」的元素（0 下标）。用快排的 partition 思想，但只递归
包含目标的那一侧，平均每次砍一半：
  1) 随机选一个 pivot，partition 把数组分成「< pivot | pivot | >= pivot」三部分，
     返回 pivot 最终落点的下标 p；
  2) 若 p == 目标下标，pivot 就是答案；
  3) 若目标在左，递归左段；否则递归右段。
不需要真的排序整个数组，所以平均 O(n)（快排是 O(n log n)，差别就在这）。

流程示意（nums=[3,2,1,5,6,4], 求第 2 大 ⇒ 找升序第 n-k = 6-2 = 4 小，下标 4）
--------------------------------------------------------------------------------
随机 pivot 假设选 4：partition 后 ~ [3,2,1,4,5,6]，pivot 下标 p=3
  目标下标 4 > 3 → 递归右段 [5,6]（在 p 右边）
右段随机 pivot 选 6：partition ~ [5,6]，p=1（相对右段）；原下标 = 3+1+1 = 5? 
  （实际实现用全局下标，这里略去细节）目标 4 < 5 → 递归左
最终收敛到升序第 4 小 = 5  ✓

复杂度：
  时间 平均 O(n)，最坏 O(n^2)（每次 pivot 都选到最值，随机化后几乎不会发生）
  空间 O(1)（原地 partition，递归栈平均 O(log n)）
面试易错点：
  - 第 k 大 = 升序第 (n-k) 小，下标别搞反。
  - 随机选 pivot 能避开最坏情况，面试时提一句「随机化防有序数组退化」。
  - 偷懒版：直接 sorted(nums)[-k]，或 heapq.nlargest(k, nums)[-1]，O(n log n)，
    面试若时间紧可先写这个再优化；但 Quickselect 才是体现功力的标准答法。
"""


def find_kth_largest(nums: list[int], k: int) -> int:
    """返回数组中第 k 大的元素。Quickselect，平均 O(n)。会原地修改 nums。"""
    import random

    def partition(left: int, right: int, pivot_idx: int) -> int:
        pivot = nums[pivot_idx]
        # 把 pivot 换到末尾，再从左到右把 < pivot 的聚到 store 位置
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        store = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[store], nums[i] = nums[i], nums[store]
                store += 1
        # 把 pivot 从末尾换回 store（它的正确位置）
        nums[right], nums[store] = nums[store], nums[right]
        return store

    def quickselect(left: int, right: int, k_smallest: int) -> int:
        if left == right:
            return nums[left]
        pivot_idx = random.randint(left, right)
        pivot_idx = partition(left, right, pivot_idx)
        if k_smallest == pivot_idx:
            return nums[k_smallest]
        elif k_smallest < pivot_idx:
            return quickselect(left, pivot_idx - 1, k_smallest)
        else:
            return quickselect(pivot_idx + 1, right, k_smallest)

    # 第 k 大 == 升序排列后第 (len-k) 个（0 下标）
    return quickselect(0, len(nums) - 1, len(nums) - k)


# ============================================================
# 测试运行：全部跑通即说明代码正确
# ============================================================
def _run_tests() -> None:
    print("=" * 66)
    print("LeetCode 必刷100题 · Day 11 自测")
    print("=" * 66)

    print("\n第 29 题：颜色分类（LeetCode 75）")
    a1 = [2, 0, 2, 1, 1, 0]; sort_colors(a1)
    ok1 = a1 == [0, 0, 1, 1, 2, 2]
    print(f"  [2,0,2,1,1,0] -> {a1}  期望 [0,0,1,1,2,2]  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    a2 = [2, 0, 1]; sort_colors(a2)
    ok2 = a2 == [0, 1, 2]
    print(f"  [2,0,1]       -> {a2}  期望 [0,1,2]        [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    a3 = [0]; sort_colors(a3)
    ok3 = a3 == [0]
    print(f"  [0]           -> {a3}  期望 [0]            [{'PASS' if ok3 else 'FAIL'}]"); assert ok3

    print("\n第 30 题：最小覆盖子串（LeetCode 76）")
    w1 = min_window("ADOBECODEBANC", "ABC")
    okw1 = w1 == "BANC"
    print(f"  'ADOBECODEBANC','ABC' -> {w1!r}  期望 'BANC'  [{'PASS' if okw1 else 'FAIL'}]"); assert okw1
    w2 = min_window("a", "a")
    okw2 = w2 == "a"
    print(f"  'a','a'              -> {w2!r}  期望 'a'     [{'PASS' if okw2 else 'FAIL'}]"); assert okw2
    w3 = min_window("a", "aa")
    okw3 = w3 == ""
    print(f"  'a','aa'             -> {w3!r}  期望 ''      [{'PASS' if okw3 else 'FAIL'}]"); assert okw3
    w4 = min_window("aab", "ab")
    okw4 = w4 == "ab"
    print(f"  'aab','ab'           -> {w4!r}  期望 'ab'    [{'PASS' if okw4 else 'FAIL'}]"); assert okw4

    print("\n第 31 题：长度最小的子数组（LeetCode 209）")
    s1 = min_sub_array_len(7, [2, 3, 1, 2, 4, 3])
    ok1 = s1 == 2
    print(f"  target=7,[2,3,1,2,4,3] -> {s1}  期望 2  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    s2 = min_sub_array_len(4, [1, 4, 4])
    ok2 = s2 == 1
    print(f"  target=4,[1,4,4]      -> {s2}  期望 1  [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    s3 = min_sub_array_len(11, [1, 1, 1, 1, 1, 1, 1, 1])
    ok3 = s3 == 0
    print(f"  target=11,全1长8      -> {s3}  期望 0  [{'PASS' if ok3 else 'FAIL'}]"); assert ok3

    print("\n第 32 题：替换后的最长重复字符（LeetCode 424）")
    c1 = character_replacement("ABAB", 2)
    okc1 = c1 == 4
    print(f"  'ABAB',k=2      -> {c1}  期望 4  [{'PASS' if okc1 else 'FAIL'}]"); assert okc1
    c2 = character_replacement("AABABBA", 1)
    okc2 = c2 == 4
    print(f"  'AABABBA',k=1   -> {c2}  期望 4  [{'PASS' if okc2 else 'FAIL'}]"); assert okc2
    c3 = character_replacement("AAAA", 2)
    okc3 = c3 == 4
    print(f"  'AAAA',k=2      -> {c3}  期望 4  [{'PASS' if okc3 else 'FAIL'}]"); assert okc3

    print("\n第 33 题：最大连续 1 的个数 III（LeetCode 1004）")
    o1 = longest_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2)
    oko1 = o1 == 6
    print(f"  [1,1,1,0,0,0,1,1,1,1,0],k=2 -> {o1}  期望 6  [{'PASS' if oko1 else 'FAIL'}]"); assert oko1
    o2 = longest_ones([0, 0, 1, 1, 1, 0, 0], 0)
    oko2 = o2 == 3
    print(f"  [0,0,1,1,1,0,0],k=0       -> {o2}  期望 3  [{'PASS' if oko2 else 'FAIL'}]"); assert oko2
    o3 = longest_ones([1, 1, 1, 1, 1], 1)
    oko3 = o3 == 5
    print(f"  [1,1,1,1,1],k=1           -> {o3}  期望 5  [{'PASS' if oko3 else 'FAIL'}]"); assert oko3

    print("\n第 34 题：子数组最大平均数 I（LeetCode 643）")
    m1 = find_max_average([1, 12, -5, -6, 50, 3], 3)
    okm1 = abs(m1 - 47 / 3) < 1e-6
    print(f"  [1,12,-5,-6,50,3],k=3 -> {m1:.5f}  期望 15.66667  [{'PASS' if okm1 else 'FAIL'}]"); assert okm1
    m2 = find_max_average([5], 1)
    okm2 = abs(m2 - 5.0) < 1e-6
    print(f"  [5],k=1               -> {m2:.5f}  期望 5.0      [{'PASS' if okm2 else 'FAIL'}]"); assert okm2

    print("\n第 35 题：第一个错误的版本（LeetCode 278）")
    fbv1 = first_bad_version(5, lambda v: v >= 4)
    okfb1 = fbv1 == 4
    print(f"  n=5,首个错误=4 -> {fbv1}  期望 4  [{'PASS' if okfb1 else 'FAIL'}]"); assert okfb1
    fbv2 = first_bad_version(1, lambda v: v >= 1)
    okfb2 = fbv2 == 1
    print(f"  n=1,首个错误=1 -> {fbv2}  期望 1  [{'PASS' if okfb2 else 'FAIL'}]"); assert okfb2
    fbv3 = first_bad_version(2, lambda v: v >= 2)
    okfb3 = fbv3 == 2
    print(f"  n=2,首个错误=2 -> {fbv3}  期望 2  [{'PASS' if okfb3 else 'FAIL'}]"); assert okfb3

    print("\n第 36 题：寻找峰值（LeetCode 162）")
    p1 = find_peak([1, 2, 3, 1])
    okp1 = nums_peak_ok([1, 2, 3, 1], p1)
    print(f"  [1,2,3,1]   -> {p1}  期望 2（峰=3）  [{'PASS' if okp1 else 'FAIL'}]"); assert okp1
    p2 = find_peak([1, 2, 1, 3, 5, 6, 4])
    okp2 = nums_peak_ok([1, 2, 1, 3, 5, 6, 4], p2)
    print(f"  [1,2,1,3,5,6,4] -> {p2}  期望 1 或 5  [{'PASS' if okp2 else 'FAIL'}]"); assert okp2
    p3 = find_peak([1])
    okp3 = p3 == 0
    print(f"  [1]        -> {p3}  期望 0  [{'PASS' if okp3 else 'FAIL'}]"); assert okp3

    print("\n第 37 题：寻找旋转排序数组中的最小值（LeetCode 153）")
    g1 = find_min([3, 4, 5, 1, 2])
    okg1 = g1 == 1
    print(f"  [3,4,5,1,2]       -> {g1}  期望 1  [{'PASS' if okg1 else 'FAIL'}]"); assert okg1
    g2 = find_min([4, 5, 6, 7, 0, 1, 2])
    okg2 = g2 == 0
    print(f"  [4,5,6,7,0,1,2]   -> {g2}  期望 0  [{'PASS' if okg2 else 'FAIL'}]"); assert okg2
    g3 = find_min([11, 13, 15, 17])
    okg3 = g3 == 11
    print(f"  [11,13,15,17]     -> {g3}  期望 11 [{'PASS' if okg3 else 'FAIL'}]"); assert okg3
    g4 = find_min([2, 1])
    okg4 = g4 == 1
    print(f"  [2,1]             -> {g4}  期望 1  [{'PASS' if okg4 else 'FAIL'}]"); assert okg4

    print("\n第 38 题：数组中的第 K 个最大元素（LeetCode 215）")
    k1 = find_kth_largest([3, 2, 1, 5, 6, 4], 2)
    okk1 = k1 == 5
    print(f"  [3,2,1,5,6,4],k=2 -> {k1}  期望 5  [{'PASS' if okk1 else 'FAIL'}]"); assert okk1
    k2 = find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4)
    okk2 = k2 == 4
    print(f"  [3,2,3,1,2,4,5,5,6],k=4 -> {k2}  期望 4  [{'PASS' if okk2 else 'FAIL'}]"); assert okk2
    k3 = find_kth_largest([1], 1)
    okk3 = k3 == 1
    print(f"  [1],k=1           -> {k3}  期望 1  [{'PASS' if okk3 else 'FAIL'}]"); assert okk3

    print("\n" + "=" * 66)
    print("✅ 今日 10 题全部测试用例通过！")
    print("   进度：已完成 38 / 100 题（Day 1-11）。")
    print("   下期预告（Day 12）：和为 K 的子数组 #560 / 连续子数组的最大和 #53 /")
    print("              乘积最大子数组 #152 / 除自身以外数组的乘积 #238 / 找到数组中重复的数字 #287 ...")
    print("=" * 66)


def nums_peak_ok(nums: list[int], idx: int) -> bool:
    """辅助：判断 idx 是不是 nums 的一个合法峰值下标。"""
    n = len(nums)
    left_ok = idx == 0 or nums[idx] > nums[idx - 1]
    right_ok = idx == n - 1 or nums[idx] > nums[idx + 1]
    return left_ok and right_ok


if __name__ == "__main__":
    _run_tests()
