# -*- coding: utf-8 -*-
"""
================================================================================
LeetCode 必刷 100 题 · Day 15（总表 #70 ~ #79）
对应篇章：回溯与递归篇（组合 / 排列 / 子集 / 棋盘类 DFS）
================================================================================

本文件是「可直接运行的 Python 文件」，不是文档。
运行方式（在你本机终端，cd 到本文件所在目录后执行）：
    python LeetCode-Day15.py
所有题目的测试用例会在运行时自动跑，结尾打印 PASS/FAIL 汇总。
只要看到 "全部通过 ✅"，就说明代码逻辑正确，可以放心交。

今天 10 道题（LeetCode 题号）：
    #70  最小路径和              (64)    动态规划（二维 → 一维）
    #71  三角形最小路径和        (120)   动态规划（自底向上 / 滚动数组）
    #72  子集                    (78)    回溯（选 / 不选）
    #73  子集 II                 (90)    回溯 + 去重
    #74  组合总和                (39)    回溯（可重复选）
    #75  组合总和 II             (40)    回溯 + 去重（每个只用一次）
    #76  组合总和 III            (216)   回溯（1~9 选 k 个数和为 n）
    #77  全排列                  (46)    回溯（used 数组）
    #78  全排列 II               (47)    回溯 + 去重（同层剪枝）
    #79  N 皇后                  (51)    回溯 + 列/对角线剪枝

为什么今天集中刷「回溯」？
    AI 应用 / Agent 开发面试里，回溯是「分治法 + 递归 + 剪枝」的集大成者。
    - 写 Agent 的工具调用规划、搜索树的剪枝，本质上就是回溯；
    - 多轮决策 + 撤销上一步（backtrack），和 Agent 的 plan/retry 一脉相承；
    - 面试官最爱问「子集 / 全排列 / 组合总和」三兄弟，因为它们
      长得像，但去重条件微妙不同 —— 这正是考察你有没有真懂。

通用心法（今天贯穿 10 题）：
    1) 先画「决策树」：每一步有哪几个分支？
    2) 每个分支做三件事：做选择 → 递归 → 撤销选择（回溯的精髓）。
    3) 去重只有两种套路：
       a. 同一层不能选相同的（i>start 且 nums[i]==nums[i-1] 跳过）
          —— 用于「子集 II / 组合总和 II」，因为元素可重复但组合不能重复。
       b. 同一层不能选「相同元素且上一个还没用」（not used[i-1] 跳过）
          —— 用于「全排列 II」，因为要的是不同排列而非不同组合。
    4) 递归出口写清楚：什么时候把 path 收进结果？
================================================================================
"""

from typing import List


# =============================================================================
# #70 最小路径和 (LeetCode 64)  —— 动态规划入门（二维 → 一维）
# =============================================================================
def problem_70_min_path_sum(grid: List[List[int]]) -> int:
    """
    题目描述：
        给定一个 m x n 的「非负整数网格」，找出一条从左上角 (0,0) 到右下角
        (m-1, n-1) 的路径，使得路径上的数字之和最小。
        每次只能「向下」或「向右」移动一步。

    思路（自顶向下递推，最直观的 DP）：
        定义 dp[i][j] = 从起点走到 (i,j) 的最小路径和。
        走到 (i,j) 只有两条来路：从上方 (i-1,j) 下来，或从左方 (i,j-1) 过来。
        所以：
            dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
        边界：
            - 第一行：只能从左边来 → dp[0][j] = dp[0][j-1] + grid[0][j]
            - 第一列：只能从上面来 → dp[i][0] = dp[i-1][0] + grid[i][0]
            - 起点：dp[0][0] = grid[0][0]

    空间优化（本题采用，O(1) 额外空间）：
        我们发现 dp[i][j] 只依赖「上一行同一列」和「本行左边」，
        因此根本不需要开整个 m×n 的表，直接在原 grid 上原地累加即可
        （grid 本就是我们要算的 dp 表）。
        注意：为了不破坏原函数外部传入的数组，这里先浅拷贝一层。

    ASCII 流程图（grid 与累加过程，示例 3×3）：
        原网格              累加后 dp 值（箭头=来路）
        1 3 1               ①1 → ②4 → ③5
        1 5 1               ↓   ↓↘  ↓
        4 2 1               ②2  ⑦7   ⑥6
                            ↓   ↓    ↓
                            ⑥6  ⑧8   ⑦7(答案)

        走到右下角 7 的最短路径：1→3→1→1→1（和为 7）

    复杂度：
        时间 O(m*n)（每个格子算一次），空间 O(1)（原地修改）。
    面试易错点：
        - 边界只能从一侧来，千万别对第一行/列也取 min（会越界）。
        - 若题目要求「不能修改原数组」，就新建一张 dp 表即可，逻辑不变。
    """
    if not grid or not grid[0]:
        return 0
    g = [row[:] for row in grid]          # 浅拷贝，不破坏原输入
    m, n = len(g), len(g[0])
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue                 # 起点不动
            elif i == 0:
                g[i][j] += g[i][j - 1]    # 第一行走左边
            elif j == 0:
                g[i][j] += g[i - 1][j]    # 第一列走上面
            else:
                g[i][j] += min(g[i - 1][j], g[i][j - 1])
    return g[m - 1][n - 1]


# =============================================================================
# #71 三角形最小路径和 (LeetCode 120)  —— DP 自底向上 + 滚动数组
# =============================================================================
def problem_71_minimum_total(triangle: List[List[int]]) -> int:
    """
    题目描述：
        给定一个「三角形」数组（triangle[i] 是第 i 行，长度 i+1）。
        从顶层出发，每一步只能走到「下一行相邻的位置」
        （即下一行的 j 或 j+1）。求从顶到底的最小路径和。

    思路（自底向上，最省空间的写法）：
        自顶向下的 DP 要处理「每行长度不同」，略麻烦。
        反过来想：从最后一行往上推。
        设 dp[j] 表示「从当前行第 j 个位置，走到最底层的最小和」。
        对于第 i 行第 j 个：
            dp[j] = triangle[i][j] + min(dp[j], dp[j+1])
        因为下一行相邻的就是 j 和 j+1，取它俩更小者即可。
        从最后一行开始，dp 初值 = 最后一行本身；
        逐行往上滚动，最后 dp[0] 就是从顶点出发的最小和。

    ASCII 流程图（示例三角形）：
            [2]                         dp = [2]
           [3,4]              → dp = [2+min(3,4), 3+min(4,?)] ... 见下
          [6,5,7]
         [4,1,8,3]            dp 初值 = [4,1,8,3]

        从底向上滚动（每个 dp[j] = 本行值 + min(下一行 j, 下一行 j+1)）：
        第3行(6,5,7)+下一行: 6+min(4,1)=7, 5+min(1,8)=6, 7+min(8,3)=10 → dp=[7,6,10]
        第2行(3,4)+下一行:   3+min(7,6)=9,  4+min(6,10)=10            → dp=[9,10]
        第1行(2)+下一行:     2+min(9,10)=11                              → dp=[11]
        答案 = 11（路径 2→3→5→1）

    复杂度：
        时间 O(n^2)（n 行，共约 n^2/2 个格子），空间 O(n)（只留一行 dp）。
    面试易错点：
        - 自顶向下容易在「越界 / 每行长度不同」上翻车；自底向上一行数组最稳。
        - 别写成「贪心」：每一步选小的（局部最优）≠全局最优，必须 DP。
    """
    if not triangle:
        return 0
    dp = triangle[-1][:]                  # 最后一行作为初值
    for i in range(len(triangle) - 2, -1, -1):
        row = triangle[i]
        for j in range(len(row)):
            dp[j] = row[j] + min(dp[j], dp[j + 1])
    return dp[0]


# =============================================================================
# #72 子集 (LeetCode 78)  —— 回溯「选 / 不选」的决策树
# =============================================================================
def problem_72_subsets(nums: List[int]) -> List[List[int]]:
    r"""
    题目描述：
        给定「不含重复元素」的整数数组 nums，返回所有可能的子集（幂集）。
        解集不能包含重复子集，元素顺序无关。

    思路（回溯模板·最通用）：
        对数组里每个数，都有「选」或「不选」两种可能，逐层决策。
        用一个 path 记录当前已选的，start 表示「本轮从哪个下标开始往后看」
        （避免回头选前面的，导致出现重复组合）。
        关键点：回溯的每一步（进入递归函数时）都要把当前 path 收集进结果，
        因为「每个节点都代表一个子集」。

    ASCII 决策树（nums=[1,2,3]，每层面对一个元素）：
                       []                       (根，先收一次空集)
              /          |          \
          选1           不选1
         [1]           []
        /   \          /   \
     选2   不选2     选2    不选2
     [1,2] [1]      [2]    []
     / \    / \     / \    / \
   选3 ...  ...    ...    ...  (叶子再各自收一次)

    最终 8 个子集：[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]

    复杂度：
        时间 O(n * 2^n)（共 2^n 个子集，每个复制一次约 O(n)），空间 O(n)（递归深度+path）。
    面试易错点：
        - 进入函数第一件事就 res.append(path[:])，不是只在叶子收！
        - path[:] 必须拷贝，否则后面 pop 会把已存进去的也改掉（经典坑）。
    """
    res: List[List[int]] = []
    path: List[int] = []

    def backtrack(start: int) -> None:
        res.append(path[:])                 # 每个节点都是一个合法子集
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1)                 # i+1：不回头，避免重复
            path.pop()                       # 回溯：撤销选择

    backtrack(0)
    return res


# =============================================================================
# #73 子集 II (LeetCode 90)  —— 回溯 + 同层去重
# =============================================================================
def problem_73_subsets_with_dup(nums: List[int]) -> List[List[int]]:
    r"""
    题目描述：
        给定「可能含重复元素」的整数数组 nums，返回所有不重复的子集。

    思路（在 #72 基础上加一道去重）：
        数组里有重复元素时，如果不处理，会出现一模一样的子集。
        去重原则：同一层递归里，如果当前数和「上一个数」相同，且上一个数
        本轮「没被跳过」（即 i>start 且 nums[i]==nums[i-1]），就跳过当前数。
        为什么是 i>start？因为同一分支内部连续选两个相同数是允许的
        （比如 [2,2] 可以选两次得到 [2,2]），只有「同一层」的重复才要剪掉。
        前置条件：必须先把 nums 排序，让相同元素挨在一起。

    ASCII 说明（nums=[1,2,2]，排序后还是 [1,2,2]）：
        第一层选 1 → 第二层面对 [2,2]：
            选第1个2 → path=[1,2]
            选第2个2：i=2>start 且 nums[2]==nums[1] → 跳过（避免 [1,2] 被重复造出）

    ASCII 决策树（nums=[1,2,2]）：
                   []
            /      |      \
         选1     选2(第1个)  选2(第2个)→ 同层重复，剪掉!
        [1]      [2]
        / \      / \
     选2 不选2  选2 不选2
    [1,2][1]  [2,2][2]

    最终 6 个子集：[], [1], [1,2], [1,2,2], [2], [2,2]

    复杂度：
        时间 O(n * 2^n)，空间 O(n)。
    面试易错点：
        - 一定先 sort！不去重会出重复，不排序去重就失效。
        - 剪枝条件是 i>start（同层），不是 i>0，理解错就会漏解或多解。
    """
    nums = sorted(nums)                    # 关键：相同元素聚到一起
    res: List[List[int]] = []
    path: List[int] = []

    def backtrack(start: int) -> None:
        res.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue                  # 同层重复元素，剪掉
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return res


# =============================================================================
# #74 组合总和 (LeetCode 39)  —— 回溯（同一个候选可重复选）
# =============================================================================
def problem_74_combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """
    题目描述：
        给定「无重复元素」的候选数组 candidates 和目标整数 target。
        找出所有使数字和为 target 的组合，candidates 中每个数可「无限次」使用，
        且解集不含重复组合。

    思路（回溯，递归传 start 而非 start+1）：
        从 start 下标开始往后尝试每个候选：
            - 选 candidates[i]，把剩余目标 remain 减去它，递归；
            - 递归时传 i（不是 i+1），表示「这一个还能继续选」→ 实现重复使用；
            - 当 remain == 0，说明凑齐了，收下当前 path；
            - 当 remain < 0，说明超了，剪枝返回。
        排序后还能加一句早停：candidates[i] > remain 时后面的更大，直接 break。

    ASCII 流程图（candidates=[2,3,6,7], target=7）：
        start=0, remain=7
        ├─选2 → remain=5
        │    ├─选2 → remain=3
        │    │    ├─选2 → remain=1
        │    │    │    ├─选2(>1)✗ 选3(>1)✗ … 都超 → 剪
        │    │    └─选3 → remain=0 ✅ 收 [2,2,3]
        │    └─选3 → remain=2 → 选2→0 ✅? 2+2+3 已覆盖 … 选3>2✗
        └─选7 → remain=0 ✅ 收 [7]

    答案：[[2,2,3],[7]]

    复杂度：
        时间取决于解的数量（指数级，但剪枝很强），空间 O(target/min)（递归深度）。
    面试易错点：
        - 「可重复」体现在递归传 i 而不是 i+1，这是和组合总和 II 的唯一区别。
        - 先排序才能用 remain<0 早停，且不排序也能出解只是慢一点。
    """
    candidates = sorted(candidates)
    res: List[List[int]] = []
    path: List[int] = []

    def backtrack(start: int, remain: int) -> None:
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break                          # 排序后早停
            path.append(candidates[i])
            backtrack(i, remain - candidates[i])   # 传 i：可重复选
            path.pop()

    backtrack(0, target)
    return res


# =============================================================================
# #75 组合总和 II (LeetCode 40)  —— 回溯 + 每个只用一次 + 去重
# =============================================================================
def problem_75_combination_sum2(candidates: List[int], target: int) -> List[List[int]]:
    """
    题目描述：
        候选数组「可能含重复元素」，每个数「只能用一次」，凑出和为 target 的组合，
        解集不含重复组合。

    思路（#74 + 去重）：
        1) 先排序，让相同候选相邻；
        2) 递归传 i+1（每个候选只用一次）；
        3) 去重：i>start 且 candidates[i]==candidates[i-1] 时跳过，
           含义是「同一层里，前面那个相同的数已经把以它开头的所有组合都试过了，
           当前这个数再选就会造出重复组合，剪掉」。

    ASCII 说明（candidates=[10,1,2,7,6,1,5] 排序后 [1,1,2,5,6,7,10], target=8）：
        第一层选第1个1 → 往下凑 7，能出 [1,1,6],[1,2,5],[1,7]
        第一层选第2个1：i>start 且与前一个1相同 → 跳过（避免 [1,2,5] 等被重复造）
        第一层选2 → 凑 6 → 出 [2,6]

    答案：[[1,1,6],[1,2,5],[1,7],[2,6]]

    复杂度：
        时间指数级（剪枝后尚可），空间 O(n)。
    面试易错点：
        - 去重条件 i>start 与「子集 II」完全一致，但递归传 i+1（每个只用一次）。
        - 别写成传 i（那样就变无限次用了，且去重逻辑会乱）。
    """
    candidates = sorted(candidates)
    res: List[List[int]] = []
    path: List[int] = []

    def backtrack(start: int, remain: int) -> None:
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break
            if i > start and candidates[i] == candidates[i - 1]:
                continue                        # 同层去重
            path.append(candidates[i])
            backtrack(i + 1, remain - candidates[i])   # i+1：每个只用一次
            path.pop()

    backtrack(0, target)
    return res


# =============================================================================
# #76 组合总和 III (LeetCode 216)  —— 回溯（1~9 选 k 个，和为 n）
# =============================================================================
def problem_76_combination_sum3(k: int, n: int) -> List[List[int]]:
    """
    题目描述：
        找出所有相加之和为 n 的 k 个数的组合，且满足：
        - 只使用数字 1 到 9；
        - 每个数字「最多使用一次」；
        - 返回所有可能的有效组合（数量不多于 9 个）。

    思路（典型的「限制长度的回溯」）：
        从 1 到 9 依次尝试，path 记录已选的数，递归时：
            - 长度达到 k 且剩余和为 0 → 收下；
            - 长度超 k 或剩余和 < 0 → 剪枝；
            - 否则继续往后选（i 从 start 到 9）。

    ASCII 说明（k=3, n=7）：
        选1(remain6)→选2(remain4)→选3(remain1,len3≠k)✗ → 选4(remain0,len3)✅[1,2,4]
        其它分支要么超长要么超和，最终只有 [1,2,4] 一组。

    k=3,n=7 → [[1,2,4]]
    k=3,n=9 → [[1,2,6],[1,3,5],[2,3,4]]

    复杂度：
        时间 O(C(9,k))（最多 9 选 k），空间 O(k)（递归深度）。
    面试易错点：
        - 出口要判断「长度 == k 且 remain == 0」，只判和会混入长度不对的组合。
        - 范围是 1~9 固定，循环到 9 即可，不用传 candidates。
    """
    res: List[List[int]] = []
    path: List[int] = []

    def backtrack(start: int, remain: int) -> None:
        if len(path) == k and remain == 0:
            res.append(path[:])
            return
        if len(path) > k or remain < 0:
            return
        for i in range(start, 10):
            path.append(i)
            backtrack(i + 1, remain - i)
            path.pop()

    backtrack(1, n)
    return res


# =============================================================================
# #77 全排列 (LeetCode 46)  —— 回溯（used 数组标记已用）
# =============================================================================
def problem_77_permute(nums: List[int]) -> List[List[int]]:
    """
    题目描述：
        给定「不含重复数字」的数组 nums，返回其所有可能的全排列。

    思路（used 标记法，最通用的排列回溯）：
        每一层都要从「所有数」里挑一个还没用过的放到当前位置。
        用 used[i] 记录 nums[i] 是否已经在当前 path 中（用过的不能再选，
        否则会重复使用同一个数）。
        path 长度 == len(nums) 时，说明排满了一组，收下。

    ASCII 决策树（nums=[1,2,3]，每层从「未用元素」里挑）：
        第1位: 1 / 2 / 3
        以第1位=1 为例：
            第2位: 从{2,3}挑 → 2 → 第3位剩3 → [1,2,3]
                                 → 3 → 第3位剩2 → [1,3,2]
        同理第1位=2、3 各出两组，共 6 组。

    答案（6 组）：[1,2,3][1,3,2][2,1,3][2,3,1][3,1,2][3,2,1]

    复杂度：
        时间 O(n! * n)（n! 个排列，每个复制 O(n)），空间 O(n)（used + 递归深度）。
    面试易错点：
        - 用 used 数组，不要靠「start 下标」——排列是「任意位置都能选」，
          和子集/组合（只能往后选）不一样。
        - path.pop() 后别忘了 used[i]=False，否则这个元素后面永远选不了。
    """
    res: List[List[int]] = []
    used = [False] * len(nums)
    path: List[int] = []

    def backtrack() -> None:
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack()
            path.pop()
            used[i] = False

    backtrack()
    return res


# =============================================================================
# #78 全排列 II (LeetCode 47)  —— 回溯 + 同层去重（not used[i-1]）
# =============================================================================
def problem_78_permute_unique(nums: List[int]) -> List[List[int]]:
    """
    题目描述：
        给定「可能含重复数字」的数组 nums，返回所有「不重复」的全排列。

    思路（#77 + 去重，剪枝条件最易写错的一题）：
        同样用 used 数组。排序让相同数字相邻。
        剪枝条件：if i>0 and nums[i]==nums[i-1] and not used[i-1]: continue
        含义拆解：
            - nums[i]==nums[i-1]：当前数和前一个相同；
            - not used[i-1]：前一个相同数「在当前层没被用」——
              说明它已经被试过并回溯撤销了，那当前这个数再选会造出相同排列，剪掉；
            - 如果 used[i-1] 为 True（前一个相同数正在 path 里），说明是「不同层」
              在连续选两个相同数，这是允许的（如 [1,1,2] 里两个 1 都要用）。
        一句话口诀：相同数，前一个没用时我才跳过；前一个正在用就说明是合法延续。

    ASCII 说明（nums=[1,1,2] 排序后一样）：
        第1位选第1个1 → 第2位可再选第2个1(used[0]=True,不剪)→[1,1,2]
                              也可选2 →[1,2,1]
        第1位选第2个1：i=1>0 且 nums[1]==nums[0] 且 not used[0](True) → 跳过
        → 不会出现重复的第1位为1分支。
        第1位选2 → [2,1,1]
        共 3 组：[1,1,2][1,2,1][2,1,1]

    复杂度：
        时间 O(n! * n)（同全排列，但剪掉大量重复），空间 O(n)。
    面试易错点：
        - 剪枝条件用「not used[i-1]」，不是「used[i-1]」，写反就漏解。
        - 必须先 sort，否则相同数不相邻，条件失效。
        - 和「子集 II / 组合总和 II」的 i>start 去重是不同套路，别混！
    """
    nums = sorted(nums)
    res: List[List[int]] = []
    used = [False] * len(nums)
    path: List[int] = []

    def backtrack() -> None:
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack()
            path.pop()
            used[i] = False

    backtrack()
    return res


# =============================================================================
# #79 N 皇后 (LeetCode 51)  —— 回溯 + 列/对角线剪枝（棋盘类 DFS）
# =============================================================================
def problem_79_solve_n_queens(n: int) -> List[List[str]]:
    """
    题目描述：
        在 n×n 的棋盘上放置 n 个皇后，使它们「互不攻击」
        （任意两个皇后不能在同一行、同一列、同一对角线）。
        返回所有可能的摆法，每种摆法用字符串列表表示（'Q' 表示皇后，'.' 表示空）。

    思路（按行回溯，三集合剪枝）：
        因为每行只能放一个皇后，所以「按行」逐层递归，每行选一个列 c。
        用三个集合记录「已被占用的列 / 主对角线 / 副对角线」：
            - 列：直接用 c；
            - 主对角线（左上→右下）：行-列 相等，用 (r-c) 标识；
            - 副对角线（右上→左下）：行+列 相等，用 (r+c) 标识。
        对某行 r，枚举每列 c，若 c / (r-c) / (r+c) 都没被占，就放下皇后，
        递归下一行；递归回来后撤销（从三个集合里移除、把格子复原）。
        递归到第 n 行（r==n），说明 n 个都放好了，收下当前棋盘。

    ASCII 说明（n=4，一种合法解）：
        . Q . .
        . . . Q
        Q . . .
        . . Q .
        列占用 {1,3,0,2}；主对角 r-c ∈ {0,-2,2,1}；副对角 r+c ∈ {1,3,2,5}，互不冲突。

    n=4 → 2 种解；n=1 → 1 种（[Q]）；n=2/n=3 → 0 种（无解）。

    复杂度：
        时间 O(n!)（每步可选列数递减，剪枝后远小于全排列），空间 O(n)（集合+递归）。
    面试易错点：
        - 对角线标识用「行-列」和「行+列」是经典技巧，别用斜率（浮点不可靠）。
        - 收结果时要把 board（二维字符数组）转成字符串列表的副本，
          否则后续回溯改掉 board 会把已存的解也改了。
        - n=2/3 无解要能想到（不是代码 bug）。
    """
    res: List[List[str]] = []
    cols = set()
    diag1 = set()         # r - c
    diag2 = set()         # r + c
    board = [['.'] * n for _ in range(n)]

    def backtrack(r: int) -> None:
        if r == n:
            res.append([''.join(row) for row in board])   # 转字符串副本收下
            return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)
            board[r][c] = 'Q'
            backtrack(r + 1)
            board[r][c] = '.'                              # 撤销
            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)

    backtrack(0)
    return res


# =============================================================================
# 测试区：运行本文件会自动执行下面的用例，结尾打印汇总
# =============================================================================
def _normalize(subsets: List[List[int]]):
    """把多组列表规范化成「排序后的元组集合」，方便忽略内部顺序地比较答案。"""
    return set(tuple(sorted(s)) for s in subsets)


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

    print("=" * 60)
    print("Day 15 自动化测试开始")
    print("=" * 60)

    # ---- #70 最小路径和 (64) ----
    print("\n#70 最小路径和 (64):")
    check("3x3 网格",
          problem_70_min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]), 7)
    check("单行",
          problem_70_min_path_sum([[1, 2, 3]]), 6)
    check("单列",
          problem_70_min_path_sum([[1], [2], [3]]), 6)

    # ---- #71 三角形最小路径和 (120) ----
    print("\n#71 三角形最小路径和 (120):")
    check("4 层三角形",
          problem_71_minimum_total([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]), 11)
    check("2 层三角形",
          problem_71_minimum_total([[-10], [1, 2]]), -9)
    check("单行",
          problem_71_minimum_total([[-1]]), -1)

    # ---- #72 子集 (78) ----
    print("\n#72 子集 (78):")
    check("nums=[1,2,3]",
          _normalize(problem_72_subsets([1, 2, 3])),
          _normalize([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]))
    check("nums=[0]",
          _normalize(problem_72_subsets([0])),
          _normalize([[], [0]]))

    # ---- #73 子集 II (90) ----
    print("\n#73 子集 II (90):")
    check("nums=[1,2,2]",
          _normalize(problem_73_subsets_with_dup([1, 2, 2])),
          _normalize([[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]))
    check("nums=[4,4,4,1]",
          _normalize(problem_73_subsets_with_dup([4, 4, 4, 1])),
          _normalize([[], [1], [4], [4, 4], [4, 4, 4], [1, 4],
                      [1, 4, 4], [1, 4, 4, 4]]))

    # ---- #74 组合总和 (39) ----
    print("\n#74 组合总和 (39):")
    check("c=[2,3,6,7] t=7",
          _normalize(problem_74_combination_sum([2, 3, 6, 7], 7)),
          _normalize([[2, 2, 3], [7]]))
    check("c=[2,3,5] t=8",
          _normalize(problem_74_combination_sum([2, 3, 5], 8)),
          _normalize([[2, 2, 2, 2], [2, 3, 3], [3, 5]]))

    # ---- #75 组合总和 II (40) ----
    print("\n#75 组合总和 II (40):")
    check("c=[10,1,2,7,6,1,5] t=8",
          _normalize(problem_75_combination_sum2([10, 1, 2, 7, 6, 1, 5], 8)),
          _normalize([[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]))
    check("c=[2,5,2,1,2] t=5",
          _normalize(problem_75_combination_sum2([2, 5, 2, 1, 2], 5)),
          _normalize([[1, 2, 2], [5]]))

    # ---- #76 组合总和 III (216) ----
    print("\n#76 组合总和 III (216):")
    check("k=3 n=7",
          _normalize(problem_76_combination_sum3(3, 7)),
          _normalize([[1, 2, 4]]))
    check("k=3 n=9",
          _normalize(problem_76_combination_sum3(3, 9)),
          _normalize([[1, 2, 6], [1, 3, 5], [2, 3, 4]]))

    # ---- #77 全排列 (46) ----
    print("\n#77 全排列 (46):")
    check("nums=[1,2,3]",
          _normalize(problem_77_permute([1, 2, 3])),
          _normalize([[1, 2, 3], [1, 3, 2], [2, 1, 3],
                      [2, 3, 1], [3, 1, 2], [3, 2, 1]]))
    check("nums=[0,1]",
          _normalize(problem_77_permute([0, 1])),
          _normalize([[0, 1], [1, 0]]))

    # ---- #78 全排列 II (47) ----
    print("\n#78 全排列 II (47):")
    check("nums=[1,1,2]",
          _normalize(problem_78_permute_unique([1, 1, 2])),
          _normalize([[1, 1, 2], [1, 2, 1], [2, 1, 1]]))
    check("nums=[1,2,3] (无重复也应 6 组)",
          _normalize(problem_78_permute_unique([1, 2, 3])),
          _normalize([[1, 2, 3], [1, 3, 2], [2, 1, 3],
                      [2, 3, 1], [3, 1, 2], [3, 2, 1]]))

    # ---- #79 N 皇后 (51) ----
    print("\n#79 N 皇后 (51):")
    n4 = problem_79_solve_n_queens(4)
    check("n=4 解的数量", len(n4), 2)
    check("n=4 含已知解",
          (".Q..", "...Q", "Q...", "..Q.") in [tuple(b) for b in n4], True)
    check("n=1 解的数量", len(problem_79_solve_n_queens(1)), 1)
    check("n=2 无解", len(problem_79_solve_n_queens(2)), 0)
    check("n=3 无解", len(problem_79_solve_n_queens(3)), 0)

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
