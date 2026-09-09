"""
LeetCode 必刷100题 · Day 08（2026-07-21）
========================================
面试方向：AI 应用 / Agent 开发
今日题目：
  - 第 15 题：删除链表的倒数第 N 个节点     LeetCode 19    中等   频率 ⭐⭐⭐⭐⭐
  - 第 16 题：有效的字母异位词             LeetCode 242   简单   频率 ⭐⭐⭐⭐

运行方式：
    python LeetCode-Day08.py
会自动执行所有测试用例并打印 PASS / FAIL。

每个题目都包含：① 思路讲解 ② 流程示意图（ASCII）③ 可运行代码 ④ 复杂度分析 ⑤ 面试易错点。
只给一种「通用解法」，方便记忆和手撕。

今日主题：第 15 题是「快慢指针在链表删除」里的经典——它和 Day 07 判环/相交不同，
这里是「让两个指针间隔固定距离同步前进，从而精准定位要删的前驱节点」。
第 16 题是哈希表/计数的入门题，看似简单，却是「计数法 vs 排序法」思维差异的代表，
也是面试里常用来追问「能不能 O(1) 空间」的引子。
"""

# ============================================================
# 公共结构：单链表节点（LeetCode 标准定义，第 15 题用）
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
# 第 15 题：删除链表的倒数第 N 个节点（LeetCode 19）
# ============================================================
"""
题目描述
--------
给你一个链表，删除链表的「倒数第 n 个」节点，并返回链表的头节点。
（题目保证 n 有效：1 ≤ n ≤ 链表长度）

输入：head = [1,2,3,4,5]，n = 2  → 输出 [1,2,3,5]   （删掉值为 4 的节点）
输入：head = [1]，n = 1           → 输出 []          （删掉唯一的节点）
输入：head = [1,2]，n = 1         → 输出 [1]         （删掉尾部）
输入：head = [1,2]，n = 2         → 输出 [2]         （删掉头部）

朴素想法（两遍扫描）：
  第一遍遍历求链表长度 L；第二遍走到第 (L - n) 个节点（即倒数第 n 个的「前驱」），
  执行 pre.next = pre.next.next 删掉它。时间 O(L)、空间 O(1)。
  缺点：要扫两遍，且处理「删除头节点」要特判（没有前驱）。

更优通用解法：快慢指针（一次扫描 + dummy 哨兵节点）
---------------------------------------------------
核心思想：让两个指针 fast、slow 之间始终「保持 n+1 个节点的间隔」。
  - 先让 fast 从起点向前走 (n+1) 步；
  - 然后 fast 和 slow 同时每次走 1 步，直到 fast 抵达 None（链表尾之后）。
  - 此时 slow 正好停在「倒数第 n 个节点的前驱」（因为两者的间隔恒为 n+1，
    fast 到 None 时，slow 与它相差 n+1 个位置 → slow 在倒数第 n+1 个）。

为什么要走 (n+1) 步而不是 n 步？
  - 链表删除需要「前驱节点」去改 .next 指针。
  - 若只保持 n 个间隔，fast 到末尾时 slow 正好在「倒数第 n 个」节点本身，
    你没法从它自身删掉自己（缺前驱）。
  - 保持 (n+1) 间隔，slow 落在「要删节点的前一个」，直接 slow.next = slow.next.next 即可。

为什么用 dummy 哨兵节点（虚拟头）？
  - 当要删的是「头节点」时（例如 n == 链表长度），slow 会停在 dummy 上，
    dummy.next = dummy.next.next 自然把原头节点摘掉，无需任何特判。
  - 这是链表题里极常用的「加哨兵避免头节点特判」技巧，面试加分。

流程示意（链表 1→2→3→4→5，删倒数第 2 个，间隔 = n+1 = 3）
--------------------------------------------------------------------------------
初始：dummy→1→2→3→4→5→None
       ↑slow,fast (都从 dummy 出发)

① fast 先走 3 步（n+1）：
dummy→1→2→3→4→5→None
          ↑fast (走了3步到值为3的节点)
slow 还在 dummy

② fast、slow 同时每次走 1 步，直到 fast 到 None：
step0: slow=dummy,  fast=3
step1: slow=1,      fast=4
step2: slow=2,      fast=5
step3: slow=3,      fast=None  → 停止（fast 到尾之后）

③ 此时 slow 停在值 3 的节点，slow.next 就是要删的「值 4」节点：
   执行 slow.next = slow.next.next  →  3 指向 5
结果：1→2→3→5  ✓  （倒数第 2 个=4 被删除）

边界情况示意（删头节点：链表 1→2，n=2，间隔=3）
--------------------------------------------------------------------------------
初始：dummy→1→2→None
fast 先走 3 步 → fast 到 None（dummy→1→2→None，第3步超出）
while 不进，slow 停在 dummy
执行 dummy.next = dummy.next.next  →  dummy.next 从 1 变成 2
结果：2→None，即 [2]  ✓ （原头 1 被删除，无特判）

复杂度：
  时间 O(L)（fast 总共走 L+1 步，slow 走 L-n 步，都只扫一遍）
  空间 O(1)（只用了 fast、slow 两个指针，外加一个 dummy 节点）
面试易错点：
  - 最容易错的是「间隔到底是 n 还是 n+1」。记住：要删节点需要前驱，
    所以 fast 比 slow 多走 1 步 → 间隔 = n+1。先走 n+1 步。
  - 一定要加 dummy 哨兵节点，否则删头节点要额外特判，容易漏。
    dummy = ListNode(0); dummy.next = head，最后 return dummy.next。
  - fast 先走时用 for 循环 range(n+1)，但要保证 n 有效（题目保证有效，
    不用处理 n 超界；若想健壮可在循环里判 fast is None）。
  - while 循环条件写 `while fast is not None:`（fast 走到 None 才停），
    不是 `while fast.next` —— 否则 fast 停在最后一个节点，slow 会差一位。
  - 删除操作就一行：slow.next = slow.next.next，别写成 slow = slow.next（那只是移动指针）。
"""


def remove_nth_from_end(head: "ListNode | None", n: int) -> "ListNode | None":
    """删除链表倒数第 n 个节点，返回新头。快慢指针 + dummy 哨兵，一次扫描。"""
    dummy = ListNode(0)
    dummy.next = head

    fast = slow = dummy

    # fast 先走 (n+1) 步，让 fast 与 slow 间隔 n+1 个节点
    for _ in range(n + 1):
        fast = fast.next

    # fast、slow 同步前进，直到 fast 走到 None（尾之后）
    while fast is not None:
        fast = fast.next
        slow = slow.next

    # slow 现在停在「要删节点的前驱」，删除 slow.next
    slow.next = slow.next.next

    return dummy.next


# ============================================================
# 第 16 题：有效的字母异位词（LeetCode 242）
# ============================================================
"""
题目描述
--------
给定两个字符串 s 和 t，判断它们是否是「字母异位词」。
「字母异位词」= 两个字符串由完全相同的字符组成，且每个字符出现的次数也完全相同，
只是排列顺序不同。（本题输入限定为小写英文字母 a-z）

输入：s = "anagram", t = "nagaram"  → true   （字母和次数都一样，只是顺序不同）
输入：s = "rat",     t = "car"      → false  （r 和 c 不同）
输入：s = "a",       t = "a"        → true
输入：s = "ab",      t = "a"        → false  （长度都不同）

朴素想法（排序法）：
  把两个字符串各自排序，排序后若完全相同则是异位词。
  sorted(s) == sorted(t)。时间 O(n log n)，空间 O(n)。
  能跑通，但排序有 log n 的额外代价，面试里一般希望 O(n)。

通用解法（计数法 / 哈希表）
---------------------------
核心判定：两个字符串是异位词 ⇔ 它们每个字符的出现次数「完全相等」（多重集合相等）。

两种等价实现，思路一样——统计每个字符出现了多少次：
  ① 数组计数（限定小写字母 a-z，用长度 26 的数组，空间 O(1)）：
     先判长度是否相等（不等直接 false，省一次计数）；
     遍历 s 时数组[字符] += 1，遍历 t 时数组[字符] -= 1；
     最后数组若全为 0 → 异位词，否则不是。
  ② 哈希表计数（更通用，字符集不限，例如含大写/中文/emoji）：
     直接用 collections.Counter，Counter(s) == Counter(t) 即判定多重集合相等。

本题给「数组计数」作为主解法（手写最稳、空间 O(1)、面试官最爱看），
并在讲解末尾用一句话说明 Counter 的等价写法，兼顾通用性。

为什么先判长度？
  异位词长度必然相等。长度不同直接返回 false，省掉后续所有计数操作，
  既是正确性的快速剪枝，也展示了「面试时先想边界/特例」的意识。

流程示意（s="anagram", t="nagaram"）
--------------------------------------------------------------------------------
计数数组 cnt[0..25] 初始全 0（对应 a..z）
① 遍历 s="anagram"，遇到字符就 +1：
   a→+1, n→+1, a→+1, g→+1, r→+1, a→+1, m→+1
   cnt: a=3, n=1, g=1, r=1, m=1，其余 0
② 遍历 t="nagaram"，遇到字符就 -1：
   n→-1, a→-1, g→-1, a→-1, r→-1, a→-1, m→-1
   cnt 全部归零 → 所有元素 == 0 → 返回 true  ✓

流程示意（s="rat", t="car"）
--------------------------------------------------------------------------------
长度 3 == 3，继续计数。
s="rat": r+1, a+1, t+1  → cnt: r=1,a=1,t=1
t="car": c-1, a-1, r-1  → cnt: c=-1,a=0,r=0,t=1
最终 cnt 不全为 0（c=-1, t=1）→ 返回 false  ✓

（Counter 等价写法：
   from collections import Counter
   return len(s) == len(t) and Counter(s) == Counter(t)
 一行搞定，原理完全相同，只是把「+1/-1 数组」换成「哈希表计数」。）

复杂度：
  时间 O(n)（n 为两串长度，各遍历一遍；排序法是 O(n log n)，计数法更优）
  空间 O(1)（数组计数法只用固定 26 长度的数组；Counter 法为 O(1)~O(字符种类数)）
面试易错点：
  - 先用 len(s) != len(t) 快速返回 false，这是正确且高效的第一步，别漏。
  - 比较的是「字符出现次数的多重集合」相等，不是「排序后字符串相等」。
    排序法多一个 log n，面试里计数法更受青睐。
  - 数组计数法按下标：ord(ch) - ord('a') 把 'a'..'z' 映射到 0..25。
    别写成 cnt[ch]，ch 是字符不是下标会报错。
  - 最后判定要「数组所有元素都为 0」(any(cnt) 为 False / all(c==0))，
    不能只判某个字符。
  - 若题目字符集不限（含大写或 Unicode），数组 26 不适用，改用 Counter/字典，
    这也是面试常追问的「如果字符不是只有小写字母怎么办」。
"""


def is_anagram(s: str, t: str) -> bool:
    """判断 s、t 是否为字母异位词。数组计数法，O(n) 时间 O(1) 空间。"""
    # 长度不同一定不是异位词，直接返回（快速剪枝 + 正确性保证）
    if len(s) != len(t):
        return False

    # 长度 26 的计数数组，对应 'a'..'z'
    cnt = [0] * 26

    # 遍历 s：对应字符计数 +1
    for ch in s:
        cnt[ord(ch) - ord("a")] += 1
    # 遍历 t：对应字符计数 -1
    for ch in t:
        cnt[ord(ch) - ord("a")] -= 1

    # 若所有计数都归零 → 两串字符及次数完全相同 → 是异位词
    return all(c == 0 for c in cnt)

# ============================================================
# 测试用例：直接运行本文件即可验证
# ============================================================
def _run_tests() -> None:
    print("=" * 62)
    print("第 15 题：删除链表的倒数第 N 个节点（LeetCode 19）")
    print("=" * 62)

    # 用例1：常规删倒数第2个
    h1 = _build_linked_list([1, 2, 3, 4, 5])
    r1 = remove_nth_from_end(h1, 2)
    ok1 = _linked_list_to_list(r1) == [1, 2, 3, 5]
    print(f"  [1,2,3,4,5] n=2 -> {_linked_list_to_list(r1)}  期望 [1,2,3,5]  [{'PASS' if ok1 else 'FAIL'}]")
    assert ok1, "用例1失败"

    # 用例2：删唯一节点（链表长度1）
    h2 = _build_linked_list([1])
    r2 = remove_nth_from_end(h2, 1)
    ok2 = _linked_list_to_list(r2) == []
    print(f"  [1] n=1        -> {_linked_list_to_list(r2)}  期望 []          [{'PASS' if ok2 else 'FAIL'}]")
    assert ok2, "用例2失败"

    # 用例3：删尾部（n=1）
    h3 = _build_linked_list([1, 2])
    r3 = remove_nth_from_end(h3, 1)
    ok3 = _linked_list_to_list(r3) == [1]
    print(f"  [1,2] n=1      -> {_linked_list_to_list(r3)}  期望 [1]         [{'PASS' if ok3 else 'FAIL'}]")
    assert ok3, "用例3失败"

    # 用例4：删头部（n=长度）
    h4 = _build_linked_list([1, 2])
    r4 = remove_nth_from_end(h4, 2)
    ok4 = _linked_list_to_list(r4) == [2]
    print(f"  [1,2] n=2      -> {_linked_list_to_list(r4)}  期望 [2]         [{'PASS' if ok4 else 'FAIL'}]")
    assert ok4, "用例4失败"

    # 用例5：删头（n=5，长链表）
    h5 = _build_linked_list([1, 2, 3, 4, 5])
    r5 = remove_nth_from_end(h5, 5)
    ok5 = _linked_list_to_list(r5) == [2, 3, 4, 5]
    print(f"  [1,2,3,4,5] n=5 -> {_linked_list_to_list(r5)}  期望 [2,3,4,5]   [{'PASS' if ok5 else 'FAIL'}]")
    assert ok5, "用例5失败"

    # 用例6：删尾（n=1，长链表）
    h6 = _build_linked_list([1, 2, 3, 4, 5])
    r6 = remove_nth_from_end(h6, 1)
    ok6 = _linked_list_to_list(r6) == [1, 2, 3, 4]
    print(f"  [1,2,3,4,5] n=1 -> {_linked_list_to_list(r6)}  期望 [1,2,3,4]   [{'PASS' if ok6 else 'FAIL'}]")
    assert ok6, "用例6失败"

    print()
    print("=" * 62)
    print("第 16 题：有效的字母异位词（LeetCode 242）")
    print("=" * 62)

    # 用例1：标准异位词
    ok_r1 = is_anagram("anagram", "nagaram") is True
    print(f"  'anagram' vs 'nagaram' -> {is_anagram('anagram', 'nagaram')}  期望 True  [{'PASS' if ok_r1 else 'FAIL'}]")
    assert ok_r1, "用例1失败"

    # 用例2：字符不同
    ok_r2 = is_anagram("rat", "car") is False
    print(f"  'rat' vs 'car'        -> {is_anagram('rat', 'car')}  期望 False [{'PASS' if ok_r2 else 'FAIL'}]")
    assert ok_r2, "用例2失败"

    # 用例3：单字符相同
    ok_r3 = is_anagram("a", "a") is True
    print(f"  'a' vs 'a'            -> {is_anagram('a', 'a')}  期望 True  [{'PASS' if ok_r3 else 'FAIL'}]")
    assert ok_r3, "用例3失败"

    # 用例4：单字符不同
    ok_r4 = is_anagram("a", "b") is False
    print(f"  'a' vs 'b'            -> {is_anagram('a', 'b')}  期望 False [{'PASS' if ok_r4 else 'FAIL'}]")
    assert ok_r4, "用例4失败"

    # 用例5：长度不同（快速返 false）
    ok_r5 = is_anagram("ab", "a") is False
    print(f"  'ab' vs 'a'           -> {is_anagram('ab', 'a')}  期望 False [{'PASS' if ok_r5 else 'FAIL'}]")
    assert ok_r5, "用例5失败"

    # 用例6：两空串（互为异位词）
    ok_r6 = is_anagram("", "") is True
    print(f"  '' vs ''              -> {is_anagram('', '')}  期望 True  [{'PASS' if ok_r6 else 'FAIL'}]")
    assert ok_r6, "用例6失败"

    print("\n✅ 全部测试用例通过！")


if __name__ == "__main__":
    _run_tests()
