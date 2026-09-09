# -*- coding: utf-8 -*-
"""
=====================================================================
LeetCode 面试手撕 · Day 21  (2026-08-13)
=====================================================================
背景：原「必刷 100 题」(Day1-18) 已完结；Day19-20 是 AI Agent / 后端岗的
      容器并发 + AI 工程专项补充。今天 Day 21 继续补齐图论进阶 + 位运算 +
      贪心 + 经典设计，这些都是 AI 应用/Agent 开发 JD 面试里最爱手撕、且
      前 20 天覆盖较少的高频题。

交付格式：可运行的 .py（直接 `python LeetCode-Day21.py` 跑通即验证对错）。
每题只给一种「通用、不复杂」的解法，附：
  - 详细思路（中文）
  - 时间/空间复杂度
  - 面试易错点
  - ASCII 流程图/示意图
所有测试用例在文件末尾 `if __name__ == "__main__"` 里，跑完会打印 PASS/FAIL。
=====================================================================
"""

# =====================================================================
# 第 1 题  · 朋友圈  (LeetCode #547, Medium) —— 并查集 Union-Find
# =====================================================================
def findCircleNum(isConnected):
    r"""
    题意：n 个人，isConnected[i][j]==1 表示 i 和 j 是朋友。朋友关系有传递性
    （朋友的朋友也是朋友）。求有多少个「朋友圈」（连通块）。

    通用解法：并查集（Disjoint Set Union, DSU）。
    把每个人看成一个节点，互为朋友就连一条边。最后求「还剩几个独立集合」即可。
    并查集两个核心优化：
      1) 路径压缩 find：找根时顺手把沿途节点直接挂到根上，下次再找就是 O(1)。
      2) 按秩合并 union：小树挂到大树下，避免退化成链。

    复杂度：时间 O(n^2 * α(n))，α 是反阿克曼函数（几乎常数）；空间 O(n)。
    易错点：只在 j>i 时 union（矩阵对称，避免重复处理同一对）；
            count 初始为 n，每成功合并一次减 1。

    流程图（n=4，矩阵对角全 1，[1][3]=0）：
        初始:  0  1  2  3     (count = 4, 各自独立)
        union(0,1) -> 1 挂到 0:  0       2  3   (count=3)
                                |
                                1
        union(2,3) -> 3 挂到 2:  0       2       (count=2)
                                |      |
                                1      3
        最终 2 个集合 => 返回 2
    """
    n = len(isConnected)
    parent = list(range(n))
    rank = [0] * n
    count = n

    def find(x):
        # 路径压缩：一路把父节点扳直
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        nonlocal count
        rx, ry = find(x), find(y)
        if rx == ry:
            return  # 已经在同一集合，不重复计数
        # 按秩合并
        if rank[rx] < rank[ry]:
            parent[rx] = ry
        elif rank[rx] > rank[ry]:
            parent[ry] = rx
        else:
            parent[ry] = rx
            rank[rx] += 1
        count -= 1

    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                union(i, j)
    return count


# =====================================================================
# 第 2 题  · 网络延迟时间  (LeetCode #743, Medium) —— Dijkstra 最短路
# =====================================================================
import heapq

def networkDelayTime(times, n, k):
    r"""
    题意：有 n 个节点（编号 1..n），times 是边列表 [u, v, w]（u->v 耗时 w）。
    从节点 k 同时发出信号，求「所有节点都收到信号」所需的最短时间；若有节点
    永远收不到，返回 -1。

    通用解法：Dijkstra 单源最短路（边权非负，用堆优化）。
    维护 dist[] 表示从 k 到每个节点的最短路；每次从优先队列里取出当前距离最小
    的节点，用它去松弛邻居。

    复杂度：时间 O(E log V)，空间 O(V+E)。（V=n, E=边数）
    易错点：dist 初始化为 inf，源点 dist[k]=0；弹出后若 d>dist[node] 说明是
            过期堆条目，直接跳过（同一个节点可能被多次入堆）；
            最后用 max(dist[1:]) 取「最慢那个节点」，是 inf 就返回 -1。

    堆推进示意（源点 k=2）：
        堆: (0,2)
        pop(0,2) -> 松弛邻居 1(0+1),3(0+1) -> 堆:(1,1),(1,3)
        pop(1,1) -> 堆:(1,3)
        pop(1,3) -> 松弛 4(1+1) -> 堆:(2,4)
        pop(2,4) -> 结束
        最终 dist=[inf,1,0,1,2] -> max=2
    """
    graph = [[] for _ in range(n + 1)]
    for u, v, w in times:
        graph[u].append((v, w))

    dist = [float("inf")] * (n + 1)
    dist[k] = 0
    pq = [(0, k)]  # (距离, 节点)

    while pq:
        d, node = heapq.heappop(pq)
        if d > dist[node]:
            continue  # 过期条目，跳过
        for nei, w in graph[node]:
            nd = d + w
            if nd < dist[nei]:
                dist[nei] = nd
                heapq.heappush(pq, (nd, nei))

    ans = max(dist[1:])
    return ans if ans != float("inf") else -1


# =====================================================================
# 第 3 题  · 外星字典  (LeetCode #269, Medium) —— 拓扑排序 (Kahn)
# =====================================================================
from collections import deque, defaultdict

def alienOrder(words):
    r"""
    题意：给定一组按「外星语字典序」排好序的单词，求外星语字母的先后关系
    （任意一种合法顺序即可）；若给出的 words 本身自相矛盾，返回 ""。

    通用解法：拓扑排序（Kahn 算法，BFS + 入度表）。
    步骤：
      1) 建图：相邻两词比较，找到第一个不同字母 ch1!=ch2，就得到一条有向边
         ch1 -> ch2（ch1 在 ch2 前面）。
      2) 统计每个字母的入度。
      3) 把所有入度为 0 的字母入队，逐层弹出不破环，删边、减入度。
      4) 最后若输出的字母数 == 总字母数，说明无环、合法；否则有环 -> ""。

    复杂度：时间 O(C)（C 为所有单词字符总数），空间 O(1)（字母集最多 26）。
    易错点：① 要先把「所有出现过的字母」都放进 indeg（有的字母可能没出现在任何
            边里，入度 0 也要进队）；② 若 w1 是 w2 的前缀且 w1 更长（如 "abc","ab"），
            字典序不可能，直接返回 ""。

    建图示意：words = ["wrt","wrf","er","ett","rftt"]
        wrt|wrf -> 首不同 't'!='f' => 边 t->f
        wrf|er  -> 首不同 'w'!='e' => 边 w->e
        er|ett  -> 首不同 'r'!='t' => 边 r->t
        ett|rftt-> 首不同 'e'!='r' => 边 e->r
        得图: w->e->r->t->f ，拓扑输出 "wertf"
    """
    # 所有出现过的字母都先入度 0
    indeg = {c: 0 for c in set("".join(words))}
    adj = defaultdict(set)

    for w1, w2 in zip(words, words[1:]):
        for ch1, ch2 in zip(w1, w2):
            if ch1 != ch2:
                if ch2 not in adj[ch1]:
                    adj[ch1].add(ch2)
                    indeg[ch2] += 1
                break
        else:
            # w1 是 w2 的前缀：若 w1 更长则非法
            if len(w2) < len(w1):
                return ""

    q = deque([c for c in indeg if indeg[c] == 0])
    order = []
    while q:
        c = q.popleft()
        order.append(c)
        for nxt in adj[c]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)

    return "".join(order) if len(order) == len(indeg) else ""


# =====================================================================
# 第 4 题  · 快乐数  (LeetCode #202, Easy) —— 哈希判圈
# =====================================================================
def isHappy(n):
    r"""
    题意：把一个数每一位平方后求和得到新数，反复如此。若最终变到 1 就是快乐数，
    否则会进入循环永远到不了 1。

    通用解法：用集合记录「已经出现过的数」，一旦遇到重复（或到 1）就停。
    这是最直白、面试最稳的写法（不用 Floyd 快慢指针也能过）。

    复杂度：时间 O(log n)（每次平方和操作位数有限，且必然进入有限循环），
            空间 O(log n) 存出现过的数。
    易错点：循环终止条件有两个——等于 1（成功）或 已在集合里（死循环失败）。

    变换示意（n=19）：
        19 -> 1+81=82 -> 64+4=68 -> 36+64=100 -> 1+0+0=1  => True
    """
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(d) * int(d) for d in str(n))
    return n == 1


# =====================================================================
# 第 5 题  · Pow(x, n)  (LeetCode #50, Medium) —— 快速幂（二分幂）
# =====================================================================
def myPow(x, n):
    r"""
    题意：实现 x^n，n 可正可负可零。

    通用解法：快速幂（二进制折半）。把指数 n 看成二进制，每次把底数 x 平方，
    若当前指数最低位是 1 就把结果乘上当前 x。这样把 O(n) 降到 O(log n)。

    复杂度：时间 O(log n)，空间 O(1)。
    易错点：① n 为负时先取倒数再把 n 转成正数；② n 可能超 int 范围（Python 不限，
            但写法要对）；③ 用位运算 n & 1 判奇偶、n >>= 1 折半最稳。

    示意（x=2, n=10，二进制 1010）：
        n=10(偶) -> res 不变, x=4,   n=5
        n=5 (奇) -> res*=4=4,  x=16,  n=2
        n=2 (偶) -> res 不变, x=256, n=1
        n=1 (奇) -> res*=256=1024, x=..., n=0 -> 返回 1024
    """
    if n == 0:
        return 1
    if n < 0:
        x = 1 / x
        n = -n
    res = 1
    while n > 0:
        if n & 1:
            res *= x
        x *= x
        n >>= 1
    return res


# =====================================================================
# 第 6 题  · 跳跃游戏  (LeetCode #55, Medium) —— 贪心
# =====================================================================
def canJump(nums):
    r"""
    题意：数组每个元素表示「从当前位置最远能跳几步」。问能否从下标 0 跳到末尾。

    通用解法：贪心。维护一个「当前能到达的最远下标 reach」。从左到右扫，若某位置
    下标 i 已经超过 reach，说明跳不过去；否则用 i+nums[i] 更新 reach。扫完没卡住
    就说明能到。

    复杂度：时间 O(n)，空间 O(1)。
    易错点：判断顺序是先 `if i > reach: return False` 再更新 reach；
            只要 reach 提前 >= 末位即可（不必真的跳到）。

    示意 nums=[2,3,1,1,4]：
        i=0 reach=max(0,0+2)=2
        i=1 reach=max(2,1+3)=4  >= 末位4 => 可达
    """
    reach = 0
    for i, step in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + step)
    return True


# =====================================================================
# 第 7 题  · 加油站  (LeetCode #134, Medium) —— 贪心
# =====================================================================
def canCompleteCircuit(gas, cost):
    r"""
    题意：环形路上有 n 个加油站，gas[i] 加油、cost[i] 到下一站耗油。从某站出发
    顺时针走，能否绕一圈回到起点？能则返回起点下标，否则 -1（若有解必唯一）。

    通用解法：贪心。两个量：
      - total：全程净油量，<0 说明整体不够，必无解。
      - tank：从当前候选起点 start 出发的累计油量；一旦 tank<0，说明从 start 到 i
        都当不了起点（中间任何一站出发都会更早没油），直接把 start 改成 i+1 重来。

    复杂度：时间 O(n)，空间 O(1)。
    易错点：只在 tank<0 时才「丢弃前面所有、从 i+1 重新计」；最后用 total>=0 决定
            返回 start 还是 -1。

    示意 gas=[1,2,3,4,5] cost=[3,4,5,1,2]：
        i=0 tank=-2<0 -> start=1,tank=0
        i=1 tank=-2<0 -> start=2,tank=0
        i=2 tank=-2<0 -> start=3,tank=0
        i=3 tank=+3 ; i=4 tank=+6 ; 结束 total=0>=0 -> 起点 3
    """
    total = 0
    tank = 0
    start = 0
    for i in range(len(gas)):
        total += gas[i] - cost[i]
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1
            tank = 0
    return start if total >= 0 else -1


# =====================================================================
# 第 8 题  · 比特位计数  (LeetCode #338, Easy) —— 位运算 DP
# =====================================================================
def countBits(n):
    r"""
    题意：返回 [0..n] 每个数的「二进制里 1 的个数」组成的数组。

    通用解法：利用性质 `bits[i] = bits[i >> 1] + (i & 1)`。
    i>>1 等于去掉最低位，所以 i 的 1 的个数 = 「去掉最低位后的数的 1 的个数」 +
    最低位本身是不是 1。O(n) 一遍递推。

    复杂度：时间 O(n)，空间 O(n)。
    易错点：(i & 1) 取最低位；dp 长度 n+1，从 1 开始递推（bits[0]=0）。

    示意 n=5：
        i:  0 1 2 3 4 5
        bits:0 1 1 2 1 2
        例 i=5(101): bits[5]=bits[2]+1=1+1=2
    """
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)
    return ans


# =====================================================================
# 第 9 题  · 设计循环队列  (LeetCode #622, Medium) —— 手写容器
# =====================================================================
class MyCircularQueue:
    r"""
    题意：用定长数组实现一个环形队列，支持 enQueue / deQueue / Front / Rear /
    isEmpty / isFull。环形=写完队尾再回头写队头（头尾指针在数组里绕圈）。

    通用解法：数组 + head 指针 + size 计数。
      - 不用单独维护 tail，tail = (head + size) % k。
      - size 同时充当「是否空/满」的判断：size==0 空，size==k 满。
      - 入队：先算 tail 位置写值，size++；出队：head 前进一格，size--。
    用 size 判断比「head/tail 相等」区分空满更不容易出错（后者空满长一样）。

    复杂度：所有操作 O(1)，空间 O(k)。
    易错点：取模 `% k` 别写错；Rear 取的是 (head+size-1)%k；
            空队列 Front/Rear 返回 -1（题目约定）。

    环形示意 (k=3, 已入 1,2)：
        [1][2][_]
         h
        size=2
    再入 3 -> [1][2][3] 满；出队 -> [_[2][3], head 移到 2
    """
    def __init__(self, k):
        self.q = [0] * k
        self.k = k
        self.head = 0
        self.size = 0

    def enQueue(self, value):
        if self.isFull():
            return False
        tail = (self.head + self.size) % self.k
        self.q[tail] = value
        self.size += 1
        return True

    def deQueue(self):
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % self.k
        self.size -= 1
        return True

    def Front(self):
        return -1 if self.isEmpty() else self.q[self.head]

    def Rear(self):
        return -1 if self.isEmpty() else self.q[(self.head + self.size - 1) % self.k]

    def isEmpty(self):
        return self.size == 0

    def isFull(self):
        return self.size == self.k


# =====================================================================
# 第 10 题 · 逆波兰表达式求值  (LeetCode #150, Medium) —— 栈
# =====================================================================
def evalRPN(tokens):
    r"""
    题意：给后缀表达式（逆波兰式），求值。操作数在前，遇到运算符就取栈顶两个
    数计算，结果再压回栈。运算符只有 + - * /。

    通用解法：栈。遍历 tokens：
      - 是数字就转 int 入栈；
      - 是运算符就弹出栈顶两个（注意顺序：先弹的是右操作数 b，再弹的是左 a），
        按运算压回结果。
    除法要「向零截断」：用 int(a/b) 而非 a//b（// 是向下取整，负数会错）。

    复杂度：时间 O(m)（m=tokens 个数），空间 O(m)。
    易错点：弹出顺序 b=pop(), a=pop()，计算 a op b；除法用 int(a/b) 向零取整。

    示意 ["2","1","+","3","*"]：
        入 2 -> 入 1 -> 遇'+' 弹1,2 => 2+1=3 入栈 -> 入 3 ->
        遇'*' 弹3,3 => 3*3=9 => 返回 9
    """
    stack = []
    ops = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: int(a / b),  # 向零截断
    }
    for t in tokens:
        if t in ops:
            b = stack.pop()
            a = stack.pop()
            stack.append(ops[t](a, b))
        else:
            stack.append(int(t))
    return stack[0]


# =====================================================================
# 自测：直接运行本文件即可验证对错
# =====================================================================
if __name__ == "__main__":
    passed = 0
    total = 0

    def check(name, got, exp):
        global passed, total
        total += 1
        ok = got == exp
        passed += ok
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {name}: got={got}  exp={exp}")

    # 第1题 朋友圈
    check("547 朋友圈", findCircleNum([[1, 1, 0], [1, 1, 0], [0, 0, 1]]), 2)
    check("547 朋友圈(单圈)", findCircleNum([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), 3)

    # 第2题 网络延迟时间
    check("743 网络延迟", networkDelayTime([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2), 2)
    check("743 不可达", networkDelayTime([[1, 2, 1]], 3, 1), -1)

    # 第3题 外星字典
    check("269 外星字典", alienOrder(["wrt", "wrf", "er", "ett", "rftt"]), "wertf")
    check("269 有环", alienOrder(["z", "x", "z"]), "")
    check("269 前缀非法", alienOrder(["abc", "ab"]), "")

    # 第4题 快乐数
    check("202 快乐数", isHappy(19), True)
    check("202 非快乐数", isHappy(2), False)

    # 第5题 快速幂
    check("50 幂(正)", myPow(2.0, 10), 1024.0)
    check("50 幂(负)", myPow(2.0, -2), 0.25)
    check("50 幂(零)", myPow(3.0, 0), 1)

    # 第6题 跳跃游戏
    check("55 跳跃(可)", canJump([2, 3, 1, 1, 4]), True)
    check("55 跳跃(否)", canJump([3, 2, 1, 0, 4]), False)

    # 第7题 加油站
    check("134 加油站", canCompleteCircuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]), 3)
    check("134 无解", canCompleteCircuit([2, 3, 4], [3, 4, 3]), -1)

    # 第8题 比特位计数
    check("338 比特位", countBits(5), [0, 1, 1, 2, 1, 2])

    # 第9题 循环队列
    q = MyCircularQueue(3)
    check("622 入队", q.enQueue(1), True)
    q.enQueue(2); q.enQueue(3)
    check("622 满", q.enQueue(4), False)
    check("622 Front", q.Front(), 1)
    check("622 Rear", q.Rear(), 3)
    check("622 出队", q.deQueue(), True)
    check("622 出队后Front", q.Front(), 2)
    check("622 空?", q.isEmpty(), False)

    # 第10题 逆波兰
    check("150 逆波兰1", evalRPN(["2", "1", "+", "3", "*"]), 9)
    check("150 逆波兰2", evalRPN(["4", "13", "5", "/", "+"]), 6)
    check("150 逆波兰3",
          evalRPN(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]), 22)

    print(f"\n=== Day21 共 {total} 个用例，通过 {passed}/{total} ===")
    if passed != total:
        raise SystemExit("存在 FAIL 用例，请检查！")
