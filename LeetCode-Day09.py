"""
LeetCode 必刷100题 · Day 09（2026-07-22）
========================================
面试方向：AI 应用 / Agent 开发
今日题目：
  - 第 17 题：字母异位词分组               LeetCode 49    中等   频率 ⭐⭐⭐⭐⭐
  - 第 18 题：最长无重复子串               LeetCode 3     中等   频率 ⭐⭐⭐⭐⭐

运行方式：
    python LeetCode-Day09.py
会自动执行所有测试用例并打印 PASS / FAIL。

每个题目都包含：① 思路讲解 ② 流程示意图（ASCII）③ 可运行代码 ④ 复杂度分析 ⑤ 面试易错点。
只给一种「通用解法」，方便记忆和手撕。

今日主题：第 17 题是「哈希表 + 签名」的代表——把同类字符串用同一个 key 归到一组，
这招在面试里会反复出现（比如分组、去重、按特征聚合）。
第 18 题是「滑动窗口」的入门镇山题——双指针维持一个合法窗口，遇到冲突就收缩左边界，
是所有子串/子数组最值问题的通用模板。
"""

# ============================================================
# 第 17 题：字母异位词分组（LeetCode 49）
# ============================================================
"""
题目描述
--------
给你一个字符串数组 strs，请你将「字母异位词」组合在一起，返回一个分组后的列表
（组内顺序、组间顺序不限）。
「字母异位词」= 字符组成和个数完全相同、只是排列顺序不同的字符串。

输入：strs = ["eat","tea","tan","ate","nat","bat"]
输出：[["eat","tea","ate"],["tan","nat"],["bat"]]
（"eat"/"tea"/"ate" 互为异位词归一组；"tan"/"nat" 一组；"bat" 单独一组）

输入：strs = [""]              → [[""]]
输入：strs = ["a"]             → [["a"]]

朴素想法（暴力两两比较）：
  对每两个字符串，统计各自字符计数，看是否完全相同，相同就放一组。
  时间 O(n² · k)（n 个串、串长 k），太慢，面试不可接受。

通用解法（哈希表 + 排序签名）
-----------------------------------
核心思想：当且仅当两个字符串是「字母异位词」时，它们「按字典序排序后」得到完全一样的字符串。
  - 给每个字符串算一个「签名」：sorted(s) 排好序后拼成的字符串，如 "eat" → 排序 → "aet"。
  - 用字典 groups：键 = 签名，值 = 该签名下所有原串组成的列表。
  - 遍历 strs，每串算签名，append 进对应组；最后把字典的所有值收集成列表返回。

为什么「排序后」能当唯一签名？
  异位词只是字母顺序不同，排序后字母顺序被唯一确定 → 必然相等；
  非异位词字符构成不同 → 排序后一定不等。所以「排序串」是同一异位词组的完美唯一 key。

备选签名法（字符计数元组，O(k) 不排序，更高效但写法略长）：
  key = tuple(sorted) 换成 key = tuple(字符计数数组)，例如 "eat" → (1,0,0,...,1,0,..,1..)
  本质一样，面试用「排序签名」最直观、最不容易写错，这里主解法用排序签名。

流程示意（strs = ["eat","tea","tan","ate","nat","bat"]）
--------------------------------------------------------------------------------
groups = {}（空字典）

s="eat"  → 排序 "aet" → groups["aet"] = ["eat"]
s="tea"  → 排序 "aet" → groups["aet"] = ["eat","tea"]
s="tan"  → 排序 "ant" → groups["ant"] = ["tan"]
s="ate"  → 排序 "aet" → groups["aet"] = ["eat","tea","ate"]
s="nat"  → 排序 "ant" → groups["ant"] = ["tan","nat"]
s="bat"  → 排序 "abt" → groups["abt"] = ["bat"]

最终 values： [["eat","tea","ate"], ["tan","nat"], ["bat"]]  ✓

复杂度：
  时间 O(n · k log k)：n 个串，每个串排序耗时 k log k（k 为串长）
  空间 O(n · k)：字典存储所有串（最坏情况每组一个）
面试易错点：
  - 签名用 sorted(s) 得到的是「列表」，字典的 key 必须是「不可变」类型，
    所以要 "".join(sorted(s)) 变成字符串，或 tuple(sorted(s))，不能直接用 list 当 key。
  - 返回的是「字典的所有值」：list(groups.values())，别返回 keys。
  - 组间/组内顺序不限，不用刻意排序，面试时说明即可。
  - 空串 "" 排序后还是 ""，会自己归到 "" 组，逻辑天然正确，无需特判。
  - 若题目字符含 Unicode，sorted 同样适用（按码点排序），比计数数组更通用。
"""


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """把字母异位词分组。哈希表 + 排序签名，O(n·klogk)。"""
    groups: dict[str, list[str]] = {}

    for s in strs:
        # 排序后的串作为「签名」key；sorted 返回列表，join 成字符串才能当字典 key
        key = "".join(sorted(s))
        if key not in groups:
            groups[key] = []
        groups[key].append(s)

    # 返回所有分组（顺序不限）
    return list(groups.values())

# ============================================================
# 第 18 题：最长无重复子串（LeetCode 3）
# ============================================================
"""
题目描述
--------
给定一个字符串 s，请你找出其中「不含有重复字符」的「最长子串」的长度。
（子串 = 连续的字符序列；只要求长度，不要求返回子串本身）

输入：s = "abcabcbb"  → 3   （最长无重复子串是 "abc"，长度 3）
输入：s = "bbbbb"    → 1   （"b"）
输入：s = "pwwkew"   → 3   （"wke" 或 "kew"，注意 "pwke" 是子序列不是子串）
输入：s = ""         → 0
输入：s = "au"       → 2

朴素想法（暴力枚举所有子串）：
  枚举所有起点 i、终点 j，检查 [i,j] 内是否无重复。时间 O(n³) 或 O(n²)，必超时。

通用解法（滑动窗口 + 哈希集合）
-----------------------------------
核心思想：用「左指针 left、右指针 right」维护一个 [left, right] 窗口，
窗口内的字符「保证都不重复」。右指针一路向右扩，遇到重复就移动左指针收缩，
全程窗口始终合法，最大窗口长度即答案。

具体步骤：
  1. 用集合 window 记录「当前窗口里有哪些字符」。
  2. right 从 0 向右遍历每个字符 c：
     - 若 c 已经在 window 里（重复了），说明当前窗口不能再容纳 c，
       于是不断把 strs[left] 从 window 移除，并 left += 1，
       直到把那个重复的 c 移出去（窗口恢复「无重复」状态）。
     - 把 c 加入 window，更新答案 ans = max(ans, right - left + 1)。
  3. 返回 ans。

为什么 left 只会向右、不会回退？
  因为一旦 left 越过某个位置，那个位置左边的字符已经永远不在窗口里了，
  再遇到它们也不会构成重复（重复只可能来自窗口内部），所以 left 单调右移，
  整体每个字符最多进出窗口一次 → 总 O(n)。

流程示意（s = "abcabcbb"，用 [ ] 表示当前窗口）
--------------------------------------------------------------------------------
window={}  left=0  ans=0
right=0 'a'：不在 → 加入；window={a}；ans=max(0,1)=1
right=1 'b'：不在 → 加入；window={a,b}；ans=max(1,2)=2
right=2 'c'：不在 → 加入；window={a,b,c}；ans=max(2,3)=3
right=3 'a'：'a' 已在 window！收缩 left：
   移除 s[0]='a'，left=1，window={b,c}；'a' 已不在 → 停
   加入 'a'，window={b,c,a}；ans=max(3,3-1+1=3)=3
right=4 'b'：'b' 已在！收缩 left：
   移除 s[1]='b'，left=2，window={c,a}；'b' 不在 → 停
   加入 'b'，window={c,a,b}；ans=max(3,4-2+1=3)=3
right=5 'c'：'c' 已在！收缩 left：
   移除 s[2]='c'，left=3，window={a,b}；'c' 不在 → 停
   加入 'c'，window={a,b,c}；ans=max(3,5-3+1=3)=3
right=6 'b'：'b' 已在！收缩 left：
   移除 s[3]='a'，left=4，window={b,c}；'b' 还在
   移除 s[4]='b'，left=5，window={c}；'b' 不在 → 停
   加入 'b'，window={c,b}；ans=max(3,6-5+1=2)=3
right=7 'b'：'b' 已在！收缩 left：
   移除 s[5]='c'，left=6，window={b}；'b' 还在
   移除 s[6]='b'，left=7，window={}；'b' 不在 → 停
   加入 'b'，window={b}；ans=max(3,7-7+1=1)=3
结束 → ans = 3  ✓ （最长无重复子串 "abc"）

复杂度：
  时间 O(n)（每个字符最多被 right 加一次、被 left 删一次）
  空间 O(min(n, 字符集大小))（window 集合大小，最坏为全部不同字符）
面试易错点：
  - 收缩窗口的 while 条件：while c in window: 把 left 指向的字符移出去，
    直到重复字符被移除。别只移一次（可能窗口里还藏着另一个重复）。
  - 答案更新用 right - left + 1（闭区间长度），不是 right - left。
  - 空串直接返回 0，循环不进，ans 初值 0 即正确。
  - left 移动和 right 移动是「同一层」的：先确保窗口无重复，再加新字符、更新答案。
  - 进阶写法（O(1) 收缩、无内层 while）：用 dict last_seen 记字符上次出现下标，
    left = max(left, last_seen[c] + 1)，一行搞定收缩，面试熟练后可展示。
"""


def length_of_longest_substring(s: str) -> int:
    """返回最长无重复字符子串的长度。滑动窗口 + 哈希集合，O(n)。"""
    # set可以无序 不重复的集合
    window: set[str] = set()   # 当前窗口内的字符
    left = 0                   # 窗口左边界
    ans = 0                    # 记录最大窗口长度

    for right, c in enumerate(s):
        # 当前字符已存在于窗口 → 收缩左边界，直到把它移出去
        while c in window:
            # 删除指定元素
            window.discard(s[left])
            left += 1
        # 现在窗口已无重复，加入新字符
        window.add(c)
        # 更新最大长度（闭区间 [left, right] 长度 = right - left + 1）
        ans = max(ans, right - left + 1)

    return ans

# ============================================================
# 测试用例：直接运行本文件即可验证
# ============================================================
def _run_tests() -> None:
    print("=" * 62)
    print("第 17 题：字母异位词分组（LeetCode 49）")
    print("=" * 62)

    # 用例1：标准多组
    out1 = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    # 把每组排序、整体排序后再比较，避免顺序差异导致误判
    norm1 = sorted(sorted(g) for g in out1)
    expect1 = sorted(sorted(g) for g in [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]])
    ok1 = norm1 == expect1
    print(f"  ['eat','tea','tan','ate','nat','bat'] -> {out1}")
    print(f"    期望 3 组(顺序不限)  [{'PASS' if ok1 else 'FAIL'}]")
    assert ok1, "用例1失败"

    # 用例2：单元素
    out2 = group_anagrams(["a"])
    ok2 = sorted(sorted(g) for g in out2) == [["a"]]
    print(f"  ['a'] -> {out2}  期望 [['a']]  [{'PASS' if ok2 else 'FAIL'}]")
    assert ok2, "用例2失败"

    # 用例3：空串
    out3 = group_anagrams([""])
    ok3 = sorted(sorted(g) for g in out3) == [[""]]
    print(f"  [''] -> {out3}  期望 [['']]  [{'PASS' if ok3 else 'FAIL'}]")
    assert ok3, "用例3失败"

    # 用例4：全部互为异位词
    out4 = group_anagrams(["abc", "bca", "cab"])
    ok4 = len(out4) == 1 and sorted(out4[0]) == ["abc", "bca", "cab"]
    print(f"  ['abc','bca','cab'] -> {out4}  期望归为 1 组  [{'PASS' if ok4 else 'FAIL'}]")
    assert ok4, "用例4失败"

    # 用例5：无异位词（每个都不同组）
    out5 = group_anagrams(["a", "b", "c"])
    ok5 = len(out5) == 3
    print(f"  ['a','b','c'] -> {out5}  期望 3 组  [{'PASS' if ok5 else 'FAIL'}]")
    assert ok5, "用例5失败"

    print()
    print("=" * 62)
    print("第 18 题：最长无重复子串（LeetCode 3）")
    print("=" * 62)

    # 用例1：标准
    r1 = length_of_longest_substring("abcabcbb")
    ok_r1 = r1 == 3
    print(f"  'abcabcbb' -> {r1}  期望 3  [{'PASS' if ok_r1 else 'FAIL'}]")
    assert ok_r1, "用例1失败"

    # 用例2：全相同
    r2 = length_of_longest_substring("bbbbb")
    ok_r2 = r2 == 1
    print(f"  'bbbbb'    -> {r2}  期望 1  [{'PASS' if ok_r2 else 'FAIL'}]")
    assert ok_r2, "用例2失败"

    # 用例3：中间最长
    r3 = length_of_longest_substring("pwwkew")
    ok_r3 = r3 == 3
    print(f"  'pwwkew'   -> {r3}  期望 3  [{'PASS' if ok_r3 else 'FAIL'}]")
    assert ok_r3, "用例3失败"

    # 用例4：空串
    r4 = length_of_longest_substring("")
    ok_r4 = r4 == 0
    print(f"  ''         -> {r4}  期望 0  [{'PASS' if ok_r4 else 'FAIL'}]")
    assert ok_r4, "用例4失败"

    # 用例5：双字符
    r5 = length_of_longest_substring("au")
    ok_r5 = r5 == 2
    print(f"  'au'       -> {r5}  期望 2  [{'PASS' if ok_r5 else 'FAIL'}]")
    assert ok_r5, "用例5失败"

    # 用例6：含大写混合
    r6 = length_of_longest_substring("abacada")
    ok_r6 = r6 == 3
    print(f"  'abacada'  -> {r6}  期望 3  [{'PASS' if ok_r6 else 'FAIL'}]")
    assert ok_r6, "用例6失败"

    print("\n✅ 全部测试用例通过！")


if __name__ == "__main__":
    _run_tests()
