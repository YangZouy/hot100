"""
LeetCode 必刷100题 · Day 04（2026-07-15）
========================================
面试方向：AI 应用 / Agent 开发
今日题目：
  - 第 7 题：最小栈                       LeetCode 155   中等   频率 ⭐⭐⭐⭐
  - 第 8 题：用栈实现队列                 LeetCode 232   简单   频率 ⭐⭐⭐⭐

运行方式：
    python LeetCode-Day04.py
会自动执行所有测试用例并打印 PASS / FAIL。

每个题目都包含：① 思路讲解 ② 流程示意图（ASCII）③ 可运行代码 ④ 复杂度分析 ⑤ 面试易错点。
只给一种「通用解法」，方便记忆和手撕。
"""

# ============================================================
# 第 7 题：最小栈（LeetCode 155）
# ============================================================
"""
题目描述
--------
设计一个「最小栈」MinStack，除了支持普通栈的 push / pop / top 外，
还要能用一个操作 getMin() 在 O(1) 时间内拿到当前栈里的最小值。

要求：push、pop、top、getMin 四个操作的时间复杂度都必须是 O(1)。

普通栈只能 O(1) 拿到「栈顶」，拿最小值需要遍历整个栈（O(n)）。
怎么让最小值也能 O(1) 取到？—— 用一个**辅助栈**专门同步记录最小值。

思路：辅助栈（同步最小栈）
--------------------------
维护两个栈：
  - main：普通栈，存所有元素（和正常栈一样）。
  - min_st：辅助栈，存「到当前位置为止的最小值」。

压栈 push(x)：
  - 把 x 压入 main。
  - 若 min_st 为空，或 x <= min_st 栈顶（当前最小值），就把 x 也压入 min_st。
    （注意用 `<=`，不是 `<`！这样遇到重复的最小值也能正确保留，pop 时不会误删。）

出栈 pop()：
  - 从 main 弹出栈顶值 v。
  - 若 v == min_st 栈顶，说明「最小的那个数被弹走了」，min_st 也跟着弹一个。

取栈顶 top()：返回 main 栈顶。

取最小值 getMin()：返回 min_st 栈顶。

为什么 O(1)？每个操作都只是「压栈/弹栈/读栈顶」——固定几步，和数据量无关。

流程示意（执行：push -2 / push 0 / push -3 / pop / getMin）
-----------------------------------------------------------------
操作            main 栈          min_st 栈        说明
初始            []               []               两个栈都空
push(-2)        [-2]             [-2]             -2≤空 → 入min栈
push(0)         [-2, 0]          [-2]             0>-2 → min栈不变
push(-3)        [-2, 0, -3]      [-2, -3]         -3≤-2 → 入min栈
pop()           [-2, 0]          [-2]             弹-3 == min顶-3 → min栈也弹
top()           → 返回 0         （main 栈顶）
getMin()        → 返回 -2        （min_st 栈顶）

复杂度：
  时间 O(1)（每个操作都是常数步）   空间 O(n)（最坏每个元素都进 min_st 一次）
面试易错点：
  - 条件写 `<=` 而不是 `<`：否则像 [2,2] 这种有重复最小值的，pop 一个 2 会把
    min_st 唯一的 2 弹掉，剩下 getMin 出错。
  - 也可以「一个栈存 (值, 当前最小值) 的元组」来实现，思路等价，但辅助栈更好讲。
  - 面试官常追问 pop 后 getMin 对不对，一定要讲清「min_st 同步弹」这一步。
"""


class MinStack:
    """用辅助栈实现 O(1) getMin 的栈。"""

    def __init__(self) -> None:
        self.main: list[int] = []   # 主栈：存所有元素
        self.min_st: list[int] = []  # 辅助栈：同步存「当前最小值」

    def push(self, x: int) -> None:
        self.main.append(x)
        # 辅助栈为空，或 x 不大于等于当前最小值时入栈
        # 用 <= 保留重复的最小值，保证 pop 时不会误删
        if not self.min_st or x <= self.min_st[-1]:
            self.min_st.append(x)

    def pop(self) -> None:
        if not self.main:
            return
        v = self.main.pop()
        # 若弹走的正好是当前最小值，辅助栈同步弹出一个
        if v == self.min_st[-1]:
            self.min_st.pop()

    def top(self) -> int:
        return self.main[-1]

    def getMin(self) -> int:
        return self.min_st[-1]


# ============================================================
# 第 8 题：用栈实现队列（LeetCode 232）
# ============================================================
"""
题目描述
--------
仅用「栈」这种数据结构，实现一个「队列」——支持：
  - push(x)：把元素 x 加入队尾
  - pop()：移除并返回队头元素
  - peek()：返回队头元素但不移除
  - empty()：队列是否为空

栈是「后进先出 LIFO」，队列是「先进先出 FIFO」。
核心矛盾：最早进栈的元素压在最底下，可队列要最早出它。
解法：用「两个栈」，一个负责进，一个负责出，出的时候把顺序反转过来。

思路：双栈法（in 栈 + out 栈，懒转移）
-------------------------------------
维护两个栈：
  - in_stack：所有新元素都从这里进（push 永远只压它）。
  - out_stack：需要 pop / peek 时从它出。

关键技巧（懒转移 lazy transfer）：
  - push(x) → 直接压入 in_stack。
  - pop() / peek() 时：
      * 若 out_stack 非空，直接从 out_stack 弹/取（栈顶就是队头）；
      * 若 out_stack 为空，就把 in_stack 里的元素「全部倒」到 out_stack。
        倒一次后，原本在 in_stack 底部的「最早元素」就跑到 out_stack 顶部了，
        顺序正好和入队顺序一致，于是 out_stack 弹出来的就是队头。
  - empty()：两个栈都为空才叫空。

为什么是「懒」转移？不需要每次 push 都倒，只在 out 空了要取元素时才倒一次，
均摊下来每个元素最多被倒一次，整体还是高效的。


流程示意（执行：push 1 / push 2 / peek / pop / empty / push 3 / push 4 / pop / peek）
-----------------------------------------------------------------
操作        in_stack     out_stack      说明
初始        []           []             两个栈都空
push(1)     [1]          []             进栈：压入 in
push(2)     [1, 2]       []             进栈：压入 in
peek()      []           [2, 1]         out空 → 把in全倒入out
                                        （in弹出2压入out，in弹出1压入out → out栈顶是1=队头）
            → 返回 1                    peek 返回 out 栈顶 = 1
pop()       []           [2]            out非空 → 直接弹栈顶 = 1（队头出列）
empty()     []           [2]            out 非空 → 返回 False
push(3)     [3]          [2]            进栈：压入 in
push(4)     [3, 4]       [2]            进栈：压入 in
pop()       []           [4]            out非空 → 弹出2；out变空 → 把in全倒入out
                                        （in弹出4压入out，in弹出3压入out → out栈顶是3=队头）
            → 返回 3                    返回 out 栈顶 = 3
peek()      []           [4]            out非空 → 返回 out 栈顶 = 4
            → 返回 4

复杂度：
  时间：push O(1)；pop/peek 均摊 O(1)（每个元素最多被倒一次）
  空间 O(n)（所有元素都存在两个栈里）
面试易错点：
  - 别在每次 push 时都倒来倒去，那样 push 退化成 O(n)；用「out 空才倒」的懒转移。
  - pop / peek 之前要先判断 out 是否为空，空了才从 in 倒。
  - peek 和 pop 逻辑几乎一样，区别只在于 peek 不弹出（可以复用「确保 out 有值」的步骤）。
  - 转移时必须把 in_stack 全部倒空，不能只倒一部分。
"""


class MyQueue:
    """用两个栈（in + out）实现队列。"""

    def __init__(self) -> None:
        self.in_stack: list[int] = []   # 负责进
        self.out_stack: list[int] = []  # 负责出

    def _transfer_if_needed(self) -> None:
        """若 out 栈空，把 in 栈元素全部倒入 out，反转成正确出队顺序。"""
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def pop(self) -> int:
        self._transfer_if_needed()
        return self.out_stack.pop()

    def peek(self) -> int:
        self._transfer_if_needed()
        return self.out_stack[-1]

    def empty(self) -> bool:
        return not self.in_stack and not self.out_stack

# ============================================================
# 测试用例：直接运行本文件即可验证
# ============================================================
def _run_tests() -> None:
    print("=" * 60)
    print("第 7 题：最小栈（LeetCode 155）")
    print("=" * 60)
    ms = MinStack()
    ms.push(-2)
    ms.push(0)
    ms.push(-3)
    got_min1 = ms.getMin()
    print(f"  push(-2) push(0) push(-3) 后 getMin -> {got_min1}  期望 -3  "
          f"[{'PASS' if got_min1 == -3 else 'FAIL'}]")
    # assert got_min1 == -3

    ms.pop()               # 弹走 -3
    got_top = ms.top()
    got_min2 = ms.getMin()
    print(f"  pop() 后 top -> {got_top}  期望 0   "
          f"[{'PASS' if got_top == 0 else 'FAIL'}]")
    print(f"  pop() 后 getMin -> {got_min2}  期望 -2   "
          f"[{'PASS' if got_min2 == -2 else 'FAIL'}]")
    assert got_top == 0 and got_min2 == -2

    # 验证重复最小值不会误删
    ms2 = MinStack()
    ms2.push(2)
    ms2.push(2)
    ms2.pop()
    dup_ok = ms2.getMin() == 2
    print(f"  重复最小值 [2,2] 弹一个后 getMin -> {ms2.getMin()}  期望 2   "
          f"[{'PASS' if dup_ok else 'FAIL'}]")
    assert dup_ok

    print()
    print("=" * 60)
    print("第 8 题：用栈实现队列（LeetCode 232）")
    print("=" * 60)
    q = MyQueue()
    print(f"  初始 empty -> {q.empty()}  期望 True  "
          f"[{'PASS' if q.empty() else 'FAIL'}]")
    assert q.empty()

    q.push(1)
    q.push(2)
    pk = q.peek()
    print(f"  push(1) push(2) 后 peek -> {pk}  期望 1  "
          f"[{'PASS' if pk == 1 else 'FAIL'}]")
    assert pk == 1

    po = q.pop()
    print(f"  pop -> {po}  期望 1  [{'PASS' if po == 1 else 'FAIL'}]")
    assert po == 1

    emp = q.empty()
    print(f"  再 empty -> {emp}  期望 False  [{('PASS' if not emp else 'FAIL')}]")
    assert not emp

    # 连续进多个再连续出，验证顺序正确（FIFO）
    q2 = MyQueue()
    for v in [10, 20, 30]:
        q2.push(v)
    order = [q2.pop(), q2.pop(), q2.pop()]
    print(f"  顺序验证 pop×3 -> {order}  期望 [10, 20, 30]  "
          f"[{'PASS' if order == [10, 20, 30] else 'FAIL'}]")
    assert order == [10, 20, 30]

    print("\n✅ 全部测试用例通过！")


if __name__ == "__main__":
    _run_tests()
