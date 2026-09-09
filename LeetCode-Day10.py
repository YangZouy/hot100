"""
LeetCode 必刷100题 · Day 10（2026-07-25）
========================================
面试方向：AI 应用 / Agent 开发
今日题目（共 10 道，按面试高频顺序）：
  - 第 19 题：找到字符串中所有字母异位词     LeetCode 438   中等   频率 ⭐⭐⭐⭐⭐  （滑动窗口）
  - 第 20 题：验证回文串                   LeetCode 125   简单   频率 ⭐⭐⭐⭐⭐  （双指针）
  - 第 21 题：最长回文子串                 LeetCode 5     中等   频率 ⭐⭐⭐⭐⭐  （中心扩展）
  - 第 22 题：搜索插入位置                 LeetCode 35    简单   频率 ⭐⭐⭐⭐    （二分查找）
  - 第 23 题：在排序数组中查找元素的第一和最后位置  LeetCode 34  中等  频率 ⭐⭐⭐⭐   （二分查找）
  - 第 24 题：搜索旋转排序数组             LeetCode 33    中等   频率 ⭐⭐⭐⭐⭐  （二分查找）
  - 第 25 题：两数之和 II - 输入有序数组    LeetCode 167   中等   频率 ⭐⭐⭐⭐    （双指针）
  - 第 26 题：三数之和                     LeetCode 15    中等   频率 ⭐⭐⭐⭐⭐  （双指针 + 排序去重）
  - 第 27 题：盛最多水的容器               LeetCode 11    中等   频率 ⭐⭐⭐⭐⭐  （双指针）
  - 第 28 题：移除元素                     LeetCode 27    简单   频率 ⭐⭐⭐⭐    （双指针 / 快慢指针）

运行方式：
    python LeetCode-Day10.py
会自动执行所有测试用例并打印 PASS / FAIL，全部通过即说明代码正确。

每个题目都包含：① 思路讲解 ② 流程示意图（ASCII）③ 可运行代码 ④ 复杂度分析 ⑤ 面试易错点。
只给一种「通用解法」，方便记忆和手撕。

今日主题：双指针 / 二分查找 / 滑动窗口的「集中轰炸」。
这三类是 AI 应用/Agent 岗面试手撕里出现频率最高的基础套路——子串子数组先想滑动窗口，
有序数组先想二分，数组配对求和先想双指针。今天一口气刷这 10 道，把这些模板刻进肌肉记忆。
"""

# ============================================================
# 第 19 题：找到字符串中所有字母异位词（LeetCode 438）
# ============================================================
"""
题目描述
--------
给定两个字符串 s 和 p，找出 s 中所有 p 的「字母异位词」的起始索引。
返回的索引顺序不限。

输入：s = "cbaebabacd", p = "abc"  → [0, 6]
  （s[0:3]="cba" 是 "abc" 的异位词；s[6:9]="bac" 也是）
输入：s = "abab", p = "ab"         → [0, 1, 2]
输入：s = "aaaa", p = "aa"          → [0, 1, 2]
输入：s = "abc", p = "abcd"         → []（p 比 s 长，不可能有）

朴素想法（暴力）：
  枚举 s 中每个起点 i，截取长度为 len(p) 的子串，判断是否与 p 互为异位词。
  时间 O(n · k)（n=s 长度，k=p 长度），但每次判断又要排序或计数，整体慢且不优雅。

通用解法（定长滑动窗口 + 计数数组）
------------------------------------------
核心思想：异位词的充要条件是「字符计数完全相同」。
  1. 用一个长度 26 的数组 p_cnt 记录 p 里每个字母的出现次数。
  2. 在 s 上开一个「长度固定为 len(p)」的窗口，用 w_cnt 记录窗口内字符计数。
  3. 窗口从头滑到尾：每向右移一步，就把新进入的字符 +1、把离开的字符 -1，
     然后比较 w_cnt 与 p_cnt 是否相等，相等就记下窗口左端点的索引。
  为什么用「数组」而不是 Counter？
    数组下标直接对应字母（ord(ch)-97），比较时 list == list 逐元素比，O(1) 且写法干净，
    面试不容易写错。Counter 当然也行，但 list 更快更直观。

流程示意（s="cbaebabacd", p="abc"，窗口长 k=3）
--------------------------------------------------------------------------------
p_cnt = [a:1, b:1, c:1, 其余 0]
初始化窗口 = s[0:3]="cba" → w_cnt = [a:1,b:1,c:1] == p_cnt ✓ 记 0
i=3 进 'e' 出 'c'：窗口 "bae" → w_cnt=[a:1,b:1,e:1] != p_cnt
i=4 进 'b' 出 'b'：窗口 "aeb" → w_cnt=[a:1,b:1,e:1] != p_cnt
i=5 进 'a' 出 'e'：窗口 "eba" → w_cnt=[a:1,b:1,e:1] != p_cnt
i=6 进 'b' 出 'a'：窗口 "bab" → w_cnt=[a:1,b:2] != p_cnt
i=7 进 'a' 出 'b'：窗口 "aba" → w_cnt=[a:2,b:1] != p_cnt
i=8 进 'c' 出 'b'：窗口 "bac" → w_cnt=[a:1,b:1,c:1] == p_cnt ✓ 记 6
i=9 进 'd' 出 'a'：窗口 "acd" → != p_cnt
结果 [0, 6]  ✓

复杂度：
  时间 O(n + k)（n=len(s)，每个字符只进出窗口一次；建 p_cnt 用 O(k)）
  空间 O(1)（两个长度 26 的定长数组，与输入规模无关）
面试易错点：
  - 特判 len(p) > len(s) 直接返回 []，否则窗口永远开不起来会越界。
  - 滑动时「先加新字符、再减旧字符」，顺序无所谓，但别漏了减。
  - ord(ch) - 97 只适用于小写英文字母；本题保证如此。若含大写/数字，先 .lower() 或扩数组。
  - 比较用整段数组相等（w_cnt == p_cnt），别只比长度和。
"""


def find_anagrams(s: str, p: str) -> list[int]:
    """返回 s 中所有 p 的异位词起始索引。定长滑动窗口 + 计数数组，O(n+k)。"""
    # if len(p) > len(s):
    #     return []

    # k = len(p)
    # p_cnt = [0] * 26
    # w_cnt = [0] * 26

    # # 1) 统计 p 的字符计数
    # for ch in p:
    #     p_cnt[ord(ch) - 97] += 1
    # # 2) 初始化第一个窗口 s[0:k]
    # for i in range(k):
    #     w_cnt[ord(s[i]) - 97] += 1

    # res: list[int] = []
    # if w_cnt == p_cnt:          # 第一个窗口就命中
    #     res.append(0)

    # # 3) 窗口向右滑动：进 s[i]，出 s[i-k]
    # for i in range(k, len(s)):
    #     w_cnt[ord(s[i]) - 97] += 1          # 新字符进入窗口
    #     w_cnt[ord(s[i - k]) - 97] -= 1      # 旧字符离开窗口
    #     if w_cnt == p_cnt:
    #         res.append(i - k + 1)           # 窗口左端点索引
    # return res

# ============================================================
# 第 20 题：验证回文串（LeetCode 125）
# ============================================================
"""
题目描述
--------
给定一个字符串，判断它是否是「回文串」。
规则：只考虑字母和数字字符，忽略大小写（其它符号和空格全部忽略）。

输入："A man, a plan, a canal: Panama"  → True
输入："race a car"                       → False
输入：" "                                → True（过滤后为空，空串算回文）

通用解法（双指针，从两端向中间夹）
------------------------------------------
核心思想：左指针 left 从前往后，右指针 right 从后往前。
  1. 各自跳过「非字母数字」字符（用 str.isalnum() 判断）。
  2. 都比较到字母数字后，转小写比较是否相等；不等就不是回文。
  3. 直到 left >= right 还没发现不等，就是回文。

为什么用双指针而不是先清洗字符串？
  清洗（保留字母数字+转小写再反转比较）也能过，但双指针是「原地、O(1) 额外空间」的标准答法，
  面试更受青睐，也顺带展示了指针操作能力。

流程示意（s = "A man, a plan, a canal: Panama"）
--------------------------------------------------------------------------------
left=0('A')  right=last('a')  → 都转小写 'a'=='a'  ✓  left=1,right=...
跳过空格/逗号：left 移到 'm'，right 移到 'n'
'm'=='n'? 否 → 但实际字符串是回文，继续：
（简化）最终所有成对字符都相等，left 越过后 right，循环正常结束 → True

复杂度：
  时间 O(n)（每个字符最多被 left/right 各访问一次）
  空间 O(1)（只用了两个指针和临时变量）
面试易错点：
  - 忽略大小写：比较前务必 .lower()（或 .upper()），"A" 和 "a" 要相等。
  - 只判断字母？题目要求字母「和」数字都算；用 isalnum() 一次搞定，别自己写 a-z/A-Z/0-9 判断。
  - 空串或全是符号：过滤后 left==right 立即结束，返回 True，逻辑自然成立无需特判。
  - 内层两个 while 都要带 left < right 的保护，否则会越界或交叉。
"""


def is_palindrome(s: str) -> bool:
    """判断字符串是否为回文（只看字母数字、忽略大小写）。双指针，O(n)/O(1)。"""
    left, right = 0, len(s) - 1
    while left < right:
        # 左边跳过非字母数字
        while left < right and not s[left].isalnum():
            left += 1
        # 右边跳过非字母数字
        while left < right and not s[right].isalnum():
            right -= 1
        # 比较（忽略大小写）
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


# ============================================================
# 第 21 题：最长回文子串（LeetCode 5）
# ============================================================
"""
题目描述
--------
给定一个字符串 s，返回「最长的回文子串」。

输入："babad"  → "bab"（或 "aba"，二者任选其一即可）
输入："cbbd"   → "bb"
输入："a"      → "a"
输入："ac"     → "a"

朴素想法（暴力枚举所有子串 + 判断回文）：O(n³)，必超时。

通用解法（中心扩展法）
------------------------------------------
核心思想：回文串一定「关于某个中心」左右对称。
  一个长度为 n 的字符串有 2n-1 个「中心」：
    - n 个「字符中心」（回文长度为奇数，如 "aba" 中心是 'b'）
    - n-1 个「字符间隙中心」（回文长度为偶数，如 "bb" 中心在中间空隙）
  对每个中心，向左右同时扩展，只要两边字符相等就继续，直到不相等为止，
  记录这次扩展得到的回文长度。所有中心里最长的那个就是要的答案。

为什么不用 DP / Manacher？
  DP 是 O(n²) 空间，Manacher 是 O(n) 但代码极难记、面试容易写崩。
  中心扩展 O(n²) 时间、O(1) 空间，写法对称好记，是面试最稳的通用解。

流程示意（s = "babad"，以 i=1 的字符 'a' 为中心）
--------------------------------------------------------------------------------
center='a'(i=1)：
  l=1, r=1 → 相等, l=0,r=2：s[0]='b'==s[2]='b' 相等 → l=-1,r=3 停止
  本次回文长度 = r-l-1 = 3-0... 实际 = 3，子串 s[0:3]="bab"  ✓
另以 i=2 的字符 'b' 为中心也能扩到 "aba"，长度同为 3。
最终取最长 → "bab"（长度 3）

复杂度：
  时间 O(n²)（n 个中心，每个最多扩展 O(n)）
  空间 O(1)（只维护几个下标）
面试易错点：
  - 别忘了「偶数长度」的中心（间隙），只扩奇数会漏掉 "bb"、"abba" 这类。
  - 用闭区间 [l, r] 表示窗口，扩展后 l、r 都已越界，长度 = r - l - 1（不是 r - l + 1）。
  - 由长度反推起止下标：start = i - (len-1)//2，end = i + len//2，再 s[start:end+1]。
  - 空串特判返回 ""，否则循环不进也能正确返回 ""（start=end=0，s[0:1] 越界——所以先判空）。
"""


def longest_palindrome(s: str) -> str:
    """返回最长回文子串。中心扩展法，O(n²)/O(1)。"""
    if not s:
        return ""

    start, end = 0, -1   # 记录最长回文的 [start, end] 闭区间；end=-1 让 end-start 初值为 -1

    def expand(l: int, r: int) -> int:
        """从中心 (l, r) 向两边扩展，返回回文长度。"""
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return r - l - 1   # 越界后的长度

    for i in range(len(s)):
        len_odd = expand(i, i)       # 奇数长度（字符中心）
        len_even = expand(i, i + 1)  # 偶数长度（间隙中心）
        cur = max(len_odd, len_even)
        if cur > end - start + 1:   # end-start 是「当前最优长度-1」，+1 才等于当前最优长度
            # 由中心 i 和长度 cur 反推起止下标
            start = i - (cur - 1) // 2
            end = i + cur // 2
    return s[start:end + 1]


# ============================================================
# 第 22 题：搜索插入位置（LeetCode 35）
# ============================================================
"""
题目描述
--------
给定一个「升序无重复」的整数数组 nums 和目标值 target，
若找到则返回下标；若找不到，返回 target 「应该插入」以保持有序的位置下标。

输入：nums = [1,3,5,6], target = 5  → 2（正好在索引 2）
输入：nums = [1,3,5,6], target = 2  → 1（插在 1 和 3 之间）
输入：nums = [1,3,5,6], target = 7  → 4（插在末尾）
输入：nums = [1,3,5,6], target = 0  → 0（插在开头）

通用解法（二分查找）
------------------------------------------
核心思想：数组有序，直接二分。
  - nums[mid] == target → 直接返回 mid。
  - nums[mid] < target  → 目标在右半，left = mid + 1。
  - nums[mid] > target  → 目标在左半，right = mid - 1。
  当循环结束（left > right）仍没找到时，「left 恰好就是插入位置」。

为什么 left 就是插入点？（关键直觉）
  二分结束时 left 指向「第一个 ≥ target 的位置」：
  所有 < target 的都已被排除在 [0, left) 里，left 及之后都 ≥ target，
  所以把 target 放在 left 处能保持升序。这正是 lower_bound 的定义。

流程示意（nums=[1,3,5,6], target=2）
--------------------------------------------------------------------------------
left=0, right=3
mid=1 → nums[1]=3 > 2 → right=0
mid=0 → nums[0]=1 < 2 → left=1
left=1 > right=0 → 结束，返回 left=1  ✓

复杂度：
  时间 O(log n)（每次砍半）
  空间 O(1)
面试易错点：
  - 找不到时返回 left，不是 right、也不是 -1（很多人惯性写 -1）。
  - 循环条件用 left <= right（闭区间写法），mid 计算用 (left+right)//2。
  - 若数组可能为空，先判空返回 0。
  - 这题是「二分查找模板」的最简版，先把这套循环刻熟，后面 #33/#34 都是它的变体。
"""


def search_insert(nums: list[int], target: int) -> int:
    """在升序数组中查找 target，找不到则返回插入位置。二分查找，O(log n)。"""
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return left   # 循环结束，left 即插入位置


# ============================================================
# 第 23 题：在排序数组中查找元素的第一个和最后一个位置（LeetCode 34）
# ============================================================
"""
题目描述
--------
给定「升序」数组 nums（可能含重复）和 target，返回 target 在数组中
「出现的起始和结束下标」[first, last]；若没有出现，返回 [-1, -1]。

输入：nums = [5,7,7,8,8,10], target = 8  → [3, 4]
输入：nums = [5,7,7,8,8,10], target = 6  → [-1, -1]
输入：nums = [], target = 0              → [-1, -1]

通用解法（两次二分：lower_bound + upper_bound）
------------------------------------------
核心思想：把「找第一个/最后一个」拆成两个经典二分：
  - lower_bound：找「第一个 ≥ target」的下标（记为 lo）。
    若 lo 越界 或 nums[lo] != target → 不存在，返回 [-1,-1]。
  - upper_bound：找「第一个 > target」的下标（记为 hi）。
    第一个 > target 的前一个，就是最后一个等于 target 的位置 → last = hi - 1。
    （若 hi == -1 表示没有 > target 的，那 last 就是数组末尾。）

为什么不直接在 #22 基础上左右扫？
  左右扫在重复很多时会退化成 O(n)。用两次 O(log n) 二分才是正解，也是面试想看的。

流程示意（nums=[5,7,7,8,8,10], target=8）
--------------------------------------------------------------------------------
lower_bound（第一个 ≥ 8）：
  mid 遍历后定位到索引 3（值 8），lo = 3，nums[3]==8 ✓
upper_bound（第一个 > 8）：
  定位到索引 5（值 10），hi = 5
  last = hi - 1 = 4
→ [lo, last] = [3, 4]  ✓

复杂度：
  时间 O(log n)（两次二分）
  空间 O(1)
面试易错点：
  - 两个二分只有「比较符号」不同（>= vs >），其余完全一样，写错一个符号全错。
  - 必须先判 lo 是否真的等于 target，否则 target 不存在时不能算命中。
  - upper_bound 返回 -1（没有更大的）时，last 应取 len(nums)-1。
  - 空数组直接返回 [-1,-1]，避免下标越界。
"""


def search_range(nums: list[int], target: int) -> list[int]:
    """返回 target 在升序数组中的 [首, 尾] 下标；不存在返回 [-1,-1]。两次二分，O(log n)。"""
    if not nums:
        return [-1, -1]

    def lower_bound() -> int:
        """第一个 ≥ target 的下标，找不到返回 -1。"""
        l, r, ans = 0, len(nums) - 1, -1
        while l <= r:
            m = (l + r) // 2
            if nums[m] >= target:
                ans = m
                r = m - 1
            else:
                l = m + 1
        return ans

    def upper_bound() -> int:
        """第一个 > target 的下标，找不到返回 -1。"""
        l, r, ans = 0, len(nums) - 1, -1
        while l <= r:
            m = (l + r) // 2
            if nums[m] > target:
                ans = m
                r = m - 1
            else:
                l = m + 1
        return ans

    lo = lower_bound()
    if lo == -1 or nums[lo] != target:
        return [-1, -1]
    hi = upper_bound()
    last = len(nums) - 1 if hi == -1 else hi - 1
    return [lo, last]


# ============================================================
# 第 24 题：搜索旋转排序数组（LeetCode 33）
# ============================================================
"""
题目描述
--------
整数数组 nums 在「某个未知下标」被旋转过一次（原本升序、无重复），
例如 [0,1,2,4,5,6,7] 可能变成 [4,5,6,7,0,1,2]。
给定 target，若在其中返回下标，否则返回 -1。要求 O(log n)。

输入：nums = [4,5,6,7,0,1,2], target = 0  → 4
输入：nums = [4,5,6,7,0,1,2], target = 3  → -1
输入：nums = [1], target = 0              → -1

通用解法（二分 + 判断哪半边有序）
------------------------------------------
核心思想：虽然整体无序，但「任意一次二分后，至少有一半是有序的」。
  比较 nums[mid] 与 nums[left]：
    - 若 nums[left] <= nums[mid]：说明「左半边 [left, mid] 是连续升序的」。
        * 若 target 落在 [nums[left], nums[mid]) 区间 → 去左半边（right=mid-1）；
        * 否则去右半边（left=mid+1）。
    - 否则（左半边被旋转断开）：说明「右半边 [mid, right] 是连续升序的」。
        * 若 target 落在 (nums[mid], nums[right]] 区间 → 去右半边（left=mid+1）；
        * 否则去左半边（right=mid-1）。
  关键：用「有序的那一半」能否容纳 target 来决定收缩方向。

为什么至少有一半有序？
  旋转只是把数组切成两段升序再拼接，mid 把数组分成两半，两段中必有一段没被旋转点切断 → 完全升序。

流程示意（nums=[4,5,6,7,0,1,2], target=0）
--------------------------------------------------------------------------------
left=0, right=6, mid=3 → nums[3]=7
nums[left]=4 <= 7 → 左半 [4,5,6,7] 有序；target=0 不在 [4,7) → left=4
left=4, right=6, mid=5 → nums[5]=1
nums[left]=0 <= 1 → 左半 [0,1] 有序；target=0 在 [0,1) → right=4
left=4, right=4, mid=4 → nums[4]=0 == target → 返回 4  ✓

复杂度：
  时间 O(log n)（每次砍半）
  空间 O(1)
面试易错点：
  - 判断「左半有序」用 nums[left] <= nums[mid]（带等号，因为 left==mid 时显然有序）。
  - 区间判断用「闭区间包含」的逻辑：target 在有序半边的 [lo, mid) 或 (mid, hi] 内才往那半走。
  - 本题「无重复」，所以能用 <=；若有重复（LeetCode 81），需先去重再二分，难度升级。
  - 找不到返回 -1（循环结束 left>right 时）。
"""


def search(nums: list[int], target: int) -> int:
    """在旋转升序数组中查找 target，O(log n)。"""
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        # 左半边 [left, mid] 是否升序
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:  # 右半边 [mid, right] 升序
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1


# ============================================================
# 第 25 题：两数之和 II - 输入有序数组（LeetCode 167）
# ============================================================
"""
题目描述
--------
给定一个「升序」数组 numbers 和目标 target，找出两个数使它们的和等于 target。
返回这两个数的「1-based 下标」[index1, index2]（index1 < index2）。
保证恰有一个解，且不能重复使用同一个元素。

输入：numbers = [2,7,11,15], target = 9   → [1, 2]（2+7=9）
输入：numbers = [2,3,4], target = 6       → [1, 3]（2+4=6）
输入：numbers = [-1,0], target = -1        → [1, 2]（-1+0=-1）

通用解法（首尾双指针）
------------------------------------------
核心思想：数组已升序，用 left=0、right=尾 向中间夹：
  - sum = numbers[left] + numbers[right]
  - sum == target → 找到，返回 [left+1, right+1]（1-based）。
  - sum < target  → 和太小，left 右移让和变大。
  - sum > target  → 和太大，right 左移让和变小。
  为什么不会错过解？因为数组升序，移动较小端一定让和增大、移动较大端一定让和减小，
  每一步都「唯一」地朝目标逼近，必然命中（题目保证有解）。

和 #1 两数之和的区别：
  #1 无序 → 用哈希表 O(n)；本题有序 → 双指针 O(n) 且 O(1) 空间，更优。

流程示意（numbers=[2,7,11,15], target=9）
--------------------------------------------------------------------------------
left=0(2), right=3(15) → 17 > 9 → right=2
left=0(2), right=2(11) → 13 > 9 → right=1
left=0(2), right=1(7)  → 9 == 9 → 返回 [0+1, 1+1] = [1, 2]  ✓

复杂度：
  时间 O(n)（左右指针最多各走一遍）
  空间 O(1)
面试易错点：
  - 返回的是「1-based 下标」，记得各 +1；数组本身下标是 0-based。
  - 循环条件 left < right（不能相等，否则用了同一个元素）。
  - 指针移动方向：和小于 target 移 left（增大），大于移 right（减小），别反。
"""


def two_sum_ii(numbers: list[int], target: int) -> list[int]:
    """在升序数组中找两数之和等于 target，返回 1-based 下标。双指针，O(n)/O(1)。"""
    left, right = 0, len(numbers) - 1
    while left < right:
        s = numbers[left] + numbers[right]
        if s == target:
            return [left + 1, right + 1]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []   # 题目保证有解，这里仅为防御


# ============================================================
# 第 26 题：三数之和（LeetCode 15）
# ============================================================
"""
题目描述
--------
给定整数数组 nums，返回所有「不重复」的三元组 [a,b,c] 使 a+b+c=0。
答案中不能有重复的三元组（但三元组内部顺序不限）。

输入：nums = [-1,0,1,2,-1,-4]  → [[-1,-1,2],[-1,0,1]]
输入：nums = [0,1,1]            → []
输入：nums = [0,0,0]            → [[0,0,0]]

通用解法（排序 + 固定一个数 + 双指针）
------------------------------------------
核心思想：固定第一个数 nums[i]，问题变成「在 i 之后找两个数和为 -nums[i]」，
这就退化成了 #25 的「有序数组两数之和」，用双指针即可。
  1. 先 nums.sort() 升序。
  2. 枚举 i 从 0 到 n-3：
     - 若 nums[i] == nums[i-1]（且 i>0）→ 跳过，避免第一个数重复导致答案重复。
     - 令 target = -nums[i]，在 [i+1, n-1] 上用 left/right 双指针找和为 target 的两数。
     - 找到后加入答案，然后「跳过所有与当前 left/right 相同的数」避免重复。
  3. 返回所有收集到的三元组。

为什么要排序 + 跳重？
  不排序没法用双指针；不跳重会得到大量重复三元组（如 [-1,-1,2] 出现多次）。
  排序后「相同值必相邻」，用 while 跳过相邻重复项即可去重，这是三数之和的标准套路。

流程示意（nums=[-1,0,1,2,-1,-4] 排序后 → [-4,-1,-1,0,1,2]）
--------------------------------------------------------------------------------
i=0, nums[0]=-4, 找和为 4 → 无
i=1, nums[1]=-1, 找和为 1 → left=2(-1),right=5(2): -1+2=1 ✓ → [-1,-1,2]
       跳过重复 left/right，left=3,right=4: 0+1=1 ✓ → [-1,0,1]
i=2, nums[2]==nums[1] → 跳过（避免重复）
i=3, nums[3]=0, 找和为 0 → left=4,right=5: 1+2=3>0 不断右移 left 无解
结果 [[-1,-1,2],[-1,0,1]]  ✓

复杂度：
  时间 O(n²)（排序 O(n log n) + 外层 n 次、内层双指针 O(n)）
  空间 O(1)（不计返回结果；若算输出最坏 O(n²)）
面试易错点：
  - 必须先排序，双指针才有意义。
  - 去重有两处：① 固定数 i 与 i-1 相同要跳；② 找到一个解后，left/right 各自的重复都要跳。
  - 跳重要在「加入答案之后」再移动指针，顺序别乱。
  - 返回的是「值的列表」，不是下标；题目要的是三元组本身。
"""


def three_sum(nums: list[int]) -> list[list[int]]:
    """返回所有不重复的三元组使和为 0。排序 + 固定一个 + 双指针，O(n²)。"""
    nums.sort()
    res: list[list[int]] = []
    n = len(nums)

    for i in range(n):
        # 跳过重复的第一个数
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        target = -nums[i]
        left, right = i + 1, n - 1
        while left < right:
            s = nums[left] + nums[right]
            if s == target:
                res.append([nums[i], nums[left], nums[right]])
                # 跳过左侧重复
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # 跳过右侧重复
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif s < target:
                left += 1
            else:
                right -= 1
    return res


# ============================================================
# 第 27 题：盛最多水的容器（LeetCode 11）
# ============================================================
"""
题目描述
--------
给定 n 个非负整数 height[i]，代表竖线的高度。找出两条线，使它们与 x 轴
构成的容器能容纳「最多」的水，返回最大水量（面积）。

输入：height = [1,8,6,2,5,4,8,3,7]  → 49
  （选索引 1 的高 8 和索引 8 的高 7：面积 = min(8,7) × (8-1) = 7×7 = 49）
输入：height = [1,1]  → 1

通用解法（首尾双指针）
------------------------------------------
核心思想：容器面积 = min(height[left], height[right]) × (right - left)。
  初始 left=0、right=n-1，算面积后，移动「较矮」那一端的指针：
    - 为什么移矮的？因为面积受限于矮边，移动高边不可能让面积变大
      （宽度变小、高度上限还是矮边），而移动矮边「也许」能遇到更高的边让面积变大。
    - 每次都「有可能」找到更大面积，且每步宽度必减 1，左右指针相遇即结束。

为什么不会错过最优？
  反证：若最优解包含当前某一高边，而我们移走了矮边，那矮边本就不是最优的一部分，
  移走它不影响后续找到最优；若最优解含矮边……不动它时高边被移走的情况同理。
  严谨结论是：每次丢弃「不可能出现在更优解中」的那一侧，故不漏解。（面试能说清「移矮边」即可）

流程示意（height=[1,8,6,2,5,4,8,3,7]，简记）
--------------------------------------------------------------------------------
l=0(1) r=8(7)：面积=min(1,7)×8=8；左矮 → l=1
l=1(8) r=8(7)：面积=min(8,7)×7=49；右矮 → r=7
l=1(8) r=7(3)：面积=min(8,3)×6=18；右矮 → r=6
l=1(8) r=6(8)：面积=min(8,8)×5=40；等高，移任一侧(右) → r=5
l=1(8) r=5(4)：面积=min(8,4)×4=16；右矮 → r=4
l=1(8) r=4(5)：面积=min(8,5)×3=15；右矮 → r=3
l=1(8) r=3(2)：面积=min(8,2)×2=4；右矮 → r=2
l=1(8) r=2(6)：面积=min(8,6)×1=6；右矮 → r=1 相遇结束
最大面积 = 49  ✓

复杂度：
  时间 O(n)（左右指针各走一遍）
  空间 O(1)
面试易错点：
  - 移动「矮边」：height[left] < height[right] 移 left，否则移 right（等号移哪边都行）。
  - 面积是 min(高) × 宽，不是 max，别用错。
  - 宽度是 right - left（下标差），不是 right - left + 1（这是数组长度，不是间距）。
"""


def max_area(height: list[int]) -> int:
    """返回容器能容纳的最大水量。首尾双指针，O(n)/O(1)。"""
    left, right = 0, len(height) - 1
    ans = 0
    while left < right:
        h = min(height[left], height[right])
        ans = max(ans, h * (right - left))
        # 移动较矮的一侧
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return ans


# ============================================================
# 第 28 题：移除元素（LeetCode 27）
# ============================================================
"""
题目描述
--------
给定数组 nums 和值 val，「原地」移除所有等于 val 的元素，
返回移除后数组的新长度 k；要求：nums 的前 k 个元素为不等于 val 的元素
（顺序不限，超出 k 的部分无所谓）。

输入：nums = [3,2,2,3], val = 3  → 返回 2，nums 前 2 个变为 [2,2]
输入：nums = [0,1,2,2,3,0,4,2], val = 2  → 返回 5，前 5 个为 [0,1,3,0,4]
输入：nums = [1], val = 1         → 返回 0

通用解法（快慢指针 / 双指针原地覆盖）
------------------------------------------
核心思想：fast 指针负责「扫描全部元素」，slow 指针指向「下一个可写入的位置」。
  - fast 每看到一个不等于 val 的元素，就把它拷到 nums[slow]，slow 前进 1。
  - 等于 val 的元素直接跳过（fast 走、slow 不动）。
  结束时 slow 就是「留下来的元素个数」，且它们都紧挨在数组前端。

为什么叫「原地」？
  没有用额外数组，只是把有效元素往前挪（覆盖掉要删的），空间 O(1)。
  这是数组删除元素的通用模板（和 #283 移动零思路一致）。

流程示意（nums=[3,2,2,3], val=3）
--------------------------------------------------------------------------------
slow=0, fast=0: nums[0]=3==val → 跳过, fast=1
slow=0, fast=1: nums[1]=2≠val → nums[0]=2, slow=1, fast=2
slow=1, fast=2: nums[2]=2≠val → nums[1]=2, slow=2, fast=3
slow=2, fast=3: nums[3]=3==val → 跳过, fast=4 结束
返回 slow=2，nums 前 2 个 = [2,2]  ✓

复杂度：
  时间 O(n)（fast 扫一遍）
  空间 O(1)（原地修改）
面试易错点：
  - 返回的是 slow（长度），不是 fast；slow 才是「有效元素个数」。
  - 是 nums[slow] = nums[fast]（拷贝值），不是交换；要删的元素被后面有效元素覆盖即可。
  - 只保证前 k 个正确，题目允许 k 之后的内容任意，无需管。
  - 这是「原地删除」的万能模板，遇到「删除满足条件的元素」先想快慢指针。
"""


def remove_element(nums: list[int], val: int) -> int:
    """原地移除所有等于 val 的元素，返回新长度。快慢指针，O(n)/O(1)。"""
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != val:
            nums[slow] = nums[fast]
            slow += 1
    return slow


# ============================================================
# 测试用例：直接运行本文件即可验证
# ============================================================
def _run_tests() -> None:
    print("=" * 66)
    print("第 19 题：找到字符串中所有字母异位词（LeetCode 438）")
    print("=" * 66)
    t1 = find_anagrams("cbaebabacd", "abc")
    ok1 = t1 == [0, 6]
    print(f"  s='cbaebabacd', p='abc' -> {t1}  期望 [0, 6]  [{'PASS' if ok1 else 'FAIL'}]")
    assert ok1
    t2 = find_anagrams("abab", "ab")
    ok2 = t2 == [0, 1, 2]
    print(f"  s='abab', p='ab'       -> {t2}  期望 [0, 1, 2]  [{'PASS' if ok2 else 'FAIL'}]")
    assert ok2
    t3 = find_anagrams("aaaa", "aa")
    ok3 = t3 == [0, 1, 2]
    print(f"  s='aaaa', p='aa'       -> {t3}  期望 [0, 1, 2]  [{'PASS' if ok3 else 'FAIL'}]")
    assert ok3
    t4 = find_anagrams("abc", "abcd")
    ok4 = t4 == []
    print(f"  s='abc', p='abcd'      -> {t4}  期望 []  [{'PASS' if ok4 else 'FAIL'}]")
    assert ok4

    print("\n" + "=" * 66)
    print("第 20 题：验证回文串（LeetCode 125）")
    print("=" * 66)
    p1 = is_palindrome("A man, a plan, a canal: Panama")
    okp1 = p1 is True
    print(f"  'A man, a plan, a canal: Panama' -> {p1}  期望 True  [{'PASS' if okp1 else 'FAIL'}]")
    assert okp1
    p2 = is_palindrome("race a car")
    okp2 = p2 is False
    print(f"  'race a car'                    -> {p2}  期望 False  [{'PASS' if okp2 else 'FAIL'}]")
    assert okp2
    p3 = is_palindrome(" ")
    okp3 = p3 is True
    print(f"  ' ' (空格)                      -> {p3}  期望 True  [{'PASS' if okp3 else 'FAIL'}]")
    assert okp3
    p4 = is_palindrome("0P")
    okp4 = p4 is False
    print(f"  '0P'                            -> {p4}  期望 False  [{'PASS' if okp4 else 'FAIL'}]")
    assert okp4

    print("\n" + "=" * 66)
    print("第 21 题：最长回文子串（LeetCode 5）")
    print("=" * 66)
    l1 = longest_palindrome("babad")
    okl1 = l1 in ("bab", "aba") and len(l1) == 3
    print(f"  'babad' -> {l1!r}  期望 'bab' 或 'aba'  [{'PASS' if okl1 else 'FAIL'}]")
    assert okl1
    l2 = longest_palindrome("cbbd")
    okl2 = l2 == "bb"
    print(f"  'cbbd'  -> {l2!r}  期望 'bb'  [{'PASS' if okl2 else 'FAIL'}]")
    assert okl2
    l3 = longest_palindrome("a")
    okl3 = l3 == "a"
    print(f"  'a'     -> {l3!r}  期望 'a'  [{'PASS' if okl3 else 'FAIL'}]")
    assert okl3
    l4 = longest_palindrome("ac")
    okl4 = l4 == "a"
    print(f"  'ac'    -> {l4!r}  期望 'a'  [{'PASS' if okl4 else 'FAIL'}]")
    assert okl4

    print("\n" + "=" * 66)
    print("第 22 题：搜索插入位置（LeetCode 35）")
    print("=" * 66)
    s1 = search_insert([1, 3, 5, 6], 5)
    print(f"  [1,3,5,6], 5 -> {s1}  期望 2  [{'PASS' if s1 == 2 else 'FAIL'}]"); assert s1 == 2
    s2 = search_insert([1, 3, 5, 6], 2)
    print(f"  [1,3,5,6], 2 -> {s2}  期望 1  [{'PASS' if s2 == 1 else 'FAIL'}]"); assert s2 == 1
    s3 = search_insert([1, 3, 5, 6], 7)
    print(f"  [1,3,5,6], 7 -> {s3}  期望 4  [{'PASS' if s3 == 4 else 'FAIL'}]"); assert s3 == 4
    s4 = search_insert([1, 3, 5, 6], 0)
    print(f"  [1,3,5,6], 0 -> {s4}  期望 0  [{'PASS' if s4 == 0 else 'FAIL'}]"); assert s4 == 0

    print("\n" + "=" * 66)
    print("第 23 题：在排序数组中查找元素的第一和最后位置（LeetCode 34）")
    print("=" * 66)
    r1 = search_range([5, 7, 7, 8, 8, 10], 8)
    print(f"  [5,7,7,8,8,10], 8 -> {r1}  期望 [3, 4]  [{'PASS' if r1 == [3, 4] else 'FAIL'}]"); assert r1 == [3, 4]
    r2 = search_range([5, 7, 7, 8, 8, 10], 6)
    print(f"  [5,7,7,8,8,10], 6 -> {r2}  期望 [-1, -1]  [{'PASS' if r2 == [-1, -1] else 'FAIL'}]"); assert r2 == [-1, -1]
    r3 = search_range([], 0)
    print(f"  [], 0             -> {r3}  期望 [-1, -1]  [{'PASS' if r3 == [-1, -1] else 'FAIL'}]"); assert r3 == [-1, -1]
    r4 = search_range([2, 2], 2)
    print(f"  [2,2], 2          -> {r4}  期望 [0, 1]  [{'PASS' if r4 == [0, 1] else 'FAIL'}]"); assert r4 == [0, 1]

    print("\n" + "=" * 66)
    print("第 24 题：搜索旋转排序数组（LeetCode 33）")
    print("=" * 66)
    q1 = search([4, 5, 6, 7, 0, 1, 2], 0)
    print(f"  [4,5,6,7,0,1,2], 0 -> {q1}  期望 4  [{'PASS' if q1 == 4 else 'FAIL'}]"); assert q1 == 4
    q2 = search([4, 5, 6, 7, 0, 1, 2], 3)
    print(f"  [4,5,6,7,0,1,2], 3 -> {q2}  期望 -1  [{'PASS' if q2 == -1 else 'FAIL'}]"); assert q2 == -1
    q3 = search([1], 0)
    print(f"  [1], 0            -> {q3}  期望 -1  [{'PASS' if q3 == -1 else 'FAIL'}]"); assert q3 == -1
    q4 = search([5, 1, 3], 3)
    print(f"  [5,1,3], 3        -> {q4}  期望 2  [{'PASS' if q4 == 2 else 'FAIL'}]"); assert q4 == 2

    print("\n" + "=" * 66)
    print("第 25 题：两数之和 II - 输入有序数组（LeetCode 167）")
    print("=" * 66)
    w1 = two_sum_ii([2, 7, 11, 15], 9)
    print(f"  [2,7,11,15], 9  -> {w1}  期望 [1, 2]  [{'PASS' if w1 == [1, 2] else 'FAIL'}]"); assert w1 == [1, 2]
    w2 = two_sum_ii([2, 3, 4], 6)
    print(f"  [2,3,4], 6      -> {w2}  期望 [1, 3]  [{'PASS' if w2 == [1, 3] else 'FAIL'}]"); assert w2 == [1, 3]
    w3 = two_sum_ii([-1, 0], -1)
    print(f"  [-1,0], -1      -> {w3}  期望 [1, 2]  [{'PASS' if w3 == [1, 2] else 'FAIL'}]"); assert w3 == [1, 2]

    print("\n" + "=" * 66)
    print("第 26 题：三数之和（LeetCode 15）")
    print("=" * 66)
    th1 = three_sum([-1, 0, 1, 2, -1, -4])
    norm_th1 = sorted([sorted(t) for t in th1])
    expect_th1 = sorted([sorted(t) for t in [[-1, -1, 2], [-1, 0, 1]]])
    okth1 = norm_th1 == expect_th1
    print(f"  [-1,0,1,2,-1,-4] -> {th1}  期望 2 组  [{'PASS' if okth1 else 'FAIL'}]"); assert okth1
    th2 = three_sum([0, 1, 1])
    print(f"  [0,1,1]          -> {th2}  期望 []  [{'PASS' if th2 == [] else 'FAIL'}]"); assert th2 == []
    th3 = three_sum([0, 0, 0])
    print(f"  [0,0,0]          -> {th3}  期望 [[0,0,0]]  [{'PASS' if th3 == [[0, 0, 0]] else 'FAIL'}]"); assert th3 == [[0, 0, 0]]

    print("\n" + "=" * 66)
    print("第 27 题：盛最多水的容器（LeetCode 11）")
    print("=" * 66)
    m1 = max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])
    print(f"  [1,8,6,2,5,4,8,3,7] -> {m1}  期望 49  [{'PASS' if m1 == 49 else 'FAIL'}]"); assert m1 == 49
    m2 = max_area([1, 1])
    print(f"  [1,1]             -> {m2}  期望 1  [{'PASS' if m2 == 1 else 'FAIL'}]"); assert m2 == 1
    m3 = max_area([4, 3, 2, 1, 4])
    print(f"  [4,3,2,1,4]       -> {m3}  期望 16  [{'PASS' if m3 == 16 else 'FAIL'}]"); assert m3 == 16

    print("\n" + "=" * 66)
    print("第 28 题：移除元素（LeetCode 27）")
    print("=" * 66)
    nums1 = [3, 2, 2, 3]
    k1 = remove_element(nums1, 3)
    okk1 = k1 == 2 and sorted(nums1[:k1]) == [2, 2]
    print(f"  [3,2,2,3], val=3 -> 长度 {k1}, 前{k1}个={nums1[:k1]}  期望 2/[2,2]  [{'PASS' if okk1 else 'FAIL'}]"); assert okk1
    nums2 = [0, 1, 2, 2, 3, 0, 4, 2]
    k2 = remove_element(nums2, 2)
    okk2 = k2 == 5 and sorted(nums2[:k2]) == [0, 0, 1, 3, 4]
    print(f"  [0,1,2,2,3,0,4,2], val=2 -> 长度 {k2}, 前{k2}个={nums2[:k2]}  期望 5  [{'PASS' if okk2 else 'FAIL'}]"); assert okk2
    nums3 = [1]
    k3 = remove_element(nums3, 1)
    print(f"  [1], val=1 -> 长度 {k3}  期望 0  [{'PASS' if k3 == 0 else 'FAIL'}]"); assert k3 == 0

    print("\n" + "=" * 66)
    print("✅ 今日 10 题全部测试用例通过！")
    print("   进度：已完成 28 / 100 题（Day 1-10）。")
    print("=" * 66)


if __name__ == "__main__":
    _run_tests()
