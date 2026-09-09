"""
Hot100 自测批改器  ·  专治「写了代码也不知道写的是否正确」
========================================================
这是给你的「练习体检仪」。你照着 Hot100-Day01~03（简单档）默写完后，
把代码写进 `test.py`（和你这份批改器放在同一个目录 D:/wiki/刷题/ 下）。
然后运行本文件：

    python Hot100-自测批改器.py

它会：
  1. 自动读取你的 `test.py`；
  2. 对里面每一个函数跑一组「标准测试用例」；
  3. 逐题打印 ✅ / ❌，❌ 时指出错误（异常 or 输出不对）；
  4. 凡是写错/没写的题，直接把「标准参考答案」贴出来，当场对照学会。

设计原则：
  - 只读你的 test.py，绝不改动它；
  - 每题独立 try/except，一道题崩了不影响其他题评分；
  - 参考答案是「通用解法」，和你 Hot100 文件里的一致，方便对照。

⚠️ 前提：你的 test.py 里函数名要和下面 REGISTRY 里的名字一致
（目前我已经按你今天 01:08 写的 test.py 的函数名对齐好了）。
如果哪天你改了函数名，本批改器会提示「未找到函数」。
"""

import importlib.util
import os
import sys
import traceback
from collections import defaultdict


# ============================================================
# 基础数据结构（链表 / 树），用来构造测试输入
# ============================================================
class ListNode:
    def __init__(self, val=0, nxt=None):
        self.val = val
        self.next = nxt


def build_list(xs):
    """[1,2,3] -> 1->2->3->None"""
    head = None
    for v in reversed(xs):
        head = ListNode(v, head)
    return head


def to_list(head):
    out = []
    p = head
    while p:
        out.append(p.val)
        p = p.next
    return out


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(xs):
    """层序数组 -> 树，None 表示空。如 [3,9,20,None,None,15,7]"""
    if not xs:
        return None
    root = TreeNode(xs[0])
    q = [root]
    i = 1
    for node in q:
        if i < len(xs) and xs[i] is not None:
            node.left = TreeNode(xs[i])
            q.append(node.left)
        i += 1
        if i < len(xs) and xs[i] is not None:
            node.right = TreeNode(xs[i])
            q.append(node.right)
        i += 1
    return root


def inorder(root, out=None):
    if out is None:
        out = []
    if root:
        inorder(root.left, out)
        out.append(root.val)
        inorder(root.right, out)
    return out


def to_level(root):
    """树 -> 层序数组（裁掉尾部 None），用来比较树结构"""
    if not root:
        return []
    res = []
    q = [root]
    while q:
        n = q.pop(0)
        if n is None:
            res.append(None)
            continue
        res.append(n.val)
        q.append(n.left)
        q.append(n.right)
    while res and res[-1] is None:
        res.pop()
    return res


# ============================================================
# 读取你的 test.py
# ============================================================
HERE = os.path.dirname(os.path.abspath(__file__))
TEST_PATH = os.path.join(HERE, "test.py")

user = None
if not os.path.exists(TEST_PATH):
    print(f"❌ 没找到 {TEST_PATH}")
    print("   请把你的练习文件命名为 test.py 放到本目录，再运行本批改器。")
    sys.exit(1)

try:
    spec = importlib.util.spec_from_file_location("user_practice", TEST_PATH)
    user = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(user)
    print(f"✅ 已读取你的练习文件：{TEST_PATH}\n")
except Exception as e:
    # 友好报错：不要把原始 traceback 甩给用户，给一句人话提示，并给出排查方向。
    # 典型场景：用户把练习文件写成了 JS / 其它语言，或文件还有语法错误没存好。
    print(f"❌ 读取你的 test.py 时整体报错，批改器无法继续。")
    if isinstance(e, SyntaxError):
        print(f"   → 看起来 test.py 不是有效的 Python 代码（模块级语法错误）。")
        print(f"     常见原因：① 文件里写成了 JavaScript / 其它语言；② 函数还没写完有语法错。")
        print(f"     请确认 test.py 是纯 Python，且函数名与 REGISTRY 对齐后再跑本批改器。")
        print(f"     出错位置：第 {e.lineno} 行附近 —— {str(e).splitlines()[-1]}")
    else:
        print(f"   → 错误类型：{type(e).__name__}：{e}")
    print(f"   （本批改器只读取、绝不改动你的 test.py，请放心修改后重跑。）")
    sys.exit(2)


# ============================================================
# 每题的「标准参考答案」（仅在❌时显示，用来对照学习）
# ============================================================
CANONICAL = {
    "two_sum": '''def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
    return []''',

    "group_anagrams": '''def group_anagrams(strs):
    groups = defaultdict(list)          # 注意：是 defaultdict(list)，不是 dict[...]
    for s in strs:
        key = "".join(sorted(s))        # 排序后的字符串作为「异位词签名」
        groups[key].append(s)           # 用 .append，不是 .appends
    return list(groups.values())''',

    "longest_consecutive": '''def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for num in s:                       # 遍历集合去重
        if num - 1 not in s:           # 只从「序列起点」出发，避免重复计数
            y = num
            while y + 1 in s:
                y += 1
            best = max(best, y - num + 1)
    return best''',

    "move_zeroes": '''def move_zeroes(nums):
    slow = 0                           # slow 指向「下一个非零该放的位置」
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1                   # 只有真正交换了才前进！''',

    "max_area": '''def max_area(height):
    l, r = 0, len(height) - 1
    ans = 0
    while l < r:
        ans = max(ans, min(height[l], height[r]) * (r - l))
        if height[l] < height[r]:       # 矮的那边没前途，向内移动
            l += 1
        else:
            r -= 1
    return ans''',

    "three_sum": '''def three_sum(nums):
    nums.sort()
    n = len(nums)
    res = []
    for i in range(n - 2):
        if nums[i] > 0: break           # 最小的数都 > 0，后面不可能凑出 0
        if i > 0 and nums[i] == nums[i - 1]: continue  # 跳过重复起点
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s == 0:
                res.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l + 1]: l += 1
                while l < r and nums[r] == nums[r - 1]: r -= 1
                l += 1; r -= 1
            elif s < 0:
                l += 1
            else:
                r -= 1
    return res''',

    "length_of_longest_substring": '''def length_of_longest_substring(s):
    last = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:   # 重复字符落在窗口内才需要收缩
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best''',

    "find_anagrams": '''def find_anagrams(s, p):
    from collections import Counter
    need = Counter(p)
    window = Counter()
    k = len(p)
    res = []
    for right, ch in enumerate(s):
        window[ch] += 1
        left = right - k + 1
        if left >= 0:
            if window == need:
                res.append(left)
            window[s[left]] -= 1                # 滑出左端字符
            if window[s[left]] == 0:
                del window[s[left]]
    return res''',

    "rotate": '''def rotate(nums, k):
    def rev(a, b):
        while a < b:
            nums[a], nums[b] = nums[b], nums[a]
            a += 1; b -= 1
    n = len(nums)
    k %= n
    rev(0, n - 1)        # 整体反转
    rev(0, k - 1)        # 反转前 k 个
    rev(k, n - 1)        # 反转剩余''',

    "merge_sorted_array": '''def merge_sorted_array(nums1, m, nums2, n):
    i, j, k = m - 1, n - 1, m + n - 1
    while i >= 0 and j >= 0:
        if nums1[i] > nums2[j]:
            nums1[k] = nums1[i]; i -= 1
        else:
            nums1[k] = nums2[j]; j -= 1
        k -= 1
    while j >= 0:                       # nums2 还有剩（nums1 前面已有序）
        nums1[k] = nums2[j]; j -= 1; k -= 1''',

    "get_intersection_node": '''def get_intersection_node(headA, headB):
    pa, pb = headA, headB
    while pa is not pb:                 # 走到头就跳到另一条链表头
        pa = pa.next if pa else headB
        pb = pb.next if pb else headA
    return pa                           # 相交则返回交点，否则都变成 None''',

    "reverse_list": '''def reverse_list(head):
    pre = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = pre
        pre = cur
        cur = nxt
    return pre''',

    "is_palindrome": '''def is_palindrome(head):
    # 1) 快慢指针找中点（fast 走两步，slow 走一步）
    fast = slow = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    # 2) 若长度为奇数，slow 多走一步跳过中心
    if fast:
        slow = slow.next
    # 3) 反转后半段
    prev = None
    while slow:
        nxt = slow.next
        slow.next = prev
        prev = slow
        slow = nxt
    # 4) 前后比较
    p = head
    while prev:
        if p.val != prev.val:
            return False
        p = p.next
        prev = prev.next
    return True''',

    "has_cycle": '''def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False''',

    "merge_two_lists": '''def merge_two_lists(l1, l2):
    if not l1: return l2
    if not l2: return l1
    if l1.val < l2.val:
        l1.next = merge_two_lists(l1.next, l2)
        return l1
    else:
        l2.next = merge_two_lists(l1, l2.next)
        return l2''',

    "inorder_traversal": '''def inorder_traversal(root):
    res, stack, cur = [], [], root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        res.append(cur.val)
        cur = cur.right
    return res''',

    "max_depth": '''def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))''',

    "invert_tree": '''def invert_tree(root):
    if not root:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root''',

    "is_symmetric": '''def is_symmetric(root):
    def mirror(a, b):
        if not a and not b: return True
        if not a or not b: return False
        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)
    return mirror(root, root)''',

    "diameter_of_binary_tree": '''def diameter_of_binary_tree(root):
    ans = 0
    def depth(n):
        nonlocal ans
        if not n: return 0
        l, r = depth(n.left), depth(n.right)
        ans = max(ans, l + r)          # 经过当前节点的最长路径 = 左深 + 右深
        return 1 + max(l, r)
    depth(root)
    return ans''',

    "sorted_array_to_bst": '''def sorted_array_to_bst(nums):
    def dfs(l, r):
        if l > r: return None
        m = (l + r) // 2              # 取中点做根 -> 天然平衡且为 BST
        root = TreeNode(nums[m])
        root.left = dfs(l, m - 1)
        root.right = dfs(m + 1, r)
        return root
    return dfs(0, len(nums) - 1)''',

    "search_insert": '''def search_insert(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        m = (l + r) // 2
        if nums[m] < target:
            l = m + 1
        else:
            r = m - 1
    return l                           # 循环结束 l 就是插入位置''',

    "is_valid": '''def is_valid(s):
    mp = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in mp:                  # 是右括号
            if not stack or stack.pop() != mp[ch]:
                return False
        else:
            stack.append(ch)
    return len(stack) == 0''',

    "max_profit": '''def max_profit(prices):
    low = float("inf")
    ans = 0
    for p in prices:
        ans = max(ans, p - low)       # 今天卖能赚多少
        low = min(low, p)             # 更新历史最低买入价
    return ans''',

    "climb_stairs": '''def climb_stairs(n):
    a, b = 1, 1                       # a=F(0)=1(0阶1种), b=F(1)=1(1阶1种)
    for _ in range(n):
        a, b = b, a + b
    return a''',

    "generate_pascal": '''def generate_pascal(numRows):
    res = []
    for i in range(numRows):
        row = [1] * (i + 1)
        for j in range(1, i):         # 中间项 = 上一行左上 + 正上
            row[j] = res[i - 1][j - 1] + res[i - 1][j]
        res.append(row)
    return res''',

    "single_number": '''def single_number(nums):
    res = 0
    for num in nums:
        res ^= num                    # 异或：相同数抵消为 0，0^x=x
    return res''',

    "majority_element": '''def majority_element(nums):
    cand = count = 0
    for num in nums:
        if count == 0:
            cand = num
        count += 1 if num == cand else -1
    return cand                       # Boyer-Moore 投票法''',
}


# ============================================================
# 每题的「标准测试用例 + 评分逻辑」
# 每个 test_xxx(user) -> (是否全过: bool, 说明: str)
# ============================================================

def _get(name):
    fn = getattr(user, name, None)
    if fn is None:
        raise AttributeError(f"未找到函数 {name}")
    return fn


def test_two_sum(u):
    fn = _get("two_sum")
    cases = [([2, 7, 11, 15], 9), ([3, 2, 4], 6), ([3, 3], 6)]
    bad = []
    for nums, t in cases:
        got = fn(list(nums), t)
        # 不硬编码下标，只校验：「两个不同下标、和为 target」即可
        ok = (isinstance(got, list) and len(got) == 2
              and got[0] != got[1]
              and 0 <= got[0] < len(nums) and 0 <= got[1] < len(nums)
              and nums[got[0]] + nums[got[1]] == t)
        if not ok:
            bad.append(f"  two_sum({nums}, {t}) -> {got}，期望返回两个和为 {t} 的不同下标")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_group_anagrams(u):
    fn = _get("group_anagrams")
    got = fn(["eat", "tea", "tan", "ate", "nat", "bat"])
    exp = [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
    got_sets = sorted([sorted(g) for g in got])
    exp_sets = sorted([sorted(g) for g in exp])
    if got_sets == exp_sets:
        return (True, "✅ 全部用例通过")
    return (False, f"  group_anagrams(...) -> {got}\n  期望（顺序无关）{exp}")


def test_longest_consecutive(u):
    fn = _get("longest_consecutive")
    cases = [([100, 4, 200, 1, 3, 2], 4), ([0, 3, 7, 2, 5, 4, 6, 1], 8)]
    bad = []
    for nums, exp in cases:
        if fn(list(nums)) != exp:
            bad.append(f"  longest_consecutive({nums}) -> {fn(list(nums))}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_move_zeroes(u):
    fn = _get("move_zeroes")
    cases = [([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]), ([0, 0, 1], [1, 0, 0])]
    bad = []
    for nums, exp in cases:
        a = list(nums)
        fn(a)
        if a != exp:
            bad.append(f"  move_zeroes({nums}) -> {a}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_max_area(u):
    fn = _get("max_area")
    cases = [([1, 8, 6, 2, 5, 4, 8, 3, 7], 49), ([1, 1], 1)]
    bad = []
    for h, exp in cases:
        if fn(list(h)) != exp:
            bad.append(f"  max_area({h}) -> {fn(list(h))}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_three_sum(u):
    fn = _get("three_sum")
    got = fn([-1, 0, 1, 2, -1, -4])
    exp = [[-1, -1, 2], [-1, 0, 1]]
    got_sets = sorted([sorted(t) for t in got])
    exp_sets = sorted([sorted(t) for t in exp])
    if got_sets == exp_sets:
        return (True, "✅ 全部用例通过")
    return (False, f"  three_sum([-1,0,1,2,-1,-4]) -> {got}\n  期望（顺序无关）{exp}")


def test_length_of_longest_substring(u):
    fn = _get("length_of_longest_substring")
    cases = [("abcabcbb", 3), ("bbbbb", 1), ("pwwkew", 3)]
    bad = []
    for s, exp in cases:
        if fn(s) != exp:
            bad.append(f"  length_of_longest_substring('{s}') -> {fn(s)}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_find_anagrams(u):
    fn = _get("find_anagrams")
    cases = [("cbaebabacd", "abc", [0, 6]), ("abab", "ab", [0, 1, 2])]
    bad = []
    for s, p, exp in cases:
        if fn(s, p) != exp:
            bad.append(f"  find_anagrams('{s}','{p}') -> {fn(s, p)}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_rotate(u):
    fn = _get("rotate")
    cases = [([1, 2, 3, 4, 5, 6, 7], 3, [5, 6, 7, 1, 2, 3, 4]), ([1, 2], 3, [2, 1])]
    bad = []
    for nums, k, exp in cases:
        a = list(nums)
        fn(a, k)
        if a != exp:
            bad.append(f"  rotate({nums}, {k}) -> {a}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_merge_sorted_array(u):
    fn = _get("merge_sorted_array")
    cases = [([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3, [1, 2, 2, 3, 5, 6]),
             ([1], 1, [], 0, [1])]
    bad = []
    for n1, m, n2, n, exp in cases:
        a = list(n1)
        fn(a, m, list(n2), n)
        if a != exp:
            bad.append(f"  merge_sorted_array({n1},{m},{n2},{n}) -> {a}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_get_intersection_node(u):
    fn = _get("get_intersection_node")
    # A: 1->2->3->4 ; B: 9->3->4（共享 3->4）
    a1 = ListNode(1); a2 = ListNode(2); a3 = ListNode(3); a4 = ListNode(4)
    a1.next = a2; a2.next = a3; a3.next = a4
    b1 = ListNode(9); b1.next = a3
    res = fn(a1, b1)
    if res is a3:
        return (True, "✅ 全部用例通过")
    return (False, f"  get_intersection_node(...) -> 交点值 {getattr(res,'val',None)}，期望 3（且应为同一节点对象）")


def test_reverse_list(u):
    fn = _get("reverse_list")
    got = to_list(fn(build_list([1, 2, 3, 4, 5])))
    if got == [5, 4, 3, 2, 1]:
        return (True, "✅ 全部用例通过")
    return (False, f"  reverse_list([1,2,3,4,5]) -> {got}，期望 [5,4,3,2,1]")


def test_is_palindrome(u):
    fn = _get("is_palindrome")
    cases = [(build_list([1, 2, 2, 1]), True), (build_list([1, 2]), False)]
    bad = []
    for head, exp in cases:
        if fn(head) != exp:
            bad.append(f"  is_palindrome(...) -> {fn(head)}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_has_cycle(u):
    fn = _get("has_cycle")
    # 有环：1->2->3->2
    n1 = ListNode(1); n2 = ListNode(2); n3 = ListNode(3)
    n1.next = n2; n2.next = n3; n3.next = n2
    # 无环：1->2
    m1 = ListNode(1); m2 = ListNode(2); m1.next = m2
    bad = []
    if fn(n1) is not True:
        bad.append("  has_cycle(有环) -> False，期望 True")
    if fn(m1) is not False:
        bad.append("  has_cycle(无环) -> True，期望 False")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_merge_two_lists(u):
    fn = _get("merge_two_lists")
    got = to_list(fn(build_list([1, 2, 4]), build_list([1, 3, 4])))
    if got == [1, 1, 2, 3, 4, 4]:
        return (True, "✅ 全部用例通过")
    return (False, f"  merge_two_lists(...) -> {got}，期望 [1,1,2,3,4,4]")


def test_inorder_traversal(u):
    fn = _get("inorder_traversal")
    got = fn(build_tree([1, None, 2, None, None, 3]))
    if got == [1, 3, 2]:
        return (True, "✅ 全部用例通过")
    return (False, f"  inorder_traversal([1,null,2,null,null,3]) -> {got}，期望 [1,3,2]")


def test_max_depth(u):
    fn = _get("max_depth")
    cases = [(build_tree([3, 9, 20, None, None, 15, 7]), 3), (build_tree([]), 0)]
    bad = []
    for root, exp in cases:
        if fn(root) != exp:
            bad.append(f"  max_depth(...) -> {fn(root)}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_invert_tree(u):
    fn = _get("invert_tree")
    got = to_level(fn(build_tree([2, 1, 3])))
    if got == [2, 3, 1]:
        return (True, "✅ 全部用例通过")
    return (False, f"  invert_tree([2,1,3]) -> 层序 {got}，期望 [2,3,1]")


def test_is_symmetric(u):
    fn = _get("is_symmetric")
    cases = [(build_tree([1, 2, 2, 3, 4, 4, 3]), True),
             (build_tree([1, 2, 2, None, 3, None, 3]), False)]
    bad = []
    for root, exp in cases:
        if fn(root) != exp:
            bad.append(f"  is_symmetric(...) -> {fn(root)}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_diameter_of_binary_tree(u):
    fn = _get("diameter_of_binary_tree")
    got = fn(build_tree([1, 2, 3, 4, 5]))
    if got == 3:
        return (True, "✅ 全部用例通过")
    return (False, f"  diameter_of_binary_tree([1,2,3,4,5]) -> {got}，期望 3")


def test_sorted_array_to_bst(u):
    fn = _get("sorted_array_to_bst")
    root = fn([-10, -3, 0, 5, 9])
    ok = inorder(root) == [-10, -3, 0, 5, 9]  # BST 中序必须升序
    if ok:
        return (True, "✅ 全部用例通过（BST 中序升序校验）")
    return (False, f"  sorted_array_to_bst(...) 中序 = {inorder(root)}，期望 [-10,-3,0,5,9]")


def test_search_insert(u):
    fn = _get("search_insert")
    cases = [([1, 3, 5, 6], 5, 2), ([1, 3, 5, 6], 2, 1), ([1, 3, 5, 6], 7, 4), ([1, 3, 5, 6], 0, 0)]
    bad = []
    for nums, t, exp in cases:
        if fn(list(nums), t) != exp:
            bad.append(f"  search_insert({nums}, {t}) -> {fn(list(nums), t)}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_is_valid(u):
    fn = _get("is_valid")
    cases = [("()[]{}", True), ("([)]", False), ("{[]}", True)]
    bad = []
    for s, exp in cases:
        if fn(s) != exp:
            bad.append(f"  is_valid('{s}') -> {fn(s)}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_max_profit(u):
    fn = _get("max_profit")
    cases = [([7, 1, 5, 3, 6, 4], 5), ([7, 6, 4, 3, 1], 0)]
    bad = []
    for p, exp in cases:
        if fn(list(p)) != exp:
            bad.append(f"  max_profit({p}) -> {fn(list(p))}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_climb_stairs(u):
    fn = _get("climb_stairs")
    cases = [(2, 2), (3, 3), (4, 5)]
    bad = []
    for n, exp in cases:
        if fn(n) != exp:
            bad.append(f"  climb_stairs({n}) -> {fn(n)}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_generate_pascal(u):
    fn = _get("generate_pascal")
    got = fn(5)
    exp = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    if got == exp:
        return (True, "✅ 全部用例通过")
    return (False, f"  generate_pascal(5) -> {got}\n  期望 {exp}")


def test_single_number(u):
    fn = _get("single_number")
    cases = [([2, 2, 1], 1), ([4, 1, 2, 1, 2], 4)]
    bad = []
    for nums, exp in cases:
        if fn(list(nums)) != exp:
            bad.append(f"  single_number({nums}) -> {fn(list(nums))}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


def test_majority_element(u):
    fn = _get("majority_element")
    cases = [([3, 2, 3], 3), ([2, 2, 1, 1, 1, 2, 2], 2)]
    bad = []
    for nums, exp in cases:
        if fn(list(nums)) != exp:
            bad.append(f"  majority_element({nums}) -> {fn(list(nums))}，期望 {exp}")
    return (not bad, "\n".join(bad) or "✅ 全部用例通过")


# 评测清单（顺序即「简单档」刷题顺序）
REGISTRY = [
    ("two_sum", "两数之和", test_two_sum),
    ("group_anagrams", "字母异位词分组", test_group_anagrams),
    ("longest_consecutive", "最长连续序列", test_longest_consecutive),
    ("move_zeroes", "移动零", test_move_zeroes),
    ("max_area", "盛最多水的容器", test_max_area),
    ("three_sum", "三数之和", test_three_sum),
    ("length_of_longest_substring", "无重复字符的最长子串", test_length_of_longest_substring),
    ("find_anagrams", "找到字符串中所有字母异位词", test_find_anagrams),
    ("rotate", "轮转数组", test_rotate),
    ("merge_sorted_array", "合并两个有序数组", test_merge_sorted_array),
    ("get_intersection_node", "相交链表", test_get_intersection_node),
    ("reverse_list", "反转链表", test_reverse_list),
    ("is_palindrome", "回文链表", test_is_palindrome),
    ("has_cycle", "环形链表", test_has_cycle),
    ("merge_two_lists", "合并两个有序链表", test_merge_two_lists),
    ("inorder_traversal", "二叉树的中序遍历", test_inorder_traversal),
    ("max_depth", "二叉树的最大深度", test_max_depth),
    ("invert_tree", "翻转二叉树", test_invert_tree),
    ("is_symmetric", "对称二叉树", test_is_symmetric),
    ("diameter_of_binary_tree", "二叉树的直径", test_diameter_of_binary_tree),
    ("sorted_array_to_bst", "有序数组转二叉搜索树", test_sorted_array_to_bst),
    ("search_insert", "搜索插入位置", test_search_insert),
    ("is_valid", "有效的括号", test_is_valid),
    ("max_profit", "买卖股票的最佳时机", test_max_profit),
    ("climb_stairs", "爬楼梯", test_climb_stairs),
    ("generate_pascal", "杨辉三角", test_generate_pascal),
    ("single_number", "只出现一次的数字", test_single_number),
    ("majority_element", "多数元素", test_majority_element),
]


# ============================================================
# 主流程：逐题评分并打印报告
# ============================================================
def main():
    print("=" * 64)
    print("Hot100 自测批改结果（简单档 / Day01–03 题目）")
    print("=" * 64)

    passed = 0
    total = len(REGISTRY)
    wrong = []

    for name, cn, tester in REGISTRY:
        print(f"\n【{cn}】{name}")
        try:
            ok, detail = tester(user)
        except AttributeError as e:
            print("  ❌ 未实现：" + str(e))
            wrong.append(name)
            continue
        except Exception as e:
            print(f"  ❌ 运行你的函数时抛异常：{type(e).__name__}: {e}")
            wrong.append(name)
            continue

        if ok:
            print("  " + detail)
            passed += 1
        else:
            print("  ❌ 未通过：")
            print("  " + detail.replace("\n", "\n  "))
            print("  —— 参考答案 ——")
            for line in CANONICAL.get(name, "# (暂无参考答案)").splitlines():
                print("    " + line)
            wrong.append(name)

    print("\n" + "=" * 64)
    print(f"总分：{passed}/{total} 题通过")
    if wrong:
        print(f"待加强（{len(wrong)} 题）：{', '.join(wrong)}")
        print("👉 把上面 ❌ 的题对应的「参考答案」盖住，自己再默一遍，直到能一次写对。")
    else:
        print("🎉 全部通过！简单档已吃透，可以进 Day04 中等档了。")
    print("=" * 64)


if __name__ == "__main__":
    main()
