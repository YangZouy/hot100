# -*- coding: utf-8 -*-
"""
================================================================================
LeetCode 必刷 100 题 · Day 17（总表 #90 ~ #99）
对应篇章：动态规划进阶收尾（背包 / 序列 DP / 单调栈 / 前缀树）
================================================================================

本文件是「可直接运行的 Python 文件」，不是文档。
运行方式（在你本机终端，cd 到本文件所在目录后执行）：
    python LeetCode-Day17.py
所有题目的测试用例会在运行时自动跑，结尾打印 PASS/FAIL 汇总。
只要看到 "全部通过 ✅"，就说明代码逻辑正确，可以放心交。

今天 10 道题（LeetCode 题号）：
    #90  打家劫舍 II          (213)   动态规划（环形 → 两次线性）
    #91  解码方法             (91)    动态规划（计数型 DP）
    #92  完全平方数           (279)   动态规划（完全背包变种）
    #93  分割等和子集         (416)   动态规划（0/1 背包 / 可行性）
    #94  零钱兑换             (322)   动态规划（完全背包 / 最小数量）
    #95  零钱兑换 II          (518)   动态规划（完全背包 / 组合数）
    #96  最长回文子序列       (516)   动态规划（区间 DP 二维模板）
    #97  接雨水               (42)    前后缀最值 / 双指针
    #98  柱状图中最大的矩形   (84)    单调栈（经典硬核题）
    #99  实现 Trie(前缀树)    (208)   数据结构设计（字典树）

为什么今天这样排？
    - #90 / #91 是「线性 DP」的收口：打家劫舍 II 把一维问题变成「两个一维取 max」，
      解码方法是「计数型 DP」的入门，两者都练「状态怎么定义、转移怎么写」。
    - #92 ~ #95 是背包四连击：完全平方数（完全背包求最小个数）、分割等和子集
      （0/1 背包求可行性）、零钱兑换（完全背包求最小数量）、零钱兑换 II
      （完全背包求组合数）。这 4 题吃透了，面试里 90% 的「选物品」类 DP 都跑不掉。
    - #96 是「二维区间 DP」的模板题，接雨水(#97)/柱状图(#98) 是单调栈/前后缀最值的
      双子星，Trie(#99) 是 AI 检索、自动补全、敏感词过滤的高频底层结构。

贯穿今天的解题心法：
    1) 背包类：先想「dp[j] 表示「容量为 j 时能不能/最多/最少/有多少种」，
       再决定「物品在外层还是内层」—— 求组合数必须「硬币在外层」。
    2) 二维 DP：先想 dp[i][j] 的「含义」，再写「转移方程」，最后补边界。
    3) 单调栈：维护一个「递增栈」，栈里存下标，遇到更小的值就把栈顶「结算」掉。
================================================================================
"""

from typing import List, Dict


# =============================================================================
# #90 打家劫舍 II (LeetCode 213)  —— 环形 → 两次线性 DP
# =============================================================================
def problem_90_rob_ii(nums: List[int]) -> int:
    r"""
    题目描述：
        你是一个专业的小偷，计划偷窃沿街的房屋。这回房屋围成一圈，
        意味着「第一间」和「最后一间」是相邻的——不能同时偷。
        给定每间房里的金额 nums，求今晚能偷到的最多金额。

    思路（把环拆成两段线性问题）：
        因为是环，最优解里「第 0 间」和「第 n-1 间」至少有一个不偷：
          - 方案 A：不偷第 0 间 → 在 nums[1..n-1] 上做「线性打家劫舍」；
          - 方案 B：不偷第 n-1 间 → 在 nums[0..n-2] 上做「线性打家劫舍」。
        两者取较大者，就是答案。
        线性打家劫舍（#89）的滚动写法：
            prev = 截止上一间的「最优」； curr = 截止当前间的「最优」
            走到 x：要么不偷 x（保持 curr），要么偷 x（prev + x）
            → 新 curr = max(curr, prev + x)

    图示（nums = [2,3,2]，环）：
             [0]=2 ── [1]=3 ── [2]=2
               \___________________/       首尾相邻，不能都偷
        方案 A：只看 [1,2]=[3,2] → 偷 3 → 3
        方案 B：只看 [0,1]=[2,3] → 偷 3 → 3
        答案 = max(3,3) = 3（偷中间那间）

    时间复杂度：O(n)，对两段各扫一遍。
    空间复杂度：O(1)，只用了几个滚动变量。

    面试易错点：
        - 别直接套线性版本就完事——环会导致首尾冲突，必须拆两段。
        - n==1 时特殊返回 nums[0]（不能取 nums[:-1] 和 nums[1:] 的 max 会算错）。
    """
    def rob_linear(arr: List[int]) -> int:
        prev = curr = 0
        for x in arr:
            prev, curr = curr, max(curr, prev + x)
        return curr

    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


# =============================================================================
# #91 解码方法 (LeetCode 91)  —— 计数型 DP
# =============================================================================
def problem_91_num_decodings(s: str) -> int:
    r"""
    题目描述：
        一条仅含数字的字符串 s，按 'A'->"1", 'B'->"2", ..., 'Z'->"26" 解码。
        求 s 一共有多少种解码方式。

    思路（dp[i] = 前 i 个字符的解码方法数）：
        空串有 1 种「什么都不做」的基准（dp[0]=1）。
        对第 i 位（对应 s[i-1]）：
          - 单字符：s[i-1] != '0' 时，可在前面所有方案后追加这个字母
            → dp[i] += dp[i-1]
          - 双字符：s[i-2:i] 在 10~26 之间时，可把这两位当成一个字母
            → dp[i] += dp[i-2]
        用 prev2=dp[i-2]、prev1=dp[i-1] 滚动即可，O(1) 空间。

    图示（s = "226"）：
             2    2    6
         dp: 1 -> 1 -> 2 -> 3
                 │      │
         单字符: 2→B   单:6→F  (dp[3]+=dp[2])
         双字符: 22→V  (dp[3]+=dp[1])
                 『2,2,6』『22,6』『2,26』共 3 种
        关键：'0' 不能单独解码（单字符加 0），必须依附在 10/20 上。

    时间复杂度：O(n)。
    空间复杂度：O(1)（滚动变量）。

    面试易错点：
        - 开头就是 '0' 直接返回 0；中间的 '0' 只能靠前一位组成 10/20 消化。
        - 用滚动变量时，prev2/prev1 的更新顺序别搞反。
    """
    if not s or s[0] == '0':
        return 0
    prev2 = 1   # dp[i-2]
    prev1 = 1   # dp[i-1]
    for i in range(1, len(s)):
        cur = 0
        if s[i] != '0':
            cur += prev1
        two = int(s[i - 1:i + 1])
        if 10 <= two <= 26:
            cur += prev2
        prev2, prev1 = prev1, cur
    return prev1


# =============================================================================
# #92 完全平方数 (LeetCode 279)  —— 完全背包求最小个数
# =============================================================================
def problem_92_num_squares(n: int) -> int:
    r"""
    题目描述：
        给定正整数 n，求「和为 n 的完全平方数的最少个数」。
        例：12 = 4+4+4 → 3 个；13 = 4+9 → 2 个。

    思路（完全背包 / 最值 DP）：
        dp[i] = 凑出和为 i 所需的最少平方数个数。
        基准 dp[0] = 0。
        对每个 i，枚举所有平方数 j*j<=i：
            dp[i] = min(dp[i], dp[i - j*j] + 1)
        这正是「物品可重复选、求最小数量」的完全背包。

    图示（n = 12）：
         平方数候选：1,4,9
         dp: dp[0]=0
             dp[4]  = dp[0]+1 = 1     (4)
             dp[8]  = dp[4]+1 = 2     (4+4)
             dp[12] = dp[8]+1 = 3     (4+4+4)   ← 最小
         （也试过 dp[12]=dp[3]+1、dp[12]=dp[11]+1，都不如 3 小）

    时间复杂度：O(n * sqrt(n))，每个 i 最多试 sqrt(i) 个平方数。
    空间复杂度：O(n)。

    面试易错点：
        - 初始化成无穷大，只有 dp[0]=0；别把 dp[0] 也设成 inf。
        - 数论彩蛋（四平方定理）：答案只可能是 1/2/3/4，但 DP 写法最通用稳妥。
    """
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1
    return dp[n]


# =============================================================================
# #93 分割等和子集 (LeetCode 416)  —— 0/1 背包（可行性）
# =============================================================================
def problem_93_can_partition(nums: List[int]) -> bool:
    r"""
    题目描述：
        给定一个非空正整数数组，判断是否「能把它分成和相等的两部分」。

    思路（等价成 0/1 背包可行性）：
        总和若为奇数 → 不可能平分，直接 False。
        令 target = sum/2。问题变成：能否从数组里挑一些数，恰好凑出 target？
        这正是「0/1 背包」：每个数选或不选，能否恰好装满容量 target。
        dp[s] = True 表示「能凑出和 s」。
        基准 dp[0] = True（什么都不选和为 0）。
        对每个数 num，从大到小更新：dp[s] |= dp[s-num]（s 从 target 倒着扫，
        保证每个数只被用一次）。

    图示（nums = [1,5,11,5]，sum=22，target=11）：
         能否凑出 11？
         选 {1,5,5} → 1+5+5 = 11 ✔  → 可以平分 {1,5,5} / {11}
         dp 递推：5 入袋后，dp[5],dp[6],dp[10],dp[11] 陆续变 True，
         最后 dp[11]==True → 返回 True。

    时间复杂度：O(n * target)。
    空间复杂度：O(target)。

    面试易错点：
        - 必判 sum 奇偶和 max(nums)>target，否则白算。
        - 内层循环必须「从大到小」，否则同一个数会被重复选成完全背包。
    """
    total = sum(nums)
    if total % 2 != 0:
        return False
    target = total // 2
    if max(nums) > target:
        return False

    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                dp[s] = True
    return dp[target]


# =============================================================================
# #94 零钱兑换 (LeetCode 322)  —— 完全背包求最小硬币数
# =============================================================================
def problem_94_coin_change(coins: List[int], amount: int) -> int:
    r"""
    题目描述：
        给定不同面额的硬币 coins 和总金额 amount，求「凑成 amount 的最少硬币数」。
        若无论如何都凑不出，返回 -1。

    思路（完全背包 / 最小数量）：
        dp[a] = 凑出金额 a 的最少硬币数，基准 dp[0] = 0，其余先设无穷大。
        对每个硬币（可重复用），从小到大更新：
            dp[a] = min(dp[a], dp[a - coin] + 1)
        最后 dp[amount] 仍是无穷大就说明凑不出，返回 -1。

    图示（coins=[1,2,5], amount=11）：
         dp[0]=0
         用 5: dp[5]=1, dp[10]=2
         用 2: dp[7]=dp[5]+1=2, dp[11]=dp[9]+1 ...
         用 1: 兜底
         最终 dp[11] = dp[6]+1 = dp[1]+1+1+1 = (1+5)+... = 3  (5+5+1 或 5+2+2+2)
         → 最少 3 枚

    时间复杂度：O(amount * len(coins))。
    空间复杂度：O(amount)。

    面试易错点：
        - 初始化为 inf 而非 0；dp[0]=0 是关键基准。
        - 凑不出时返回 -1，别返回 inf。
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1


# =============================================================================
# #95 零钱兑换 II (LeetCode 518)  —— 完全背包求组合数
# =============================================================================
def problem_95_change(coins: List[int], amount: int) -> int:
    r"""
    题目描述：
        给定硬币 coins 和金额 amount，求「凑成 amount 的组合数」
        （顺序不同但硬币集合相同算同一种，例如 [1,2] 和 [2,1] 只算 1 种）。

    思路（完全背包 / 组合数，和 #94 只差一行）：
        dp[a] = 凑出金额 a 的组合数，基准 dp[0] = 1（空组合）。
        关键：必须「硬币在外层、金额在内层」循环，
        这样才能保证每种组合里硬币按固定顺序出现，避免把 [1,2] 和 [2,1] 算两遍。
            for coin in coins:
                for a in range(coin, amount+1):
                    dp[a] += dp[a - coin]

    图示（coins=[1,2,5], amount=5）：
         只数「组合」：
          [1,1,1,1,1]
          [1,1,1,2]
          [1,2,2]
          [5]
         → 共 4 种
         若把内外层反过来（金额在外层），会多算出 [2,1,1,1] 等排列，答案就错了。

    时间复杂度：O(amount * len(coins))。
    空间复杂度：O(amount)。

    面试易错点：
        - 求「组合数」和「排列数」的唯一差别就是「硬币在外层还是内层」。
          记死：组合数 → 硬币在外层。
        - 基准是 dp[0]=1，不是 0。
    """
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]
    return dp[amount]


# =============================================================================
# #96 最长回文子序列 (LeetCode 516)  —— 二维区间 DP
# =============================================================================
def problem_96_longest_palindrome_subseq(s: str) -> int:
    r"""
    题目描述：
        给定字符串 s，求「最长的回文子序列的长度」（子序列可以不连续）。

    思路（区间 DP：dp[i][j] = s[i..j] 里的最长回文子序列长度）：
        - 单字符：dp[i][i] = 1。
        - 两端相等 s[i]==s[j]：首尾可以一起放进回文，dp[i][j] = dp[i+1][j-1] + 2。
        - 两端不等：去掉左端或去掉右端取较优，dp[i][j] = max(dp[i+1][j], dp[i][j-1])。
        按「区间长度」从短到长递推（长度 2 → n），保证算长区间时短区间已就绪。

    图示（s = "bbbab"，答案 "bbbb" 长度 4）：
         dp[i][j] 填表（只填右上三角 i<=j）：
              b  b  b  a  b
           b  1  2  3  3  4
           b     1  2  2  3
           b        1  1  3
           a           1  1
           b              1
         例如 dp[0][4]：s[0]=s[4]='b' → dp[1][3]+2 = 1+2 = 3? 实际是 4（bbbb），
         因为子区间会累积；最终 dp[0][4]=4。

    时间复杂度：O(n^2)。
    空间复杂度：O(n^2)。

    面试易错点：
        - 子序列「不连续」，和「子串」不同；别用滑窗做。
        - 递推必须按长度递增，否则会用到还没算好的短区间。
    """
    n = len(s)
    if n == 0:
        return 0
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1
    for length in range(2, n + 1):           # 区间长度从 2 开始
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                # 长度为 2 时 dp[i+1][j-1] 是「空区间」=0，初始化已是 0，正好
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]


# =============================================================================
# #97 接雨水 (LeetCode 42)  —— 前后缀最值
# =============================================================================
def problem_97_trap(height: List[int]) -> int:
    r"""
    题目描述：
        给定 n 个非负整数表示「柱子高度」，求下雨之后这些柱子之间能接多少雨水。

    思路（对每根柱子单独算它的积水量）：
        一根柱子 i 能接的水 = min(它左边最高, 它右边最高) - 它自己的高度，
        若结果 >0 才接得住水。
        所以先预处理两个数组：
          left_max[i]  = max(height[0..i])
          right_max[i] = max(height[i..n-1])
        然后 water += min(left_max[i], right_max[i]) - height[i]。

    图示（height = [0,1,0,2,1,0,1,3,2,1,2,1]）：
         3|        ■
         2|    ■   ■ ■   ■
         1|  ■ ■ ■ ■ ■ ■ ■ ■
         0|__■_■_■_■_■_■_■_■_■_■_■_■_■_■_■_■_■_■_■
            0 1 0 2 1 0 1 3 2 1 2 1
         例如下标4(高1)：左最高=2，右最高=3 → min=2，积水 2-1=1
         所有积水格加起来 = 6

    时间复杂度：O(n)，三遍扫描。
    空间复杂度：O(n)，两个最值数组。
    （面试常追问 O(1) 空间双指针版，思路相同：左右各一个指针，维护左右当前最大值。）

    面试易错点：
        - 积水是「凹槽」才存得住，凸起来的柱子自己不存水（min-自身=0）。
        - left_max/right_max 必须包含当前柱子本身，这样 min>=自身，不会出负数。
    """
    n = len(height)
    if n <= 2:
        return 0
    left_max = [0] * n
    right_max = [0] * n
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])
    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    water = 0
    for i in range(n):
        water += min(left_max[i], right_max[i]) - height[i]
    return water


# =============================================================================
# #98 柱状图中最大的矩形 (LeetCode 84)  —— 单调栈
# =============================================================================
def problem_98_largest_rectangle_area(heights: List[int]) -> int:
    r"""
    题目描述：
        给定 n 根柱子高度，求「能勾勒出的最大矩形面积」（矩形必须连续）。

    思路（单调递增栈：为每根柱子找「左右第一个更矮的边界」）：
        以第 i 根柱子为高 h 的最大矩形，宽度 = 右边界 - 左边界 - 1，
        其中「左边界」是左边第一个比 h 矮的位置，「右边界」是右边第一个比 h 矮的位置。
        用栈维护「下标递增、高度递增」：
          - 当前高度 h 比栈顶矮时，说明栈顶那根找到了右边界，把它弹出结算；
          - 结算时：高 = 弹出柱的高度，宽 = 当前 i - 新栈顶 - 1（新栈顶即左边界）；
          - 末尾加一根「高度 0」的哨兵，逼着把所有柱子都结算完。

    图示（heights = [2,1,5,6,2,3]）：
         6|       ■
         5|       ■ ■
         3|           ■
         2| ■     ■ ■ ■
         1| ■ ■   ■ ■ ■
         0|__■_■_■_■_■_■_■
            2 1 5 6 2 3
         以 5(下标2,高5)：左边界=1(高1)，右边界=4(高6) → 宽=4-1-1=2 → 面积10
         以 6(下标3,高6)：左边界=1，右边界=4 → 宽=2 → 面积12  ← 最大

    时间复杂度：O(n)，每个下标最多进栈出栈一次。
    空间复杂度：O(n)，栈。

    面试易错点：
        - 必须加「高度 0 哨兵」收尾，否则最后几根柱子结算不到。
        - 弹出后若栈空，左边界取 -1（表示一直延伸到最左）。
    """
    h = list(heights) + [0]          # 末尾哨兵，强制清空栈
    stack = []                       # 存「高度递增」的下标
    max_area = 0
    for i, cur_h in enumerate(h):
        while stack and cur_h < h[stack[-1]]:
            top = stack.pop()
            height = h[top]
            left = stack[-1] if stack else -1
            width = i - left - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area


# =============================================================================
# #99 实现 Trie(前缀树) (LeetCode 208)  —— 数据结构设计
# =============================================================================
class Trie:
    r"""
    题目描述：
        设计一个「前缀树（Trie）」，支持三种操作：
          insert(word)      插入一个单词
          search(word)      单词是否完整存在
          startsWith(pre)   是否有任意单词以 pre 为前缀

    思路（每个节点是一个 Trie，含「子节点字典」和「是否单词结尾」标志）：
        - 每个节点 children: 字符 -> 子节点。
        - is_end 标记「从根到该节点是否构成一个完整单词」。
        - insert：沿字符往下走，没有就新建节点，走完把末节点 is_end 置 True。
        - search：沿字符走，走不到就 False，走到末尾还要查 is_end（否则只是前缀）。
        - startsWith：同理，走到末尾即可，不要求 is_end。

    图示（插入 "apple" 和 "bee"）：
                 root
                /    \
              'a'    'b'
               |      |
              'p'    'e'
               |      |
              'p'    'e'  ← is_end=True ("bee")
               |
              'l'
               |
              'e'  ← is_end=True ("apple")
         search("app") → 走到 'p' 但 is_end=False → False（只是前缀）
         startsWith("app") → True
         search("apple") → True

    时间复杂度：每次操作 O(L)，L 为单词长度。
    空间复杂度：O(所有单词字符总数)。
    """

    def __init__(self) -> None:
        self.children: Dict[str, 'Trie'] = {}
        self.is_end: bool = False

    def insert(self, word: str) -> None:
        node = self
        for ch in word:
            if ch not in node.children:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True


# =============================================================================
# 测试区：运行本文件会自动执行下面的用例，结尾打印汇总
# =============================================================================
def _run_tests() -> None:
    passed = 0
    total = 0

    def check(name: str, got, expected) -> None:
        nonlocal passed, total
        total += 1
        ok = got == expected
        passed += 1 if ok else 0
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        if not ok:
            print(f"        期望: {expected}")
            print(f"        实际: {got}")

    # ---- #90 打家劫舍 II (213) ----
    print("\n#90 打家劫舍 II (213):")
    check("[2,3,2] -> 3", problem_90_rob_ii([2, 3, 2]), 3)
    check("[1,2,3,1] -> 4", problem_90_rob_ii([1, 2, 3, 1]), 4)
    check("[1,2,3] -> 3", problem_90_rob_ii([1, 2, 3]), 3)
    check("[5] -> 5", problem_90_rob_ii([5]), 5)

    # ---- #91 解码方法 (91) ----
    print("\n#91 解码方法 (91):")
    check("'12' -> 2", problem_91_num_decodings("12"), 2)
    check("'226' -> 3", problem_91_num_decodings("226"), 3)
    check("'0' -> 0", problem_91_num_decodings("0"), 0)
    check("'06' -> 0", problem_91_num_decodings("06"), 0)
    check("'10' -> 1", problem_91_num_decodings("10"), 1)
    check("'27' -> 1", problem_91_num_decodings("27"), 1)
    check("'261' -> 2", problem_91_num_decodings("261"), 2)

    # ---- #92 完全平方数 (279) ----
    print("\n#92 完全平方数 (279):")
    check("12 -> 3", problem_92_num_squares(12), 3)
    check("13 -> 2", problem_92_num_squares(13), 2)
    check("1 -> 1", problem_92_num_squares(1), 1)
    check("4 -> 1", problem_92_num_squares(4), 1)

    # ---- #93 分割等和子集 (416) ----
    print("\n#93 分割等和子集 (416):")
    check("[1,5,11,5] -> True", problem_93_can_partition([1, 5, 11, 5]), True)
    check("[1,2,3,5] -> False", problem_93_can_partition([1, 2, 3, 5]), False)
    check("[2,2,3,3,4] -> True (和14, 可拆 3+4)", problem_93_can_partition([2, 2, 3, 3, 4]), True)

    # ---- #94 零钱兑换 (322) ----
    print("\n#94 零钱兑换 (322):")
    check("[1,2,5],11 -> 3", problem_94_coin_change([1, 2, 5], 11), 3)
    check("[2],3 -> -1", problem_94_coin_change([2], 3), -1)
    check("[1],0 -> 0", problem_94_coin_change([1], 0), 0)
    check("[1,2,5],100 -> 20", problem_94_coin_change([1, 2, 5], 100), 20)

    # ---- #95 零钱兑换 II (518) ----
    print("\n#95 零钱兑换 II (518):")
    check("[1,2,5],5 -> 4", problem_95_change([1, 2, 5], 5), 4)
    check("[2],3 -> 0", problem_95_change([2], 3), 0)
    check("[1,2,5],11 -> 11", problem_95_change([1, 2, 5], 11), 11)

    # ---- #96 最长回文子序列 (516) ----
    print("\n#96 最长回文子序列 (516):")
    check("'bbbab' -> 4", problem_96_longest_palindrome_subseq("bbbab"), 4)
    check("'cbbd' -> 2", problem_96_longest_palindrome_subseq("cbbd"), 2)
    check("'a' -> 1", problem_96_longest_palindrome_subseq("a"), 1)
    check("'abcde' -> 1", problem_96_longest_palindrome_subseq("abcde"), 1)

    # ---- #97 接雨水 (42) ----
    print("\n#97 接雨水 (42):")
    check("[0,1,0,2,1,0,1,3,2,1,2,1] -> 6",
          problem_97_trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]), 6)
    check("[4,2,0,3,2,5] -> 9", problem_97_trap([4, 2, 0, 3, 2, 5]), 9)
    check("[1,0,2] -> 1", problem_97_trap([1, 0, 2]), 1)

    # ---- #98 柱状图中最大的矩形 (84) ----
    print("\n#98 柱状图中最大的矩形 (84):")
    check("[2,1,5,6,2,3] -> 10",
          problem_98_largest_rectangle_area([2, 1, 5, 6, 2, 3]), 10)
    check("[2,4] -> 4", problem_98_largest_rectangle_area([2, 4]), 4)
    check("[1] -> 1", problem_98_largest_rectangle_area([1]), 1)
    check("[2,1,2] -> 3", problem_98_largest_rectangle_area([2, 1, 2]), 3)

    # ---- #99 实现 Trie(前缀树) (208) ----
    print("\n#99 实现 Trie(前缀树) (208):")
    trie = Trie()
    trie.insert("apple")
    check("search('apple') -> True", trie.search("apple"), True)
    check("search('app') -> False", trie.search("app"), False)
    check("startsWith('app') -> True", trie.starts_with("app"), True)
    trie.insert("app")
    check("插入'app'后 search('app') -> True", trie.search("app"), True)
    trie.insert("bee")
    check("startsWith('be') -> True", trie.starts_with("be"), True)
    check("search('be') -> False", trie.search("be"), False)

    # ---- 汇总 ----
    print("\n" + "=" * 60)
    print(f"测试结果：{passed}/{total} 通过")
    if passed == total:
        print("全部通过 ✅  —— 今天的 10 题逻辑都正确，可以放心交。")
    else:
        print("有失败用例 ❌  —— 上面 FAIL 处已打印期望/实际，请检查。")
    print("=" * 60)


if __name__ == "__main__":
    _run_tests()
