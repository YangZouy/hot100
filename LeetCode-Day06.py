"""
LeetCode 必刷100题 · Day 06（2026-07-18）
========================================
面试方向：AI 应用 / Agent 开发
今日题目：
  - 第 11 题：合并两个有序链表                 LeetCode 21    简单   频率 ⭐⭐⭐⭐⭐
  - 第 12 题：环形链表                         LeetCode 141   简单   频率 ⭐⭐⭐⭐⭐

运行方式：
    python LeetCode-Day06.py
会自动执行所有测试用例并打印 PASS / FAIL。

每个题目都包含：① 思路讲解 ② 流程示意图（ASCII）③ 可运行代码 ④ 复杂度分析 ⑤ 面试易错点。
只给一种「通用解法」，方便记忆和手撕。
"""

# ============================================================
# 公共结构：单链表节点（LeetCode 标准定义，两题共用）
# ============================================================
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None) -> None:
        self.val = val
        self.next = next


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
# 第 11 题：合并两个有序链表（LeetCode 21）
# ============================================================
"""
题目描述
--------
将两个升序链表合并为一个新的「升序链表」并返回。新链表由拼接给定的两个链表的所有节点组成。
（新链表节点就是原来那两个链表的节点，不要新建额外节点值——面试常问这点。）

输入：l1 = [1,2,4], l2 = [1,3,4]
输出：[1,1,2,3,4,4]

朴素想法（递归，代码最短但易爆栈）：merge(l1,l2) = min 那个节点接到剩下部分的 merge 结果上。
通用且稳的写法是「迭代 + 哑节点(dummy)」，面试优先写这个。

思路：迭代法（哑节点 + 双指针）
-----------------------------------------
核心任务：每次从两条链表头部挑一个「当前最小」的节点，接到结果链表尾部。
难点在于「结果链表的头节点不确定、要动态接」。用一个 dummy 哑节点统一处理：
- dummy 是一个不存真实数据的哨兵节点，tail 一开始指向 dummy。
- p1、p2 分别指向 l1、l2 当前待比较的节点。
- 循环（p1 和 p2 都非空时）：
      比较 p1.val 与 p2.val：
      谁小，就把谁接到 tail 后面（tail.next = 较小者），然后该指针后移一步，tail 也后移一步。
- 循环结束后，必有一条链表先走完。把另一条链表的剩余部分整段接到 tail.next（剩余部分已经有序，直接接即可）。
- 返回 dummy.next（真正的结果头节点；dummy 本身被丢弃）。

为什么用 dummy？因为不预先知道结果头是谁，若不用 dummy，处理第一个节点要单独写分支；
dummy 让我们「插入第一个节点」和「插入后续节点」走同一条代码路径，干净且不易错。

流程示意（l1 = 1->2->4->None，l2 = 1->3->4->None）
--------------------------------------------------------------------------------
初始：  dummy -> ...
        tail = dummy
        p1 → 1→2→4→None      p2 → 1→3→4→None

第1轮： p1.val=1, p2.val=1，p1 较小（相等取谁都行，这里取 p1）
        tail.next = p1  → dummy -> 1
        tail = p1(=1), p1 = p1.next(=2)
        状态： dummy -> 1 -> ...； p1 → 2→4, p2 → 1→3→4

第2轮： p1.val=2, p2.val=1，p2 较小
        tail.next = p2  → 1 -> 1
        tail = p2(=1), p2 = p2.next(=3)
        状态： dummy -> 1 -> 1 -> ...； p1 → 2→4, p2 → 3→4

第3轮： p1.val=2, p2.val=3，p1 较小
        tail.next = p1  → ... -> 2
        tail = p1(=2), p1 = p1.next(=4)
        状态： ... -> 1 -> 2 -> ...； p1 → 4, p2 → 3→4

第4轮： p1.val=4, p2.val=3，p2 较小
        tail.next = p2  → ... -> 3
        tail = p2(=3), p2 = p2.next(=4)
        状态： ... -> 2 -> 3 -> ...； p1 → 4, p2 → 4

第5轮： p1.val=4, p2.val=4，p1 较小
        tail.next = p1  → ... -> 4
        tail = p1(=4), p1 = p1.next(=None)
        状态： ... -> 3 -> 4 -> ...； p1 = None, p2 → 4

循环结束（p1 已空）：tail.next = p2  → ... -> 4 -> 4 -> None
返回 dummy.next = 1->1->2->3->4->4->None  ✓

复杂度：
  时间 O(n+m)（每个节点访问一次，n、m 为两链表长度）
  空间 O(1)（只用了几个指针，原地重接，没有新建节点）
面试易错点：
  - 循环条件是 `while p1 and p2`（两个都还有），不是 `while p1 or p2`。
  - 循环结束必须把「非空的那条剩余部分」整段接上：`tail.next = p1 if p1 else p2`。
    漏掉这一步，结果链表就只到一半，面试直接挂。
  - 比较时相等取哪边都行（左或右），不要纠结——关键是「每次只接一个最小节点」。
  - 返回 `dummy.next`，不是 dummy。
  - 题目说「拼接节点」意味着直接复用原节点重指 next，不要去 new 新节点（除非面试官要求深拷贝）。
"""


def merge_two_lists(l1: "ListNode | None", l2: "ListNode | None") -> "ListNode | None":
    """合并两个升序链表，返回新的升序链表头。迭代法 + 哑节点。"""
    dummy = ListNode(0)          # 哑节点，简化头节点处理
    tail = dummy                 # tail 始终指向结果链表的「当前尾」
    p1, p2 = l1, l2

    while p1 is not None and p2 is not None:
        if p1.val <= p2.val:     # 取较小的接到 tail 后面（相等优先取 l1，无所谓）
            tail.next = p1
            p1 = p1.next
        else:
            tail.next = p2
            p2 = p2.next
        tail = tail.next         # tail 后移一步

    # 必有一条先走完，把另一条剩余部分整段接上（已是有序，直接接）
    tail.next = p1 if p1 is not None else p2
    return dummy.next


# ============================================================
# 第 12 题：环形链表（LeetCode 141）
# ============================================================
"""
题目描述
--------
给你一个链表的头节点 head，判断链表中是否有环。
「环」指链表中某个节点的 next 指向在它前面出现过的节点，使得链表在尾部形成闭环。

输入：head = [3,2,0,-4]，pos = 1（即尾部连回下标1的节点）→ 有环 → true
输入：head = [1,2]，pos = 0 → 有环 → true
输入：head = [1]，pos = -1 → 无环 → false

朴素想法（哈希表）：遍历时把每个节点存进集合，若遇到已在集合中的节点 → 有环。O(n) 时间但 O(n) 空间。
面试更爱考的 O(1) 空间解法 → 快慢指针（Floyd 判圈算法）。

思路：快慢指针（Fast & Slow Pointer）
-----------------------------------------
想象两个人在环形跑道上跑步：快的人速度是慢的人的 2 倍。如果有环，快的人迟早会绕一圈追上慢的人（套圈）；
如果没环（是直线跑到尽头），快的人会先冲出终点（碰到 None）。

具体：
  - slow 每次走 1 步，fast 每次走 2 步（fast.next 和 fast.next.next 都要存在才走）。
  - 循环（fast 和 fast.next 都非空时，即还能继续走两步）：
        慢走一步：slow = slow.next
        快走两步：fast = fast.next.next
        若 slow is fast（指向同一个节点）→ 相遇，说明有环，返回 True。
  - 循环正常结束（fast 撞到 None）→ 无环，返回 False。

为什么快走 2 步、慢走 1 步必然相遇？
  - 一旦两者都进入环，把「慢指针位置」看作参照系，快指针相对它每一步逼近 1 个节点
    （快 +2、慢 +1，相对位移 +1），所以最多再过「环长」步必然追上，绝不会跳过。
  - 若快指针走 3 步，相对速度 2，可能在环长为偶数时「擦肩而过」错开，不如 2 步保险。

流程示意（有环：1->2->3->4->2 形成环，即 4 连回 2）
--------------------------------------------------------------------------------
         ┌─────────────┐
         ↓             │
  1 → 2 → 3 → 4 ───────┘

步数   slow            fast
 0     →1              →1
 1     →2              →3        (fast 走两步：1→2→3)
 2     →3              →2        (fast 从3走两步：3→4→2)
 3     →4              →4        (fast 从2走两步：2→3→4)  ★ slow is fast → 相遇，有环！

流程示意（无环：1->2->3->None）
--------------------------------------------------------------------------------
步数   slow            fast
 0     →1              →1
 1     →2              →3
 2     →3              →None     (fast 从3走两步：3→None，fast.next 为 None，循环结束)
循环结束未相遇 → 无环，返回 False  ✓

复杂度：
  时间 O(n)（无环时快指针到尾约 n/2 步；有环时相遇前走的步数也最多 O(n)）
  空间 O(1)（只用了两个指针，不用额外存储）
面试易错点：
  - 循环条件写 `while fast and fast.next:`（fast 要走两步，必须保证 fast.next 非空），
    写成 `while fast:` 在 fast.next.next 时会访问 None.next 直接报错。
  - 相遇判断用 `slow is fast`（同一节点对象），不是 `slow == fast`（这里等价但 is 更准确表达「同一个节点」）。
  - 返回的是「是否有环」(bool)，不要返回相遇节点——那是环形链表 II (#142) 的事。
  - 快慢指针是「链表判环 / 找中点 / 找倒数第 k 个」的通用套路，务必背熟。
"""


def has_cycle(head: "ListNode | None") -> bool:
    """判断链表是否有环。快慢指针 O(1) 空间。"""
    slow = head
    fast = head

    while fast is not None and fast.next is not None:
        slow = slow.next          # 慢走一步
        fast = fast.next.next     # 快走两步
        if slow is fast:          # 相遇 → 有环
            return True
    return False                  # 快指针冲出终点 → 无环

# ============================================================
# 测试用例：直接运行本文件即可验证
# ============================================================
def _run_tests() -> None:
    print("=" * 62)
    print("第 11 题：合并两个有序链表（LeetCode 21）")
    print("=" * 62)

    cases = [
        ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
        ([], [], []),
        ([], [0], [0]),
        ([5], [1, 2, 3], [1, 2, 3, 5]),
        ([-1, 2], [-2, 1], [-2, -1, 1, 2]),
    ]
    for l1_vals, l2_vals, expect in cases:
        l1 = _build_linked_list(l1_vals)
        l2 = _build_linked_list(l2_vals)
        merged = merge_two_lists(l1, l2)
        got = _linked_list_to_list(merged)
        ok = (got == expect)
        print(f"  l1={l1_vals}  l2={l2_vals}")
        print(f"    合并后 {got}  期望 {expect}  [{'PASS' if ok else 'FAIL'}]")
        assert ok, f"合并两个有序链表失败：得到 {got}，期望 {expect}"

    print()
    print("=" * 62)
    print("第 12 题：环形链表（LeetCode 141）")
    print("=" * 62)

    # 用例1：有环 1->2->3->4->2（尾连回下标1）
    h1 = _build_linked_list([1, 2, 3, 4])
    # 找到下标1的节点(2)和下标3的节点(4)
    nodes1 = []
    cur = h1
    while cur:
        nodes1.append(cur)
        cur = cur.next
    nodes1[3].next = nodes1[1]      # 4 -> 2，成环
    r1 = has_cycle(h1)
    print(f"  有环用例(尾连回下标1)  -> {r1}  期望 True  [{'PASS' if r1 else 'FAIL'}]")
    assert r1 is True

    # 用例2：无环 1->2->3->4
    h2 = _build_linked_list([1, 2, 3, 4])
    r2 = has_cycle(h2)
    print(f"  无环用例(1->2->3->4)   -> {r2}  期望 False  [{'PASS' if not r2 else 'FAIL'}]")
    assert r2 is False

    # 用例3：单节点有环（自己指向自己）
    h3 = ListNode(1)
    h3.next = h3
    r3 = has_cycle(h3)
    print(f"  单节点自环             -> {r3}  期望 True  [{'PASS' if r3 else 'FAIL'}]")
    assert r3 is True

    # 用例4：空链表
    r4 = has_cycle(None)
    print(f"  空链表                 -> {r4}  期望 False  [{'PASS' if not r4 else 'FAIL'}]")
    assert r4 is False

    print("\n✅ 全部测试用例通过！")


if __name__ == "__main__":
    _run_tests()
