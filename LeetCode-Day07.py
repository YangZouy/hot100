"""
LeetCode 必刷100题 · Day 07（2026-07-19）
========================================
面试方向：AI 应用 / Agent 开发
今日题目：
  - 第 13 题：环形链表 II                     LeetCode 142   中等   频率 ⭐⭐⭐⭐⭐
  - 第 14 题：相交链表                         LeetCode 160   简单   频率 ⭐⭐⭐⭐

运行方式：
    python LeetCode-Day07.py
会自动执行所有测试用例并打印 PASS / FAIL。

每个题目都包含：① 思路讲解 ② 流程示意图（ASCII）③ 可运行代码 ④ 复杂度分析 ⑤ 面试易错点。
只给一种「通用解法」，方便记忆和手撕。

今日主题：链表双指针的进阶——Day 06 学了「快慢指针判环」只返回 有无环，
今天第 13 题在判环基础上「定位环的入口」；第 14 题是另一类经典双指针：
「两条链表长度不同，如何对齐起点」。两题都是面试高频，且解法极其优美。
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
    """把单链表转回 Python 列表，方便断言（遇到环会死循环，仅用于无环链表）。"""
    out: list[int] = []
    cur = head
    while cur is not None:
        out.append(cur.val)
        cur = cur.next
    return out


def _build_cycle(vals: list[int], pos: int) -> "tuple[ListNode | None, ListNode | None]":
    """
    构造带环链表，返回 (头节点, 环的入口节点)。
    pos = -1 表示无环（入口返回 None）。pos = k 表示尾节点连回下标 k 的节点。
    """
    head = _build_linked_list(vals)
    if head is None or pos < 0:
        return head, None
    nodes: list[ListNode] = []
    cur = head
    while cur is not None:
        nodes.append(cur)
        cur = cur.next
    # 尾节点(nodes[-1])连回 nodes[pos]，形成环
    nodes[-1].next = nodes[pos]
    return head, nodes[pos]


def _build_intersect(
    listA: list[int], listB: list[int], shared: list[int], intersect_val: int | None
) -> "tuple[ListNode | None, ListNode | None, ListNode | None]":
    """
    构造两条「在 shared 段相交」的链表。
    listA = listA 独有部分 + shared；listB = listB 独有部分 + shared。
    intersect_val 不为 None 时，shared 的首个值会被替换成 intersect_val，
    并作为真正的相交节点返回；为 None 时表示两链表不相交（shared=[]）。
    返回 (headA, headB, 相交节点(无则 None))。
    """
    headA = _build_linked_list(listA)
    headB = _build_linked_list(listB)

    if not shared:  # 不相交
        return headA, headB, None

    shared_head = _build_linked_list(shared)
    if intersect_val is not None:
        shared_head.val = intersect_val  # 标记相交节点值，便于核对

    # 把 A 走到尾部，接上 shared_head
    if headA is None:
        headA = shared_head
    else:
        tail = headA
        while tail.next is not None:
            tail = tail.next
        tail.next = shared_head

    # 把 B 走到尾部，接上同一个 shared_head（关键：是「同一个」节点对象）
    if headB is None:
        headB = shared_head
    else:
        tail = headB
        while tail.next is not None:
            tail = tail.next
        tail.next = shared_head

    return headA, headB, shared_head


# ============================================================
# 第 13 题：环形链表 II（LeetCode 142）
# ============================================================
"""
题目描述
--------
给定一个链表的头节点 head，判断链表中是否有环。如果有环，返回「环的入口节点」；
如果没有环，返回 None（/null）。

输入：head = [3,2,0,-4]，pos = 1（尾部连回下标1的节点）
输出：返回下标1的节点（值为 2 的节点）——即环的入口
输入：head = [1,2]，pos = 0 → 返回值为 1 的节点
输入：head = [1]，pos = -1 → 返回 None（无环）

朴素想法（哈希表）：遍历时把每个节点存进集合，遇到已在集合中的节点 → 它就是入口。
O(n) 时间、O(n) 空间。面试想要 O(1) 空间的解法 → Floyd 判圈算法（快慢指针）的进阶版。

思路：快慢指针（Floyd 算法，两阶段）
-----------------------------------------
阶段一（判环 + 找相遇点）：
  和 Day 06 的 #141 完全一样——slow 每次 1 步，fast 每次 2 步。
  若有环，两者必在环内某点「相遇」，记相遇节点为 meet。
  若无环，fast 先撞到 None，直接返回 None。

阶段二（定位入口）：这是本题的关键，也是面试官最爱追问的「为什么」。
  让 slow 重新回到 head，fast 留在相遇点 meet。
  然后 slow、fast 都「每次只走 1 步」。它们会在「环的入口节点」相遇。

为什么阶段二一定能找到入口？——一个简洁的数学推导：
  设：
     a = 从 head 到「入口节点」的距离（步数）
     b = 从「入口节点」到「相遇点 meet」的距离（沿环走）
     c = 环的周长
  相遇时：
     slow 走的总步数 = a + b
     fast 走的总步数 = a + b + n*c     （n 是 fast 在环里多绕的圈数，n≥1）
  因为 fast 速度是 slow 的 2 倍 → fast 步数 = 2 × slow 步数：
     a + b + n*c = 2*(a + b)
     => a + b = n*c
     => a = n*c - b = (n-1)*c + (c - b)
  注意 c - b 是什么？是从「相遇点 meet」沿环再走、回到「入口节点」的距离！
  所以「从 head 走 a 步」和「从 meet 走 (c-b) 步」到达的是同一个节点——就是入口节点。
  阶段二里：
     slow 从 head 走 a 步 → 到达入口；
     fast 从 meet 走 (n-1) 圈 + (c-b) 步 → 也到达入口；
  两者在入口相遇。证毕。

流程示意（有环：3->2->0->-4->2，入口是值为 2 的节点，环长 c=3）
--------------------------------------------------------------------------------
            ┌───────────────┐
            ↓               │
   head→3→2→0→-4 ───────────┘
         ↑___入口(a=1)___│
              相遇点meet：假设在 0（b=1，c-b=2）

阶段一（判环）：
步数   slow            fast
 0     →3              →3
 1     →2              →0        (fast 走两步：3→2→0)
 2     →0              →-4       (fast 走两步：0→-4→2... 等下，环是 2→0→-4→2)
 这里环顺序：2→0→-4→(回到2)。fast 在步1到了 0，步2从0走两步：0→-4→2，到 2；
 slow 从2走到0。
步数   slow            fast
 0     →3              →3
 1     →2              →0
 2     →0              →2        (0→-4→2)
 3     →-4             →0        (2→0 一步... 等等)
 （示意只为表达「必相遇」，真实相遇点取决于起点；关键是阶段二）
阶段一结束：slow 与 fast 在某节点 meet 相遇（有环）。

阶段二（定位入口）：slow 回 head，fast 留在 meet，都每次 1 步
步数   slow(从head)   fast(从meet)
 0     →3              →meet
 1     →2(入口!)       →meet走1步
 2     →0              →meet走2步=入口
 当 slow 到达入口(值2)的那一步，fast 也恰好走到入口 → 两者 is 同一节点 → 返回它。★

流程示意（无环：head=[1,2,3]，fast 先到 None）
--------------------------------------------------------------------------------
步数   slow            fast
 0     →1              →1
 1     →2              →3
 2     →3              →None      (fast 从3走两步：3→None)
阶段一循环结束未相遇 → 无环 → 返回 None  ✓

复杂度：
  时间 O(n)（阶段一相遇前步数 ≤ n，阶段二 slow 最多走 n 步）
  空间 O(1)（只用了 slow、fast 两个指针）
面试易错点：
  - 阶段二必须把「slow 重置回 head」，fast 留在 meet，且两者都改成「每次 1 步」。
    忘记重置 slow → 直接返回 meet，得到的是相遇点不是入口，结果错误。
  - 阶段二两个指针都在移动，循环条件是 `while slow is not fast:`，
    slow=slow.next; fast=fast.next。初始 slow=head、fast=meet，第一次可能已相等（meet 就是入口的退化情况），
    此时 while 不进，直接返回 head（正确）。
  - 返回的是「节点对象」本身（LeetCode 要求返回入口节点引用），不是它的值。
  - 阶段一若 fast 撞 None 直接返回 None，不要进入阶段二。
  - 「为什么是 2 倍速度」——回答见上面数学推导，面试官常深挖，背住 a=(n-1)c+(c-b) 这个等式。
"""


def detect_cycle(head: "ListNode | None") -> "ListNode | None":
    """返回环的入口节点；无环返回 None。Floyd 算法两阶段。"""
    slow = head
    fast = head

    # 阶段一：判环 + 找相遇点
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:           # 相遇，有环
            # 阶段二：定位入口
            slow = head            # slow 回到起点
            while slow is not fast:  # 注意：此时 fast 仍在相遇点，两者每次 1 步
                slow = slow.next
                fast = fast.next
            return slow            # 相遇点即入口
    return None                    # 无环

# ============================================================
# 第 14 题：相交链表（LeetCode 160）
# ============================================================
"""
题目描述
--------
给你两个单链表的头节点 headA 和 headB，找出并返回「两个单链表相交的起始节点」。
如果两个链表不存在相交节点，返回 None。

「相交」指：从某个节点开始，之后的节点两个链表完全共用（同一个节点对象），
而不是值相等。链表的尾部是共享的 Y 字形，不是 X 字形。

输入：listA = [4,1,8,4,5]，listB = [5,6,1,8,4,5]，相交节点值为 8
输出：返回值为 8 的那个节点（两链表共用的那个节点）
输入：listA = [2,6,4]，listB = [1,5]，不相交 → 返回 None

朴素想法（哈希表）：把 A 的所有节点放进集合，遍历 B 找第一个在集合里的节点。O(n+m) 时间 O(n) 空间。
面试更爱考的 O(1) 空间解法 → 双指针「接力跑」。

思路：双指针接力法（双指针走对方的路）
-----------------------------------------
核心矛盾：两条链表长度可能不同（设 lenA、lenB），导致它们「不是从同一起跑线出发」，
即使相交也对齐不上。

巧妙解法：让指针 pA、pB 分别遍历自己的链表，走到头后「切换到对方的链表头」继续走。
  - pA 的路径：A 全段 + B 全段
  - pB 的路径：B 全段 + A 全段
  - 两条路径总长度都是 lenA + lenB，所以 pA、pB 走过的「总步数」始终相等。

为什么这能找到交点？
  - 若两链表在距离各自尾部 d 处相交（即从交点到尾巴共 d 个节点）：
      pA 走完 A(=lenA) 后进入 B，再走 (lenB - d) 步到达交点；
      此时 pA 共走 lenA + lenB - d 步。
      pB 走完 B(=lenB) 后进入 A，再走 (lenA - d) 步到达交点；
      此时 pB 共走 lenB + lenA - d 步 = 同样步数。
      → 两者「同时」到达交点，相遇！返回该节点。
  - 若不相交（无交点）：
      pA 走完 A+B 到 None，pB 走完 B+A 也到 None，两者同步变成 None，循环结束返回 None。
      （相当于「在虚拟的 None 处相交」）

这个方法无需知道长度、无需额外空间，极为优雅，是面试高频标准答。

流程示意（相交：A=4->1->8->4->5，B=5->6->1->8->4->5，交点=8）
--------------------------------------------------------------------------------
A: 4 → 1 ─┐
           ├→ 8 → 4 → 5 → None
B: 5 → 6 →1 ┘
   （注意：1->8->4->5 这一段是「同一组节点」，两表共用）

pA 走： 4,1,8,4,5, (到None) 切到B头: 5,6,1,8,4,5 → 在 8 相遇
pB 走： 5,6,1,8,4,5, (到None) 切到A头: 4,1,8,4,5 → 在 8 相遇
两者都在第 (lenA+lenB-d) 步到达 8 → 同时相遇，返回 8。★

流程示意（不相交：A=2->6->4，B=1->5）
--------------------------------------------------------------------------------
pA: 2,6,4,None, 1,5,None
pB: 1,5,None, 2,6,4,None
两者同步到达 None → 返回 None。✓

复杂度：
  时间 O(n+m)（每个指针最多走 lenA+lenB 步）
  空间 O(1)（只用了两个指针）
面试易错点：
  - 切换链表不是「交换两条链表」，而是「指针走到 None 后，next 指向另一条链表的头」。
    经典写法：`pA = pA.next if pA else headB`，一行搞定。
  - 比较交点用 `pA is pB`（同一个节点对象），不是 `pA.val == pB.val`（值相等不算相交）。
  - 循环条件写 `while pA is not pB:`（不是 `while pA and pB`）。当不相交时
    两者会同时变 None，`pA is pB` 为 True（None is None），循环正常退出返回 None。
  - 若写成 `while pA and pB` 且相交，会漏掉「都走到 None 才相等」的退出，逻辑错。
  - 这个方法「天然处理」了长度不同和交点为 None 两种情况，不用特判，干净。
"""


def get_intersection_node(headA: "ListNode | None", headB: "ListNode | None") -> "ListNode | None":
    """返回两链表相交的起始节点；不相交返回 None。双指针接力法 O(1) 空间。"""
    pA, pB = headA, headB

    # 若相交，两者会在交点相遇；若不相交，两者会同时变成 None 退出循环
    while pA is not pB:
        # pA 走到头就切到 B 的头；否则正常后移
        pA = pA.next if pA is not None else headB
        pB = pB.next if pB is not None else headA
    return pA  # 相交时为交点节点；不相交时为 None

# ============================================================
# 测试用例：直接运行本文件即可验证
# ============================================================
def _run_tests() -> None:
    print("=" * 62)
    print("第 13 题：环形链表 II（LeetCode 142）")
    print("=" * 62)

    # 用例1：有环，pos=1（入口是值为 2 的节点）
    head1, entry1 = _build_cycle([3, 2, 0, -4], pos=1)
    res1 = detect_cycle(head1)
    ok1 = (res1 is entry1) and (res1 is not None) and (res1.val == 2)
    print(f"  有环 pos=1   -> 入口值 {res1.val if res1 else None}  期望 2   [{'PASS' if ok1 else 'FAIL'}]")
    assert ok1, "用例1失败：未正确定位环入口"

    # 用例2：有环，pos=0（入口是头节点，值为 1）
    head2, entry2 = _build_cycle([1, 2], pos=0)
    res2 = detect_cycle(head2)
    ok2 = (res2 is entry2) and (res2.val == 1)
    print(f"  有环 pos=0   -> 入口值 {res2.val if res2 else None}  期望 1   [{'PASS' if ok2 else 'FAIL'}]")
    assert ok2, "用例2失败：头节点为入口时定位错误"

    # 用例3：单节点自环（值为 1 指向自己）
    head3 = ListNode(1)
    head3.next = head3
    res3 = detect_cycle(head3)
    ok3 = (res3 is head3)
    print(f"  单节点自环   -> 入口值 {res3.val if res3 else None}  期望 1   [{'PASS' if ok3 else 'FAIL'}]")
    assert ok3, "用例3失败：单节点自环未识别"

    # 用例4：无环
    head4, entry4 = _build_cycle([1, 2, 3, 4], pos=-1)
    res4 = detect_cycle(head4)
    ok4 = (res4 is None)
    print(f"  无环 pos=-1  -> {res4}  期望 None  [{'PASS' if ok4 else 'FAIL'}]")
    assert ok4, "用例4失败：无环却返回了节点"

    # 用例5：单节点无环
    head5, entry5 = _build_cycle([1], pos=-1)
    res5 = detect_cycle(head5)
    ok5 = (res5 is None)
    print(f"  单节点无环   -> {res5}  期望 None  [{'PASS' if ok5 else 'FAIL'}]")
    assert ok5, "用例5失败：单节点无环未返回 None"

    print()
    print("=" * 62)
    print("第 14 题：相交链表（LeetCode 160）")
    print("=" * 62)

    # 用例1：相交，交点值 8（A=4,1,8,4,5；B=5,6,1,8,4,5）
    a1, b1, inter1 = _build_intersect([4, 1], [5, 6, 1], [8, 4, 5], intersect_val=8)
    r1 = get_intersection_node(a1, b1)
    ok_r1 = (r1 is inter1) and (r1 is not None) and (r1.val == 8)
    print(f"  相交(交点8)  -> 交点值 {r1.val if r1 else None}  期望 8   [{'PASS' if ok_r1 else 'FAIL'}]")
    assert ok_r1, "用例1失败：未找到相交节点"

    # 用例2：不相交（A=2,6,4；B=1,5）
    a2, b2, inter2 = _build_intersect([2, 6, 4], [1, 5], [], None)
    r2 = get_intersection_node(a2, b2)
    ok_r2 = (r2 is None)
    print(f"  不相交       -> {r2}  期望 None  [{'PASS' if ok_r2 else 'FAIL'}]")
    assert ok_r2, "用例2失败：不相交却返回了节点"

    # 用例3：相交于第一个节点（整个 B 都嵌在 A 后面，交点即 B 头）
    # A=1,2,3 ; B=3 (相交于值3)
    a3, b3, inter3 = _build_intersect([1, 2], [], [3], intersect_val=3)
    r3 = get_intersection_node(a3, b3)
    ok_r3 = (r3 is inter3) and (r3.val == 3)
    print(f"  相交于3      -> 交点值 {r3.val if r3 else None}  期望 3   [{'PASS' if ok_r3 else 'FAIL'}]")
    assert ok_r3, "用例3失败：相交于B头未识别"

    # 用例4：两条都为空
    r4 = get_intersection_node(None, None)
    ok_r4 = (r4 is None)
    print(f"  两表皆空     -> {r4}  期望 None  [{'PASS' if ok_r4 else 'FAIL'}]")
    assert ok_r4, "用例4失败：空链表处理错误"

    print("\n✅ 全部测试用例通过！")


if __name__ == "__main__":
    _run_tests()
