# -*- coding: utf-8 -*-
"""
================================================================================
LeetCode 必刷 100 题 · Day 18（总表 #100，收官单题）
对应篇章：链表 / 堆 / 分治 —— 合并 K 个升序链表
================================================================================

本文件是「可直接运行的 Python 文件」，不是文档。
运行方式（在你本机终端，cd 到本文件所在目录后执行）：
    python LeetCode-Day18.py
所有题目的测试用例会在运行时自动跑，结尾打印 PASS/FAIL 汇总。
只要看到 "全部通过 ✅"，就说明代码逻辑正确，可以放心交。

今天 1 道题（LeetCode 题号）：
    #100  合并 K 个升序链表   (23)   优先队列（最小堆）/ 多路归并

为什么今天只有 1 道？
    这是「必刷 100 题」计划的收官题。Day 1~9 每天 2 题（共 18 题），
    Day 10~17 每天 10 题（共 80 题），加上今天的 #100，正好凑满 100 题。
    所以今天用这道「链表综合题」给整个计划画上句号。

为什么 #23 是收官？（它的含金量）
    - 它把前面练过的「链表操作(#19/#21/#206 改指针）」「堆/优先队列(#215 第K大也用堆）」
      「分治思想（Day14 前序+中序建树分治）」全都串起来了，是面试里检验
      「基础是否扎实」的经典题。
    - AI 应用 / Agent 开发岗面试中，它常被当作「能不能写出干净、可维护代码」的
      试金石，也是很多系统设计（多路归并、外部排序、日志合并）的微观缩影。

贯穿今天的解题心法：
    多路归并 = 「每次从 K 个有序序列的头部里挑最小的那个」。
    最通用的实现就是「最小堆」：把每条链表的头节点丢进堆，反复弹出最小、补它的 next。
================================================================================
"""

from typing import List, Optional
import heapq


# ---- 链表节点定义（LeetCode 官方 ListNode）----
class ListNode:
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None) -> None:
        self.val = val
        self.next = next


# ---- 测试辅助：把 Python 列表变成链表 / 把链表变回列表 ----
def build_list(vals: List[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> List[int]:
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res


# =============================================================================
# #100 合并 K 个升序链表 (LeetCode 23)  —— 最小堆（优先队列）多路归并
# =============================================================================
def problem_100_merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    r"""
    题目描述：
        给你一个链表的数组 lists，每个链表都已经按「升序」排列好了。
        请你把所有链表「合并成一个升序链表」，返回合并后的链表头节点。
        例：lists = [[1,4,5],[1,3,4],[2,6]]
            →  [1,1,2,3,4,4,5,6]

    思路（最小堆 / 优先队列，最通用也最好写）：
        核心动作叫「多路归并」：K 条有序链表，每一步都从「各链表当前头部」里挑最小的那个。
        具体做法：
          1. 建一个最小堆（Python 用 heapq）。
          2. 把每条链表的「头节点」push 进堆。注意堆里要存 (节点值, 链表编号, 节点)，
             用「链表编号」做第二关键字——因为 ListNode 不能比大小，而且两条链表可能
             出现相同的值，得靠编号区分谁先谁后，否则 heapq 会报错。
          3. 用一个 dummy 哨兵节点起手，cur 指针一路往后接。
          4. 循环：从堆里 pop 出当前最小的节点，把它接到 cur 后面；
             如果它还有 next，就把它的 next 也 push 进堆（补上这条链表的下一个候选）。
          5. 堆空了，所有链表就都归并完了，返回 dummy.next。

    为什么用堆？
        每次「找 K 个头里最小的」如果暴力扫描是 O(K)，用堆是 O(log K)，
        总共要取 N 次（N 是所有节点总数），所以总复杂度 O(N log K)。
        比「每次都线性扫一遍所有链表头」快得多。

    图示（lists = [[1,4,5],[1,3,4],[2,6]]）：
        初始：3 条链表的头分别是 1、1、2，全进堆
              heap = [(1,#0),(1,#1),(2,#2)]
        第1步 pop (1,#0) → 接到结果，它的 next 是 4 → 把 (4,#0) 进堆
              heap = [(1,#1),(2,#2),(4,#0)]     结果: 1
        第2步 pop (1,#1) → 接 1，next 是 3 → 进 (3,#1)
              heap = [(2,#2),(3,#1),(4,#0)]     结果: 1→1
        第3步 pop (2,#2) → 接 2，next 是 6 → 进 (6,#2)
              heap = [(3,#1),(4,#0),(6,#2)]     结果: 1→1→2
        第4步 pop (3,#1) → 接 3，next 是 4 → 进 (4,#1)
              heap = [(4,#0),(4,#1),(6,#2)]     结果: 1→1→2→3
        第5步 pop (4,#0) → 接 4（来自第0条），next 是 5 → 进 (5,#0)
              heap = [(4,#1),(5,#0),(6,#2)]     结果: 1→1→2→3→4
        第6步 pop (4,#1) → 接 4（来自第1条），该链已空，不再补
              heap = [(5,#0),(6,#2)]            结果: ...→4→4
        第7步 pop (5,#0) → 接 5，该链空
              heap = [(6,#2)]                   结果: ...→4→4→5
        第8步 pop (6,#2) → 接 6，该链空，堆空，结束
        最终：1→1→2→3→4→4→5→6  ✅

    时间复杂度：O(N log K)，N 为所有节点总数，K 为链表条数。
    空间复杂度：O(K)，堆里最多同时存 K 个节点（不计入返回结果本身）。

    面试易错点：
        - 堆里千万别只 push 节点！ListNode 不可比较、且同值会崩；必须带 (val, 编号)。
        - 空链表（[]）和空输入（lists=[]）都要跳过，否则 None 进堆直接报错。
        - 也可以用「分治两两合并」（像归并排序）做到同样 O(N log K)。堆写法更短更稳，
          面试首推堆；分治写法在「K 巨大、单条很短」时内存更省，可作为补充话术。
    """
    dummy = ListNode(0)
    cur = dummy
    heap: List[tuple] = []
    for i, head in enumerate(lists):
        if head:                                  # 跳过空链表，避免 None 进堆
            heapq.heappush(heap, (head.val, i, head))
    while heap:
        val, i, node = heapq.heappop(heap)
        cur.next = node
        cur = cur.next
        if node.next:                             # 这条链还有后继，补进堆当候选
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next


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

    # ---- #100 合并 K 个升序链表 (23) ----
    print("\n#100 合并 K 个升序链表 (23):")
    lists = [build_list([1, 4, 5]), build_list([1, 3, 4]), build_list([2, 6])]
    check("[[1,4,5],[1,3,4],[2,6]] -> [1,1,2,3,4,4,5,6]",
          to_list(problem_100_merge_k_lists(lists)),
          [1, 1, 2, 3, 4, 4, 5, 6])

    check("[] -> []  (空输入)",
          to_list(problem_100_merge_k_lists([])), [])

    check("[[ ]] -> []  (含空链表)",
          to_list(problem_100_merge_k_lists([build_list([])])), [])

    check("[[1],[0]] -> [0,1]",
          to_list(problem_100_merge_k_lists([build_list([1]), build_list([0])])),
          [0, 1])

    check("[[1,2,3],[4,5,6],[7,8,9]] -> 三段顺序接",
          to_list(problem_100_merge_k_lists(
              [build_list([1, 2, 3]), build_list([4, 5, 6]), build_list([7, 8, 9])])),
          [1, 2, 3, 4, 5, 6, 7, 8, 9])

    check("[[2],[],[-1]] -> [-1,2]  (含负数/空链)",
          to_list(problem_100_merge_k_lists(
              [build_list([2]), build_list([]), build_list([-1])])),
          [-1, 2])

    check("[[1,3,5,7],[2,4,6,8],[0,9]] -> 全量归并",
          to_list(problem_100_merge_k_lists(
              [build_list([1, 3, 5, 7]), build_list([2, 4, 6, 8]), build_list([0, 9])])),
          [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    # ---- 汇总 ----
    print("\n" + "=" * 60)
    print(f"测试结果：{passed}/{total} 通过")
    if passed == total:
        print("全部通过 ✅  —— 今天的题目逻辑正确，可以放心交。")
        print()
        print("🎉 恭喜！这是「必刷 100 题」计划的第 100 题，也是收官题。")
        print("   Day 1~9（每天2题）+ Day 10~17（每天10题）+ 今天 #100 = 共 100 题全部完成。")
        print("   建议下一步：把做错的、靠背的题挑出来二刷；重点练「讲思路+复杂度+边界」。")
    else:
        print("有失败用例 ❌  —— 上面 FAIL 处已打印期望/实际，请检查。")
    print("=" * 60)


if __name__ == "__main__":
    _run_tests()
