"""
LeetCode 必刷100题 · Day 05（2026-07-15）
========================================
面试方向：AI 应用 / Agent 开发
今日题目：
  - 第 9 题：每日温度                       LeetCode 739   中等   频率 ⭐⭐⭐⭐⭐
  - 第 10 题：反转链表                      LeetCode 206   简单   频率 ⭐⭐⭐⭐⭐

运行方式：
    python LeetCode-Day05.py
会自动执行所有测试用例并打印 PASS / FAIL。

每个题目都包含：① 思路讲解 ② 流程示意图（ASCII）③ 可运行代码 ④ 复杂度分析 ⑤ 面试易错点。
只给一种「通用解法」，方便记忆和手撕。
"""

# ============================================================
# 第 9 题：每日温度（LeetCode 739）
# ============================================================
"""
题目描述
--------
给定一个整数数组 temperatures 表示每天的温度，返回一个数组 answer，
其中 answer[i] 表示「在 i 之后、第一个比 temperatures[i] 高的温度的索引 j 与 i 的距离 (j - i)」。
如果之后没有更高的温度，answer[i] = 0。

示例：
    temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
    answer       = [ 1,  1,  4,  2,  1,  1,  0,  0]
    （第0天73度，第1天74度更高，距离 = 1-0 = 1；第2天75度，下一个更高是76度在下标6，距离=4 …）

朴素想法（暴力）：对每一天 i，往后扫找第一个更高的 j。最坏 O(n^2)（温度一路下降时）。
面试要的是 O(n) 解法 → 单调栈。

思路：单调递减栈（栈里存「索引」，对应的温度从栈底到栈顶递减）
-----------------------------------------------------------
为什么用「栈」？我们要找「每个温度右侧第一个更高的温度」。栈顶恰好是「最近一个还没找到
更高温度的日子」。一旦遇到更热的日子，就把栈顶那些被它「终结」的日子全部结算掉。

维护一个栈 st，里面只存索引，且保证 temperatures[st[-1]] >= temperatures[st[-2]] >= ...
（从栈顶到栈底温度递减）。遍历 i = 0..n-1：

  1. 只要栈非空，且 temperatures[i] > temperatures[st[-1]]：
        说明第 i 天比栈顶那天更热，栈顶等到了「第一个更高的温度」！
        弹出栈顶 top，记录 answer[top] = i - top。
        （循环弹出，因为新来的热天可能一次终结栈里多个更凉的日子。）
  2. 把当前 i 压入栈。
  3. 没被结算的日子（栈里剩下的）answer 默认 0，说明它右边没有更热的。

每篇文章只入栈一次、出栈一次 → 总时间 O(n)。

流程示意（temperatures = [73,74,75,71,69,72,76,73]，栈内写「索引(温度)」）
--------------------------------------------------------------------------------
i   温度   动作                                 栈 st（栈底→栈顶）            answer 更新
0   73     栈空，压入 0                         [0(73)]                      -
1   74     74>73 弹0，ans[0]=1-0=1；压1         [1(74)]                      ans[0]=1
2   75     75>74 弹1，ans[1]=2-1=1；压2         [2(75)]                      ans[1]=1
3   71     71<75 压入3                          [2(75),3(71)]                -
4   69     69<71 压入4                          [2(75),3(71),4(69)]          -
5   72     72>69 弹4 ans[4]=1；72>71 弹3 ans[3]=2；
        72<75 压5                               [2(75),5(72)]               ans[4]=1, ans[3]=2
6   76     76>72 弹5 ans[5]=1；76>75 弹2 ans[2]=4；压6
                                            [6(76)]                      ans[5]=1, ans[2]=4
7   73     73<76 压入7                          [6(76),7(73)]                -
结束 栈剩 [6,7] 未结算 → ans[6]=0, ans[7]=0
最终 answer = [1, 1, 4, 2, 1, 1, 0, 0]  ✓

复杂度：
  时间 O(n)（每个索引最多入栈、出栈各一次）  空间 O(n)（栈最坏存所有索引）
面试易错点：
  - 栈里存「索引」而不是「温度值」，结算时需要 j - i，必须靠索引算距离。
  - 是「单调递减栈」（从栈底到栈顶递减），不是递增；搞反了就全错。
  - 弹出条件是 temperatures[i] > temperatures[st[-1]]（严格大于），等于时不结算。
  - 这种「找每个元素右边第一个更大的」的题，单调栈是通用模板，务必背熟。
"""


def daily_temperatures(temperatures: list[int]) -> list[int]:
    """返回每天需要等多少天才能遇到更高温；用单调递减栈 O(n) 求解。"""
    n = len(temperatures)
    answer = [0] * n          # 没被结算的默认就是 0
    st: list[int] = []        # 单调栈，存索引（对应温度从栈底→栈顶递减）

    for i in range(n):
        # 当前温度比栈顶那天更热 → 栈顶等到了「第一个更高温度」，结算并弹出
        while st and temperatures[i] > temperatures[st[-1]]:
            top = st.pop()
            answer[top] = i - top
        st.append(i)          # 当前这天入栈，等它右边的更热天来结算它
    return answer


# ============================================================
# 第 10 题：反转链表（LeetCode 206）
# ============================================================
"""
题目描述
--------
给你单链表的头节点 head，反转链表，返回新的头节点。

输入：1 -> 2 -> 3 -> 4 -> 5 -> None
输出：5 -> 4 -> 3 -> 2 -> 1 -> None

思路：迭代法（三指针：prev / curr / next）
-----------------------------------------
反转的本质：把每个节点的 next 指针「掉头」，从指向下一个改成指向上一个。
但一旦改了 curr.next，就丢失了原来后面的节点，所以改之前必须先用 next 把后段接住。

三个指针：
  - prev：已经被反转好的那一段的头（初始 None，因为最开始没有任何节点被反转）。
  - curr：当前正在处理的节点（初始 head）。
  - next：临时保存 curr 原来的下一个节点，防止断链。

循环（curr 不为空时）：
  1. next = curr.next          # 先保存后段，否则下一步会丢失
  2. curr.next = prev          # 把当前节点指针掉头，指向「已经反转好的那段」
  3. prev = curr               # 当前节点成为新反转段的头
  4. curr = next               # 指针右移到原后段，处理下一个
  循环结束（curr 为 None）时，prev 正好是整条链表的新头。

流程示意（链表 1 -> 2 -> 3 -> None，每轮展示 prev / curr / next 指向）
--------------------------------------------------------------------------------
初始：  prev = None      curr → 1 → 2 → 3 → None      next = ?

第1轮： next = 2
        curr.next = prev (1→None)        → 1 -> None
        prev = 1, curr = 2
        状态： prev → 1 -> None；  curr → 2 → 3 -> None

第2轮： next = 3
        curr.next = prev (2→1)           → 2 -> 1 -> None
        prev = 2, curr = 3
        状态： prev → 2 -> 1 -> None；  curr → 3 -> None

第3轮： next = None
        curr.next = prev (3→2)           → 3 -> 2 -> 1 -> None
        prev = 3, curr = None
        状态： prev → 3 -> 2 -> 1 -> None；  curr = None → 循环结束

返回 prev（=3），即新链表头 3 -> 2 -> 1 -> None  ✓

复杂度：
  时间 O(n)（每个节点访问一次）  空间 O(1)（只用了几个指针，原地反转）
面试易错点：
  - 一定要在第①步先把 next = curr.next 存下来，否则 curr.next = prev 之后链路就断了，
    后面的节点再也找不回来（经典手撕翻车点）。
  - 循环结束条件写 `while curr:`，返回 `prev`（不是 curr，curr 最后已经变成 None）。
  - 递归写法也常考，但迭代更稳、不爆栈，面试优先写迭代。
"""
from typing import Optional
class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next
def reverse_list(head: ListNode) -> ListNode:
    prev: Optional["ListNode"] = None
    curr: ListNode = head

    while curr is not None:
        # 保存curr的下一个节点
        next = curr.next
        # 反转curr指向
        curr.next = prev
        # 向后移动一个节点
        prev = curr
        curr = next

    return prev

# ============================================================
# 测试辅助：把 list 转链表 / 链表转 list（仅为验证，不影响解法）
# ============================================================
def _build_linked_list(vals: list[int]) -> "ListNode | None":
    """把 Python 列表转成单链表。空列表返回 None。"""
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def _linked_list_to_list(head: "ListNode | None") -> list[int]:
    """把单链表转回 Python 列表，方便断言。"""
    out: list[int] = []
    cur = head
    while cur is not None:
        out.append(cur.val)
        cur = cur.next
    return out


# ============================================================
# 测试用例：直接运行本文件即可验证
# ============================================================
def _run_tests() -> None:
    print("=" * 60)
    print("第 9 题：每日温度（LeetCode 739）")
    print("=" * 60)

    case1 = [73, 74, 75, 71, 69, 72, 76, 73]
    out1 = daily_temperatures(case1)
    expect1 = [1, 1, 4, 2, 1, 1, 0, 0]
    print(f"  输入  {case1}")
    print(f"  输出  {out1}")
    print(f"  期望  {expect1}   "
          f"[{'PASS' if out1 == expect1 else 'FAIL'}]")
    assert out1 == expect1

    case2 = [30, 40, 50, 60]
    out2 = daily_temperatures(case2)
    expect2 = [1, 1, 1, 0]
    print(f"  输入  {case2}  ->  {out2}  期望 {expect2}  "
          f"[{'PASS' if out2 == expect2 else 'FAIL'}]")
    assert out2 == expect2

    case3 = [30, 60, 90]  # 一路升温，每天都只等1天
    out3 = daily_temperatures(case3)
    expect3 = [1, 1, 0]
    print(f"  输入  {case3}  ->  {out3}  期望 {expect3}  "
          f"[{'PASS' if out3 == expect3 else 'FAIL'}]")
    assert out3 == expect3

    print()
    print("=" * 60)
    print("第 10 题：反转链表（LeetCode 206）")
    print("=" * 60)

    for vals in ([1, 2, 3, 4, 5], [1, 2], [1], []):
        head = _build_linked_list(vals)
        reversed_head = reverse_list(head)
        got = _linked_list_to_list(reversed_head)
        expect = vals[::-1]
        print(f"  输入 {vals}  ->  反转后 {got}  期望 {expect}  "
              f"[{'PASS' if got == expect else 'FAIL'}]")
        assert got == expect

    print("\n✅ 全部测试用例通过！")


if __name__ == "__main__":
    _run_tests()
