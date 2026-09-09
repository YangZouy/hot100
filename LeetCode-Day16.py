# -*- coding: utf-8 -*-
"""
================================================================================
LeetCode 必刷 100 题 · Day 16（总表 #80 ~ #89）
对应篇章：回溯收尾 + 图论基础 + 动态规划进阶起点
================================================================================

本文件是「可直接运行的 Python 文件」，不是文档。
运行方式（在你本机终端，cd 到本文件所在目录后执行）：
    python LeetCode-Day16.py
所有题目的测试用例会在运行时自动跑，结尾打印 PASS/FAIL 汇总。
只要看到 "全部通过 ✅"，就说明代码逻辑正确，可以放心交。

今天 10 道题（LeetCode 题号）：
    #80  单词搜索          (79)    回溯（网格 DFS）
    #81  岛屿数量          (200)   DFS/BFS 洪泛（连通块计数）
    #82  课程表            (207)   拓扑排序（判环 / 可行性）
    #83  课程表 II         (210)   拓扑排序（输出修课顺序）
    #84  腐烂的橘子        (994)   多源 BFS（层序扩散）
    #85  单词拆分          (139)   动态规划（区间可分段）
    #86  最长递增子序列    (300)   动态规划（LIS）
    #87  最长公共子序列    (1143)  动态规划（二维 DP 模板）
    #88  编辑距离          (72)    动态规划（二维 DP 模板）
    #89  打家劫舍          (198)   动态规划（状态压缩）

为什么今天这样排？
    - #80 / #81 是「回溯 + 图遍历」的收尾：单词搜索是带 visited 的网格 DFS，
      岛屿数量是「找到一块就淹掉一块」的洪泛，两者都练「别走回头路」。
    - #82 / #83 / #84 是图论三件套：拓扑排序（有向无环图）和 BFS 层序扩散。
      这几题在 Agent / 工作流（DAG 依赖、任务调度）面试里高频出现。
    - #85 ~ #89 正式进入「二维 DP 与线性 DP」：单词拆分是入门 DP，
      LIS / LCS / 编辑距离是三个最经典的二维 DP 模板，打家劫舍是状态压缩 DP。
      把今天这 5 道 DP 吃透，后面 Day 17+ 的背包、接雨水都会轻松很多。

贯穿今天的解题心法：
    1) 回溯 / DFS：用一个 visited 标记（或临时改成 '#'）防止走回头路，递归后撤销。
    2) BFS：用队列，每一层一起往外扩；多源 BFS 就是把所有起点同时入队。
    3) 拓扑排序：算入度 → 入度为 0 的入队 → 出队时把它指向的节点入度 -1，
       减到 0 再入队。最后入队数 == 节点数 说明无环。
    4) 二维 DP：先想 dp[i][j] 的「含义」，再写「转移方程」，最后补边界。
================================================================================
"""

from typing import List
from collections import defaultdict, deque


# =============================================================================
# #80 单词搜索 (LeetCode 79)  —— 网格 DFS + 回溯（visited 防回头）
# =============================================================================
def problem_80_exist(board: List[List[str]], word: str) -> bool:
    """
    题目描述：
        给定一个 m x n 的字母网格 board 和一个单词 word。
        如果网格中存在一条「相邻单元格（上下左右）连成」的路径恰好拼出 word，
        且路径上的格子不能重复使用，返回 True；否则返回 False。

    思路（网格上的 DFS 回溯）：
        1) 先枚举每一个格子作为起点（只有 board[i][j] == word[0] 才值得开始）。
        2) 从起点做 DFS：当前要匹配 word[idx]。
           - 越界 / 字母不符 / 已访问 → 返回 False；
           - idx == len(word) → 整词匹配完，返回 True。
        3) 标记当前格为「已访问」（临时改成 '#'），往四个方向继续找下一个字母。
        4) 递归返回后「撤销标记」（恢复原来的字母），因为别的路径可能还要用它。

    图示（以 board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']]，word="ABCCED" 为例）：
            A B C E
            S F C S
            A D E E
        起点 (0,0)='A' 命中首字母，接着：
            A->B (0,1) ->C (0,2) ->C (1,2) ->E (2,2) ->D (2,1)  ✔ 拼出 ABCCED
        搜索树（每个节点试上下左右，'X' 表示撞墙/已访问）：
            (0,0)A
              ├─(0,1)B
              │    ├─(0,2)C
              │    │    ├─(1,2)C
              │    │    │    ├─(2,2)E
              │    │    │    │    └─(2,1)D ✔ 命中
        关键：走过 (0,2) 后不能再回头走 (0,1)，靠「临时改 '#' + 撤销」保证。

    时间复杂度：O(m * n * 3^L)，L = len(word)。每个格子最多 4 个方向，
        但来路被挡住只剩 3 个，最坏从每个起点深搜 L 层。
    空间复杂度：O(L) 递归栈深度（visited 是原地改的，不额外占空间）。

    面试易错点：
        - 必须「先标记再递归，递归后撤销」。只标记不撤销 → 同一条路径会自交。
        - 起点要用 for 循环枚举所有等于首字母的格子，不能只试 (0,0)。
        - 题目允许修改 board，所以原地改 '#' 是合法且省空间的写法。
    """
    if not board or not board[0]:
        return False
    m, n = len(board), len(board[0])

    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):          # 整词匹配完
            return True
        if r < 0 or r >= m or c < 0 or c >= n:
            return False
        if board[r][c] != word[idx]:  # 字母对不上
            return False
        # 标记已访问，并准备回溯撤销
        temp = board[r][c]
        board[r][c] = '#'
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if dfs(r + dr, c + dc, idx + 1):
                return True
        board[r][c] = temp            # 撤销标记
        return False

    for i in range(m):
        for j in range(n):
            if board[i][j] == word[0] and dfs(i, j, 0):
                return True
    return False


# =============================================================================
# #81 岛屿数量 (LeetCode 200)  —— DFS 洪泛（连通块计数）
# =============================================================================
def problem_81_num_islands(grid: List[List[str]]) -> int:
    """
    题目描述：
        给你一个 '1'（陆地）和 '0'（水）组成的二维网格，计算「岛屿的数量」。
        岛屿被水包围，并且由水平或竖直相邻的陆地连接而成（斜着不算）。

    思路（找到一块就淹掉一块）：
        1) 遍历每个格子，遇到 '1' 说明发现了一座新岛，计数器 +1。
        2) 立即从这个格子做 DFS，把与它相连的所有 '1' 全部改成 '0'（「沉岛」），
           这样它们就不会被重复计数。
        3) 所有格子扫完，计数器就是岛屿数。

    图示（grid = [['1','1','0','0','0'],
                  ['1','1','0','0','0'],
                  ['0','0','1','0','0'],
                  ['0','0','0','1','1']]）：
            1 1 0  0  0       扫到(0,0)是1 -> 计数=1，洪泛把左上海岛沉掉
            1 1 0  0  0
            0 0 1  0  0       扫到(2,2)是1 -> 计数=2，沉掉这个小岛
            0 0 0  1  1       扫到(3,3)是1 -> 计数=3，沉掉右下岛
        答案 = 3。

    时间复杂度：O(m * n)，每个格子最多被访问一次。
    空间复杂度：O(m * n) 最坏递归栈（斜线退化为一条链时）。

    面试易错点：
        - 洪泛时要把访问过的陆地改成 '0'（或标记 visited），否则会死循环 / 重复计数。
        - 只上下左右四个方向，不要斜着连（题目明确不算）。
        - 空网格（grid 为空或首行空）要 early return 0，避免取 grid[0] 越界。
    """
    if not grid or not grid[0]:
        return 0
    m, n = len(grid), len(grid[0])
    count = 0

    def dfs(r: int, c: int) -> None:
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != '1':
            return
        grid[r][c] = '0'            # 沉岛，防止重复访问
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            dfs(r + dr, c + dc)

    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                count += 1
                dfs(i, j)
    return count


# =============================================================================
# #82 课程表 (LeetCode 207)  —— 拓扑排序判环（能否修完）
# =============================================================================
def problem_82_can_finish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    题目描述：
        共 numCourses 门课（编号 0..numCourses-1）。prerequisites 里 [a, b]
        表示「修 a 之前必须先修 b」。判断是否能修完所有课（即依赖图无环）。

    思路（Kahn 算法 / 拓扑排序）：
        1) 建图：b -> a（b 是 a 的前置），同时统计每门课的入度 indeg[a]。
        2) 把所有入度为 0 的课入队（没有前置要求的课可以先修）。
        3) 不断出队：每修完一门课 u，把它指向的课 v 入度 -1；减到 0 说明
           前置都满足了，v 入队。
        4) 统计「实际修完的课数」。若等于总课数 → 无环、能修完；否则有环、不能。

    图示（numCourses=2, prereq=[[1,0]] 表示修1要先修0）：
            入度: 0 -> 0,  1 -> 1
            边:   0 -> 1
            队列起点: [0]
            出队0 -> 1的入度变0 -> 入队1 -> 出队1
            修完2门 == 总数2 -> 能修完 ✔
        若 prereq=[[1,0],[0,1]]（0依赖1，1依赖0）：
            0和1入度都是1，谁都进不了队列 -> 修完0门 < 2 -> 有环 ❌

    时间复杂度：O(V + E)，V 门课，E 条依赖边。
    空间复杂度：O(V + E) 存图和入度数组。

    面试易错点：
        - 边方向别建反：是「前置 -> 后继」，入度统计的是「有几门前置」。
        - 用入度 == 0 作为入队条件，而不是出度。
        - 判环的本质就是「拓扑排序能否排完所有节点」。
    """
    indeg = [0] * numCourses
    adj = defaultdict(list)
    for a, b in prerequisites:
        adj[b].append(a)       # b 是 a 的前置
        indeg[a] += 1
    q = deque(i for i in range(numCourses) if indeg[i] == 0)
    visited = 0
    while q:
        u = q.popleft()
        visited += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return visited == numCourses


# =============================================================================
# #83 课程表 II (LeetCode 210)  —— 拓扑排序（输出修课顺序）
# =============================================================================
def problem_83_find_order(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    """
    题目描述：
        与 #82 相同，但要求返回「一种可行的修课顺序」（任意一种即可）。
        如果存在环无法修完，返回空列表 []。

    思路：
        和 #82 几乎一样，只是把「每次出队的课」按顺序记下来即可。
        最后若记录的课数 == 总课数，返回该顺序；否则返回 []。

    图示（numCourses=4, prereq=[[1,0],[2,0],[3,1],[3,2]]）：
            入度: 0->0, 1->1, 2->1, 3->2
            边:   0->1, 0->2, 1->3, 2->3
            队列起点: [0]
            出队0 -> order=[0]; 1、2入度变0入队
            出队1 -> order=[0,1]; 3入度1
            出队2 -> order=[0,1,2]; 3入度0入队
            出队3 -> order=[0,1,2,3]
            返回 [0,1,2,3] ✔（注意：合法拓扑序不唯一，这是其中一种）

    时间复杂度：O(V + E)
    空间复杂度：O(V + E)

    面试易错点：
        - 拓扑序不唯一，面试时只要「合法」即可，不要纠结唯一解。
        - 有环时必须返回 []（题目明确要求），别忘了最后那个长度判断。
    """
    indeg = [0] * numCourses
    adj = defaultdict(list)
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(numCourses) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == numCourses else []


# =============================================================================
# #84 腐烂的橘子 (LeetCode 994)  —— 多源 BFS（层序扩散计时）
# =============================================================================
def problem_84_oranges_rotting(grid: List[List[int]]) -> int:
    """
    题目描述：
        网格里 0=空，1=新鲜橘子，2=腐烂橘子。每分钟，腐烂橘子会把「上下左右」
        相邻的新鲜橘子也弄腐烂。返回「全部橘子都腐烂所需的最少分钟数」；
        如果不可能（有新鲜橘子永远烂不到），返回 -1。

    思路（多源 BFS）：
        1) 初始把所有腐烂橘子 (值为2) 同时入队，并记录层数 d=0。
        2) 同时统计新鲜橘子数量 fresh。
        3) 层序 BFS：每一层（同一分钟）把队里所有腐烂橘子拿出来，
           把相邻的新鲜橘子弄烂（改 2、fresh-1、以 d+1 入队）。
        4) BFS 结束时，若 fresh==0 返回最后到达的层数（分钟），否则 -1。
        若一开始 fresh==0，直接返回 0。

    图示（grid=[[2,1,1],[1,1,0],[0,1,1]]）：
            第0分钟: 2 1 1     只有(0,0)是烂的，入队
                    1 1 0
                    0 1 1
            第1分钟: 2 2 1     (0,0)把(0,1)(1,0)弄烂
                    2 1 0
                    0 1 1
            第2分钟: 2 2 2     (0,1)(1,0)继续向外烂
                    2 2 0
                    0 1 1
            第3分钟: 2 2 2
                    2 2 0
                    0 2 1
            第4分钟: 2 2 2     (2,1)把(2,2)烂掉
                    2 2 0
                    0 2 2
            fresh 归零，答案 = 4 分钟。

    时间复杂度：O(m * n)
    空间复杂度：O(m * n) 队列最坏存满网格

    面试易错点：
        - 是「多源」BFS：所有初始腐烂橘子同一时刻入队，而不是只从一个开始。
        - 用层序（按分钟）扩散，返回的是「最后被烂掉的橘子所在层」，不是橘子总数。
        - 初始就没有新鲜橘子时，要直接返回 0，别返回 -1。
        - 有新鲜橘子被空地/边界孤立（永远烂不到）→ 最后 fresh>0 → 返回 -1。
    """
    if not grid or not grid[0]:
        return 0
    m, n = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 2:
                q.append((i, j, 0))
            elif grid[i][j] == 1:
                fresh += 1
    if fresh == 0:
        return 0
    minutes = 0
    while q:
        r, c, d = q.popleft()
        minutes = d
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                q.append((nr, nc, d + 1))
    return minutes if fresh == 0 else -1


# =============================================================================
# #85 单词拆分 (LeetCode 139)  —— 动态规划（前缀能否被分割）
# =============================================================================
def problem_85_word_break(s: str, wordDict: List[str]) -> bool:
    """
    题目描述：
        给定字符串 s 和单词字典 wordDict，判断 s 是否能被拆成若干个「字典里的单词」
        拼接而成（单词可重复使用）。

    思路（一维 DP）：
        定义 dp[i] = 「s 的前 i 个字符（s[0:i]）能否被完整拆分」。
        - 边界：dp[0] = True（空串视作可拆分，是递推的基石）。
        - 转移：对每个 i（1..len(s)），枚举字典里的每个单词 w：
            若 len(w) <= i 且 s[i-len(w):i] == w 且 dp[i-len(w)] 为 True，
            说明「前面那段能拆 + 当前这个单词正好接上」→ dp[i] = True。
        - 答案：dp[len(s)]。

    图示（s="leetcode", wordDict=["leet","code"]）：
            s = l e e t c o d e
            dp下标: 0 1 2 3 4 5 6 7 8
            dp:     T F F F T F F F T
                    ^        ^        ^
                 空串      "leet"   "leet"+"code"
            dp[4]=True（"leet"），dp[8]=True（"leet"+"code"）→ 返回 True。

    时间复杂度：O(n * L * W)，n=len(s)，L=平均词长，W=字典词数（内层枚举单词）。
    空间复杂度：O(n) dp 数组 + O(W) 字典集合（用 set 查找更快，见下）。

    面试易错点：
        - dp[0]=True 必须初始化，它是所有拆分的起点，漏了就全 False。
        - 判断前缀用 s[i-len(w):i]，注意切片右开区间。
        - 实际工程可用 set(wordDict) 把「枚举单词 + 比对」优化成「枚举长度 + 在集合里查」，
          本题为了直观保留「枚举单词」写法，思路完全一致。
    """
    word_set = set(wordDict)
    dp = [False] * (len(s) + 1)
    dp[0] = True                      # 空串可拆
    for i in range(1, len(s) + 1):
        for w in word_set:
            if len(w) <= i and s[i - len(w):i] == w and dp[i - len(w)]:
                dp[i] = True
                break
    return dp[len(s)]


# =============================================================================
# #86 最长递增子序列 (LeetCode 300)  —— 动态规划（LIS）
# =============================================================================
def problem_86_length_of_lis(nums: List[int]) -> int:
    """
    题目描述：
        给你一个整数数组 nums，找到其中「最长严格递增子序列」的长度。
        子序列不要求连续，只要下标递增、数值严格递增即可。

    思路（O(n^2) DP，最通用好懂）：
        定义 dp[i] = 「以 nums[i] 结尾的最长递增子序列长度」，初始每个都是 1
        （至少包含自己）。
        对每个 i，往前看所有 j < i：如果 nums[j] < nums[i]，说明可以把 nums[i]
        接到以 nums[j] 结尾的子序列后面，于是 dp[i] = max(dp[i], dp[j] + 1)。
        最后返回 max(dp)。

    图示（nums = [10, 9, 2, 5, 3, 7, 101, 18]）：
            i :  0  1  2  3  4  5   6   7
            nums:10  9  2  5  3  7 101  18
            dp  : 1  1  1  2  2  3   4   4
            例如 dp[5]=3 来自 2->5->7；dp[6]=4 来自 2->5->7->101（或 2->3->7->101）。
            答案 = max(dp) = 4。

    时间复杂度：O(n^2)，双重循环。
    空间复杂度：O(n)。
    注：还有 O(n log n) 的「贪心 + 二分（牌堆法）」写法，面试若被追问可讲，
        但 O(n^2) 最稳、最好写、不易错，先保证这个拿分。

    面试易错点：
        - 子序列「不要求连续」，所以是比较 nums[j] < nums[i] 而非相邻比较。
        - dp 初值全 1（每个数自己就是长度 1 的子序列）。
        - 返回的是 max(dp)，不是 dp[-1]（结尾元素不一定在最长序列里）。
    """
    if not nums:
        return 0
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


# =============================================================================
# #87 最长公共子序列 (LeetCode 1143)  —— 二维 DP（经典模板）
# =============================================================================
def problem_87_longest_common_subsequence(text1: str, text2: str) -> int:
    """
    题目描述：
        给定两个字符串 text1 和 text2，返回它们的「最长公共子序列」的长度。
        子序列可删除若干字符得到，不要求连续，但顺序要一致。

    思路（二维 DP 模板，务必背熟）：
        令 dp[i][j] = 「text1 前 i 个字符 与 text2 前 j 个字符 的 LCS 长度」。
        - 若 text1[i-1] == text2[j-1]：这两个字符都能用上 → dp[i][j] = dp[i-1][j-1] + 1
        - 否则：不要 text1[i-1] 或不要 text2[j-1]，取较大者 →
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        - 边界：任一串为空，LCS=0，即 dp 第 0 行/第 0 列都是 0。
        答案：dp[m][n]。

    图示（text1="abcde", text2="ace"）：
              "" a c e
          ""  0 0 0 0
          a   0 1 1 1
          b   0 1 1 1
          c   0 1 2 2
          d   0 1 2 2
          e   0 1 2 3
        右下角 dp[5][3] = 3，对应子序列 "ace"。

    时间复杂度：O(m * n)
    空间复杂度：O(m * n)（可优化到 O(min(m,n)) 滚动数组，但面试先用二维最清楚）

    面试易错点：
        - 注意 dp 下标比字符串下标「多 1」，用 text1[i-1] / text2[j-1] 对齐字符。
        - 两字符相等时一定 +1（用的是左上角 dp[i-1][j-1]），不相等时才取 max(上, 左)。
        - 「公共子序列」vs「公共子串」：子序列不连续，子串连续；本题是子序列，
          所以不相等时不需要把长度清零，而是继承 max(上,左)。
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


# =============================================================================
# #88 编辑距离 (LeetCode 72)  —— 二维 DP（经典模板）
# =============================================================================
def problem_88_min_distance(word1: str, word2: str) -> int:
    """
    题目描述：
        给你两个单词 word1 和 word2，计算把 word1 变成 word2 的「最少操作数」。
        允许三种操作：插入一个字符、删除一个字符、替换一个字符，每步算 1 次。

    思路（二维 DP，和 LCS 同出一源）：
        令 dp[i][j] = 「word1 前 i 个字符 变成 word2 前 j 个字符 的最少操作数」。
        - 边界：dp[i][0] = i（删光 word1 前 i 个），dp[0][j] = j（插入 j 个）。
        - 转移：
            若 word1[i-1] == word2[j-1]：这两个字符已经一致，不用操作 →
                dp[i][j] = dp[i-1][j-1]
            否则：从三种操作取最小 +1：
                dp[i][j] = 1 + min( dp[i-1][j]   (删除 word1[i-1])
                                    dp[i][j-1]   (插入 word2[j-1])
                                    dp[i-1][j-1] (把 word1[i-1] 替换成 word2[j-1]) )
        - 答案：dp[m][n]。

    图示（word1="horse", word2="ros"）：
              "" r o s
          ""  0 1 2 3
          h   1 1 2 3
          o   2 1 2 3
          r   3 2 2 3
          s   4 3 3 3
          e   5 4 4 4
        右下角 = 3（horse -> rse(删h,删e) -> ros(把中间e...实际路径见代码逻辑)）。

    时间复杂度：O(m * n)
    空间复杂度：O(m * n)

    面试易错点：
        - 边界初始化容易漏：dp[i][0]=i、dp[0][j]=j 必须单独填。
        - 字符相等时「直接继承左上角」不要 +1，不相等时才 +1。
        - 三种操作对应三个来源格子：上(删)、左(插)、左上(替)，别记混。
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]


# =============================================================================
# #89 打家劫舍 (LeetCode 198)  —— 动态规划（状态压缩）
# =============================================================================
def problem_89_rob(nums: List[int]) -> int:
    """
    题目描述：
        你是一个劫匪，沿街有若干房子，每个房子有金额 nums[i]。
        不能「偷相邻的房子」（相邻房子有联动报警）。求能偷到的最大金额。

    思路（线性 DP + 滚动变量）：
        令 dp[i] = 「考虑到第 i 个房子为止能偷到的最大金额」。
        到第 i 个房子只有两种选择：
            - 偷它：那么第 i-1 个不能偷 → money = dp[i-2] + nums[i]
            - 不偷它： → money = dp[i-1]
        所以 dp[i] = max(dp[i-1], dp[i-2] + nums[i])。
        由于只用到前两个状态，用两个变量 prev(=dp[i-2])、curr(=dp[i-1]) 滚动即可，
        空间 O(1)。

    图示（nums = [2,7,9,3,1]）：
            i :     0   1   2   3   4
            nums:   2   7   9   3   1
            dp  :   2   7  11  11  12
            dp[0]=2（偷第0个）
            dp[1]=max(2,7)=7（偷第1个更划算）
            dp[2]=max(7, 2+9)=11（偷第2个：2+9）
            dp[3]=max(11, 7+3)=11（不偷第3个）
            dp[4]=max(11, 11+1)=12（偷第4个：11+1）
            答案 = 12（偷第0、2、4个：2+9+1）。

    时间复杂度：O(n)
    空间复杂度：O(1)（只滚动两个变量）

    面试易错点：
        - 初始值：空数组返回 0；只有 1 个房子返回它本身。
        - 滚动变量更新顺序：先算新值，再把 prev、curr 往后挪，别覆盖错。
        - 注意是「不相邻」而非「至少隔一个」以上，状态只依赖前两个。
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    prev, curr = 0, 0
    for x in nums:
        prev, curr = curr, max(curr, prev + x)
    return curr


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

    # ---- #80 单词搜索 (79) ----
    print("\n#80 单词搜索 (79):")
    b1 = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    check("ABCCED", problem_80_exist(b1, "ABCCED"), True)
    b2 = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    check("SEE", problem_80_exist(b2, "SEE"), True)
    b3 = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    check("ABCB", problem_80_exist(b3, "ABCB"), False)

    # ---- #81 岛屿数量 (200) ----
    print("\n#81 岛屿数量 (200):")
    g1 = [["1", "1", "0", "0", "0"],
          ["1", "1", "0", "0", "0"],
          ["0", "0", "1", "0", "0"],
          ["0", "0", "0", "1", "1"]]
    check("3 座岛", problem_81_num_islands(g1), 3)
    g2 = [["1", "0", "1", "1", "0"],
          ["1", "0", "1", "0", "1"],
          ["1", "1", "0", "0", "1"]]
    check("复杂网格 3 座岛", problem_81_num_islands(g2), 3)

    # ---- #82 课程表 (207) ----
    print("\n#82 课程表 (207):")
    check("能修完 [[1,0]]", problem_82_can_finish(2, [[1, 0]]), True)
    check("有环 [[1,0],[0,1]]", problem_82_can_finish(2, [[1, 0], [0, 1]]), False)

    # ---- #83 课程表 II (210) ----
    print("\n#83 课程表 II (210):")
    check("顺序 [0,1]", problem_83_find_order(2, [[1, 0]]), [0, 1])
    check("顺序 [0,1,2,3]",
          problem_83_find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]), [0, 1, 2, 3])
    check("有环返回 []", problem_83_find_order(2, [[1, 0], [0, 1]]), [])

    # ---- #84 腐烂的橘子 (994) ----
    print("\n#84 腐烂的橘子 (994):")
    o1 = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    check("4 分钟", problem_84_oranges_rotting(o1), 4)
    o2 = [[2, 1, 1], [0, 1, 1], [1, 0, 1]]
    check("有橘子烂不到 -> -1", problem_84_oranges_rotting(o2), -1)
    o3 = [[0, 2]]
    check("无新鲜橘子 -> 0", problem_84_oranges_rotting(o3), 0)

    # ---- #85 单词拆分 (139) ----
    print("\n#85 单词拆分 (139):")
    check("leetcode", problem_85_word_break("leetcode", ["leet", "code"]), True)
    check("applepenapple",
          problem_85_word_break("applepenapple", ["apple", "pen"]), True)
    check("catsandog 不可分",
          problem_85_word_break("catsandog",
                                ["cats", "dog", "sand", "and", "cat"]), False)

    # ---- #86 最长递增子序列 (300) ----
    print("\n#86 最长递增子序列 (300):")
    check("[10,9,2,5,3,7,101,18] -> 4",
          problem_86_length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]), 4)
    check("[0,1,0,3,2,3] -> 4",
          problem_86_length_of_lis([0, 1, 0, 3, 2, 3]), 4)
    check("[7,7,7,7] -> 1", problem_86_length_of_lis([7, 7, 7, 7]), 1)

    # ---- #87 最长公共子序列 (1143) ----
    print("\n#87 最长公共子序列 (1143):")
    check("abcde / ace -> 3",
          problem_87_longest_common_subsequence("abcde", "ace"), 3)
    check("abc / abc -> 3",
          problem_87_longest_common_subsequence("abc", "abc"), 3)
    check("abc / def -> 0",
          problem_87_longest_common_subsequence("abc", "def"), 0)

    # ---- #88 编辑距离 (72) ----
    print("\n#88 编辑距离 (72):")
    check("horse / ros -> 3",
          problem_88_min_distance("horse", "ros"), 3)
    check("intention / execution -> 5",
          problem_88_min_distance("intention", "execution"), 5)

    # ---- #89 打家劫舍 (198) ----
    print("\n#89 打家劫舍 (198):")
    check("[1,2,3,1] -> 4", problem_89_rob([1, 2, 3, 1]), 4)
    check("[2,7,9,3,1] -> 12", problem_89_rob([2, 7, 9, 3, 1]), 12)
    check("[2,1,1,2] -> 4", problem_89_rob([2, 1, 1, 2]), 4)

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
