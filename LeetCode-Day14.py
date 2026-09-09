"""
LeetCode 必刷100题 · Day 14（2026-07-31）
========================================
面试方向：AI 应用 / Agent 开发
今日题目（共 10 道，对应必刷表 #60–#69）：
  - 第 60 题：验证二叉搜索树              LeetCode 98    中等   频率 ⭐⭐⭐⭐⭐  （递归 + 值区间）
  - 第 61 题：二叉树的所有路径            LeetCode 257   简单   频率 ⭐⭐⭐⭐    （DFS + 回溯）
  - 第 62 题：二叉搜索树中的搜索          LeetCode 700   简单   频率 ⭐⭐⭐⭐    （利用 BST 性质）
  - 第 63 题：删除二叉搜索树中的节点      LeetCode 450   中等   频率 ⭐⭐⭐⭐⭐  （BST 删除三情况）
  - 第 64 题：二叉树展开为链表            LeetCode 114   中等   频率 ⭐⭐⭐⭐    （递归 + 拼接尾节点）
  - 第 65 题：从前序与中序遍历构造二叉树   LeetCode 105   中等   频率 ⭐⭐⭐⭐⭐  （递归分治）
  - 第 66 题：爬楼梯                      LeetCode 70    简单   频率 ⭐⭐⭐⭐⭐  （动态规划入门）
  - 第 67 题：斐波那契数                  LeetCode 509   简单   频率 ⭐⭐⭐⭐    （动态规划）
  - 第 68 题：不同路径                    LeetCode 62    中等   频率 ⭐⭐⭐⭐⭐  （二维 DP）
  - 第 69 题：不同路径 II                 LeetCode 63    中等   频率 ⭐⭐⭐⭐⭐  （带障碍 DP）

运行方式：
    python LeetCode-Day14.py
会自动执行所有测试用例并打印 PASS / FAIL，全部通过即说明代码正确。

每个题目都包含：① 思路讲解 ② 流程示意图（ASCII）③ 可运行代码 ④ 复杂度分析 ⑤ 面试易错点。
只给一种「通用解法」，方便记忆和手撕。

今日主题：把「树与递归」篇章收尾（#60–#65），并开启「动态规划」篇章（#66–#69）。
- #60 验证 BST：递归下传「允许的值域区间」，是 BST 系列题的基石。
- #61 所有路径：DFS + 回溯的雏形，几乎所有「枚举所有路径」题都用这套。
- #62 搜索 BST：BST 性质的最直白应用，O(h) 一次走到底。
- #63 删除节点：BST 最难的一题，记住「右子树最小节点（中序后继）顶替」即可。
- #64 展开为链表：递归先展开左右、再把左子树拼到右边，体会「返回尾节点」的技巧。
- #65 前序+中序建树：分治 + 哈希表定位根，构造类题的模板。
- #66–#69：DP 四连，从「滚动变量」「二维表」到「带障碍」，建立状态转移直觉。
"""

from collections import deque


# ============================================================
# 通用工具：TreeNode 定义 + 建树 / 序列化的辅助函数（沿用 Day 12/13）
# ============================================================
class TreeNode:
    def __init__(self, val: int = 0, left: "TreeNode | None" = None,
                 right: "TreeNode | None" = None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(vals) -> "TreeNode | None":
    """把 LeetCode 风格的层序数组（用 None 表示空节点）建成树。"""
    if not vals:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


def to_level(root: "TreeNode | None") -> list:
    """把树序列化回 LeetCode 风格的层序数组（尾部多余的 None 会被裁掉）。"""
    if not root:
        return []
    res = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node:
            res.append(node.val)
            q.append(node.left)
            q.append(node.right)
        else:
            res.append(None)
    while res and res[-1] is None:   # 裁掉尾部无用的 None
        res.pop()
    return res


def find_node(root: "TreeNode | None", val: int) -> "TreeNode | None":
    """按值找节点（测试里给需要『节点引用』的题准备用）。"""
    if not root:
        return None
    if root.val == val:
        return root
    return find_node(root.left, val) or find_node(root.right, val)


def to_list(root: "TreeNode | None") -> list[int]:
    """沿 right 指针把『展开后的链表』走一遍（专门给 #64 序列化用）。"""
    res = []
    while root:
        res.append(root.val)
        root = root.right
    return res


# ============================================================
# 第 60 题：验证二叉搜索树（LeetCode 98）
# ============================================================
r"""
题目描述
--------
给定一个二叉树，判断它是否是一个「有效的二叉搜索树（BST）」。
BST 定义：节点的左子树所有值 < 节点值 < 右子树所有值（严格小于/大于，不能相等）。

输入：[2,1,3]                 输出：True
输入：[5,1,4,None,None,3,6]   输出：False
       树：      5                4 在 5 的右子树里，但 4 < 5，违反 BST
              /   \
             1     4
                  / \
                 3   6

通用解法（递归下传「允许的值域区间」）
---------------------------------------------------
只比较「当前节点和左右孩子」是错的！例如 [5,1,4,None,None,3,6] 里，4 比 5 小、比父节点
没问题，但 4 的左孩子 3 比根 5 还小，就违规了。所以必须检查「整棵子树」都在某个范围里。

做法：从根开始，允许的值域是 (-∞, +∞)。
每下一层，把「上界/下界」收窄：
  - 进入左子树：上界收紧为「当前节点值」（左子树必须都 < 它），下界不变
  - 进入右子树：下界收紧为「当前节点值」（右子树必须都 > 它），上界不变
  - 若某节点值不落在区间内（low < val < high 不成立）→ 不是 BST

    dfs(node, low, high):
        if node 为空: return True          # 空树是 BST
        if not (low < node.val < high): return False
        return dfs(node.left, low, node.val) and dfs(node.right, node.val, high)

起始调用：dfs(root, -∞, +∞)

流程示意（[5,1,4,None,None,3,6]，区间随递归收窄）
--------------------------------------------------------------------------------
  dfs(5, -∞, +∞)          5 ∈ (-∞,+∞) ✓
   ├─ dfs(1, -∞, 5)       1 ∈ (-∞,5) ✓
   │    ├─ dfs(None,...) → True
   │    └─ dfs(None,...) → True
   └─ dfs(4, 5, +∞)       4 ∈ (5,+∞)? ✗ 4 不大于 5 → 直接 False！
  → 整棵不是 BST

复杂度
------
时间 O(n)：每个节点访问一次。
空间 O(h)：递归栈深度 = 树高（最坏 O(n)，平衡树 O(log n)）。

面试易错点
---------
1. 最经典错误：只判断 root.left.val < root.val < root.right.val。右子树里更小的数
   会被漏掉（本题示例正是这个坑）。必须下传「整段区间」。
2. 用 float('-inf') / float('inf') 表示无界；不要初始化成某个具体数（如 -1），
   否则根节点值恰为 -1 时会误判。
3. BST 不允许相等（左 < 根 < 右）。遇到 [2,2,2] 这种重复值，区间里用严格小于/大于，
   直接返回 False。
"""


def is_valid_bst(root: "TreeNode | None") -> bool:
    def dfs(node: "TreeNode | None", low: float, high: float) -> bool:
        if not node:
            return True
        if not (low < node.val < high):     # 不落在区间内就违规
            return False
        # 左子树上界收紧为 node.val；右子树下界收紧为 node.val
        return dfs(node.left, low, node.val) and dfs(node.right, node.val, high)

    return dfs(root, float("-inf"), float("inf"))


# ============================================================
# 第 61 题：二叉树的所有路径（LeetCode 257）
# ============================================================
r"""
题目描述
--------
给你一个二叉树的根节点，返回「所有从根节点到叶子节点」的路径，路径用 "->" 连接成字符串。

输入：[1,2,3,None,5]   输出：["1->2->5","1->3"]
       树：      1
              /   \
             2     3
              \
               5
输入：[1]               输出：["1"]
输入：[1,2,None,3]      输出：["1->2->3"]

通用解法（DFS + 回溯）
---------------------------------------------------
用一个列表 path 记录「当前已经走过的节点值」。从根往下走：
  - 把当前节点值加入 path
  - 如果到了叶子（无左右孩子）→ 把 path 用 "->" 连成字符串，加入答案
  - 否则 → 递归走左、递归走右
  - 回溯：从 path 弹出刚加的节点值（让兄弟分支用干净的 path）

    dfs(node, path):
        path.append(node.val)
        if 叶子: res.append("->".join(map(str, path)))
        else:
            if node.left:  dfs(node.left, path)
            if node.right: dfs(node.right, path)
        path.pop()     # 回溯

流程示意（[1,2,3,None,5]，path 的变化）
--------------------------------------------------------------------------------
  dfs(1): path=[1]
    dfs(2): path=[1,2]
      dfs(5): path=[1,2,5] → 5 是叶子 → 加入 "1->2->5"
              path.pop() → [1,2]
      path.pop() → [1]
    dfs(3): path=[1,3] → 3 是叶子 → 加入 "1->3"
            path.pop() → [1]
  结果：["1->2->5","1->3"]

复杂度
------
时间 O(n)：每个节点访问一次；字符串拼接最坏 O(n)，整体 O(n^2) 量级但面试够用。
空间 O(h)：递归栈 + path 长度（h 为树高）。

面试易错点
---------
1. 必须「到叶子」才算一条路径，不能半路就收。判叶子用 `not left and not right`。
2. 回溯 path.pop() 不能漏——否则走到右分支时 path 里还残留左分支的节点。
3. 拼接用 `"->".join(...)`，别手动画字符串（易在末尾多一个 "->"）。
"""


def binary_tree_paths(root: "TreeNode | None") -> list[str]:
    res: list[str] = []

    def dfs(node: "TreeNode | None", path: list[int]) -> None:
        if not node:
            return
        path.append(node.val)
        if not node.left and not node.right:        # 叶子：收一条路径
            res.append("->".join(map(str, path)))
        else:
            if node.left:
                dfs(node.left, path)
            if node.right:
                dfs(node.right, path)
        path.pop()                                  # 回溯

    dfs(root, [])
    return res


# ============================================================
# 第 62 题：二叉搜索树中的搜索（LeetCode 700）
# ============================================================
r"""
题目描述
--------
给定二叉搜索树（BST）的根节点和一个值 val，在 BST 中查找值为 val 的节点，
返回以该节点为根的子树；若不存在返回 None。

输入：树 [4,2,7,1,3]，val = 2   输出：子树 [2,1,3]（即值为 2 的节点及其左右孩子）
输入：同上，val = 5             输出：None

通用解法（利用 BST 性质，一路比大小往下走）
---------------------------------------------------
BST 的核心性质：左子树都小、右子树都大。所以：
  - 当前节点值 == val → 找到了，返回它
  - val 比当前节点小 → 往左子树找
  - val 比当前节点大 → 往右子树找
比完后还没找到（走到空）→ 返回 None。

    search(node, val):
        if node 为空: return None
        if node.val == val: return node
        if val < node.val: return search(node.left, val)
        else:              return search(node.right, val)

（也可以写成 while 循环迭代版，面试能写递归就写递归，更简洁。）

流程示意（[4,2,7,1,3]，查找 val=2）
--------------------------------------------------------------------------------
  node=4: 2 < 4 → 往左
  node=2: 2 == 2 → 命中，返回节点 2（子树为 [2,1,3]）✓

  （查找 val=5）
  node=4: 5>4 → 往右
  node=7: 5<7 → 往左
  node=None → 返回 None

复杂度
------
时间 O(h)：h 为树高，平衡 BST 为 O(log n)，退化为链 O(n)。
空间 O(h)：递归栈（迭代版为 O(1)）。

面试易错点
---------
1. 这题能一路比大小是因为「BST」；普通二叉树（#56/LCA 那类）不能这么走。
2. 找到了就「返回该节点（子树根）」，不是返回 True/False，看清题目要求。
3. 找不到时返回 None，别返回空列表或报错，LeetCode 上就是返回 None。
"""


def search_bst(root: "TreeNode | None", val: int) -> "TreeNode | None":
    if not root:
        return None
    if root.val == val:
        return root
    if val < root.val:
        return search_bst(root.left, val)
    return search_bst(root.right, val)


# ============================================================
# 第 63 题：删除二叉搜索树中的节点（LeetCode 450）
# ============================================================
r"""
题目描述
--------
给定一个 BST 的根节点和一个 key，删除 BST 中值为 key 的节点，并保持它依然是 BST，
返回删除后树的（新）根节点。

输入：[5,3,6,2,4,None,None,1]，key = 3   输出：[5,4,6,2,None,None,None,1]
       原树：       删除 3 后（用右子树最小节点 4 顶替）：
          5             5
        /   \         /   \
       3     6       4     6
      / \           /
     2   4         2
    /              /
   1              1

通用解法（BST 删除三类情况，递归）
---------------------------------------------------
先按 BST 性质递归找到要删的节点，再根据它的孩子情况处理：

  情况 1：叶子节点（无孩子）→ 直接删（返回 None 给父节点）
  情况 2：只有一个孩子 → 用那个孩子顶替自己（返回孩子）
  情况 3：有两个孩子 → 找「右子树里最小的节点」（中序后继 successor）：
            · 它一定没有左孩子（否则它不是最小的）
            · 用它的值覆盖当前节点
            · 再递归去右子树里把那个 successor 删掉

    delete(node, key):
        if node 为空: return None                 # 没找到
        if key < node.val: node.left  = delete(node.left, key)
        elif key > node.val: node.right = delete(node.right, key)
        else:                                       # 找到要删的 node
            if not node.left:  return node.right    # 情况1/2：左空
            if not node.right: return node.left     # 情况2：右空
            succ = node.right                        # 情况3：找右子树最小
            while succ.left: succ = succ.left
            node.val = succ.val                      # 用 successor 值覆盖
            node.right = delete(node.right, succ.val)  # 删掉 successor
        return node

流程示意（删除 key=3，右子树最小 = 4）
--------------------------------------------------------------------------------
  找到节点 3（左右都有孩子）
    → succ = 右子树最小 = 4
    → 把 3 的值改成 4
    → 递归去右子树删除 4（4 是叶子，情况1，返回 None）
    → 4 原本的右指针（None）接回 → 结构变成 [5,4,6,2,None,None,None,1]

复杂度
------
时间 O(h)：每次递归走一条路径，平衡树 O(log n)。
空间 O(h)：递归栈。

面试易错点
---------
1. 情况 3 用「右子树最小（中序后继）」或「左子树最大（前驱）」都行，二选一记住即可。
   本题用右子树最小最直观。
2. 覆盖值之后，一定要「再去右子树删掉那个 successor」，否则 4 会重复出现。
3. successor 一定没有左孩子，所以删它时最多走情况 1/2，不会无限递归。
4. 别忘了处理「根就是要删的节点」这种情况（递归会自动处理，因为根也走同一套逻辑）。
"""


def delete_node(root: "TreeNode | None", key: int) -> "TreeNode | None":
    if not root:
        return None
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        # 找到要删除的节点 root
        if not root.left:
            return root.right          # 情况1/2：左空，右孩子（或 None）顶上
        if not root.right:
            return root.left           # 情况2：右空，左孩子顶上
        # 情况3：左右都有 → 找右子树最小节点（中序后继）
        succ = root.right
        while succ.left:
            succ = succ.left
        root.val = succ.val            # 用 successor 的值覆盖
        root.right = delete_node(root.right, succ.val)  # 删掉 successor
    return root


# ============================================================
# 第 64 题：二叉树展开为链表（LeetCode 114）
# ============================================================
r"""
题目描述
--------
给你二叉树的根节点，将它「原地」展开成一个单链表：
  - 链表同样用 TreeNode 的 right 指针串联，left 指针全部置为 None
  - 链表顺序为「先序遍历」（根 → 左 → 右）的顺序

输入：[1,2,5,3,4,None,6]   输出：[1,2,3,4,5,6]（全部沿 right 指针）
       原树：        展开后（left 全空，right 串联）：
          1             1
         / \             \
        2   5             2
       / \   \              \
      3   4   6             3
                             \
                              4
                               \
                                5
                                 \
                                  6

通用解法（递归展开左右，再把左子树拼到右边）
---------------------------------------------------
对当前节点，先递归把「左子树」和「右子树」各自展开好，拿到它们各自的「尾节点」。
然后：如果有左子树，就把整段左子树插到「当前节点」和「原右子树」之间。

    dfs(node):   # 返回以 node 为根展开后「最右的节点」（链表尾）
        if node 为空: return None
        left_tail  = dfs(node.left)    # 左子树展开后的尾
        right_tail = dfs(node.right)   # 右子树展开后的尾
        if node.left:                   # 有左子树才需要拼接
            left_tail.right = node.right   # 左子树尾 → 接原右子树
            node.right = node.left         # 当前节点右 → 原左子树
            node.left  = None              # 左指针清空
        # 整棵子树的尾：优先右子树尾，否则左子树尾，否则自己
        return right_tail or left_tail or node

流程示意（[1,2,5,3,4,None,6]）
--------------------------------------------------------------------------------
  dfs(2): 展开后变成 2->3->4，返回 tail=4
  dfs(5): 展开后变成 5->6，返回 tail=6
  dfs(1):
    有左子树 2。把 2->3->4 的尾(4) 接到原右(5) 前面：4->5->6
    1.right = 2（原左），1.left = None
    → 1->2->3->4->5->6，返回 tail=6
  结果链表：[1,2,3,4,5,6] ✓

复杂度
------
时间 O(n)：每个节点访问一次。
空间 O(h)：递归栈。

面试易错点
---------
1. 顺序必须是「先序」（根左右）。很多解法会写成「后序拼接」(右→左→接)，本质是同一件事，
   但本题用「先展开后拼接 + 返回尾节点」最直观，好讲。
2. 拼接后务必 `node.left = None`，否则链表里有 left 指针会判错。
3. 找「尾节点」是为了把原右子树正确接上去；漏了这步右子树就丢了。
"""


def flatten(root: "TreeNode | None") -> None:
    def dfs(node: "TreeNode | None") -> "TreeNode | None":
        if not node:
            return None
        left_tail = dfs(node.left)     # 左子树展开后的尾
        right_tail = dfs(node.right)   # 右子树展开后的尾
        if node.left:                  # 有左子树才拼接
            left_tail.right = node.right   # 左子树尾 → 接原右子树
            node.right = node.left         # 当前右 → 原左子树
            node.left = None               # 左指针清空
        # 整棵子树的尾：优先右尾，否则左尾，否则自己
        return right_tail or left_tail or node

    dfs(root)


# ============================================================
# 第 65 题：从前序与中序遍历序列构造二叉树（LeetCode 105）
# ============================================================
r"""
题目描述
--------
给定一棵二叉树的前序遍历 preorder 和中序遍历 inorder，请构造并返回这棵树。
（题目保证没有重复值）

输入：preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]   输出：[3,9,20,None,None,15,7]
       树：      3
              /   \
             9    20
                 /  \
                15   7

通用解法（递归分治 + 哈希表定位根）
---------------------------------------------------
关键事实：
  - 前序的第 1 个 = 当前子树的根
  - 在「中序」里找到根的位置 i → 根的左边是左子树、右边是右子树
  - 左子树节点数 = i - in_start
  - 前序里：根后面紧挨着的 left_size 个 = 左子树的前序；再后面 = 右子树的前序

    build(pre_start, pre_end, in_start, in_end):
        if pre_start > pre_end: return None
        root_val = preorder[pre_start]
        i = idx_map[root_val]              # 根在中序的位置
        left_size = i - in_start
        root = TreeNode(root_val)
        root.left  = build(pre_start+1, pre_start+left_size, in_start, i-1)
        root.right = build(pre_start+left_size+1, pre_end, i+1, in_end)
        return root

用 idx_map（值→中序下标）把「找根位置」从 O(n) 降到 O(1)，整体 O(n)。

流程示意（pre=[3,9,20,15,7]，in=[9,3,15,20,7]）
--------------------------------------------------------------------------------
  root=3（pre[0]），在中序 i=1
    left_size = 1-0 = 1 → 左子树 1 个节点(9)，右子树 [15,20,7]
    左：build(pre[1..1], in[0..0]) → 9（叶子）
    右：build(pre[2..4], in[2..4]) → 根 20（in i=3）
          left_size=3-2=1 → 左 15（叶子），右 7（叶子）
  拼好：3(左9, 右20(左15,右7)) → [3,9,20,None,None,15,7] ✓

复杂度
------
时间 O(n)：每个节点当一次根，哈希表定位 O(1)。
空间 O(n)：哈希表 O(n) + 递归栈 O(h)。

面试易错点
---------
1. 必须用哈希表存「值→中序下标」，否则每次线性查找根是 O(n^2)，大数据会超时。
2. 左子树大小 = i - in_start，不是固定一半；它是「中序里根左边的元素数」。
3. 前序切分：左子树占 [pre_start+1, pre_start+left_size]，右子树占其后，别算错边界。
4. 有重复值的树这题用不了（根的位置不唯一），题目保证无重复。
"""


def build_tree_from_pre_in(preorder: list[int], inorder: list[int]) -> "TreeNode | None":
    idx_map = {v: i for i, v in enumerate(inorder)}   # 值 → 中序下标

    def build(pre_start: int, pre_end: int, in_start: int, in_end: int) -> "TreeNode | None":
        if pre_start > pre_end:
            return None
        root_val = preorder[pre_start]
        i = idx_map[root_val]                  # 根在中序的位置
        left_size = i - in_start               # 左子树节点数
        root = TreeNode(root_val)
        root.left = build(pre_start + 1, pre_start + left_size, in_start, i - 1)
        root.right = build(pre_start + left_size + 1, pre_end, i + 1, in_end)
        return root

    return build(0, len(preorder) - 1, 0, len(inorder) - 1)


# ============================================================
# 第 66 题：爬楼梯（LeetCode 70）
# ============================================================
r"""
题目描述
--------
假设你正在爬 n 阶楼梯。每次可以爬 1 或 2 个台阶。问有多少种不同的方法爬到顶部？

输入：n = 2   输出：2    （1+1，或 2）
输入：n = 3   输出：3    （1+1+1，1+2，2+1）
输入：n = 5   输出：8

通用解法（动态规划，滚动变量 O(1) 空间）
---------------------------------------------------
思考：要到达第 i 阶，最后一步只有两种可能：
  - 从 i-1 阶跨 1 步上来 → 方法有 dp[i-1] 种
  - 从 i-2 阶跨 2 步上来 → 方法有 dp[i-2] 种
所以 dp[i] = dp[i-1] + dp[i-2]。
这就是斐波那契数列！用两个变量滚动即可，不用开数组。

    a, b = 1, 1          # dp[0]=1(地面), dp[1]=1(到1阶只有1种)
    for _ in range(2, n+1):
        a, b = b, a + b
    return b

流程示意（n=5，dp 值随台阶变化）
--------------------------------------------------------------------------------
  dp[0]=1  dp[1]=1  dp[2]=2  dp[3]=3  dp[4]=5  dp[5]=8
   地面      1阶      2种      3种      5种      8种
  （每一步都等于前两步之和）

复杂度
------
时间 O(n)：循环 n-1 次。
空间 O(1)：只用两个变量。

面试易错点
---------
1. 边界：n=1 返回 1，n=2 返回 2。注意 dp[0]=1 是「地面算一种」，不是 0。
2. 这题是「斐波那契」换皮，面试常连着 #67 一起考。
3. n 很大时（如 10^9）O(n) 会超时，需要矩阵快速幂；但面试手撕 n≤45 用本解法即可。
"""


def climb_stairs(n: int) -> int:
    if n <= 1:
        return 1
    a, b = 1, 1          # dp[0], dp[1]
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


# ============================================================
# 第 67 题：斐波那契数（LeetCode 509）
# ============================================================
r"""
题目描述
--------
斐波那契数定义：F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)（n≥2）。给定 n，返回 F(n)。

输入：n = 2   输出：1    （F(2)=F(1)+F(0)=1+0）
输入：n = 10  输出：55

通用解法（动态规划，滚动变量）
---------------------------------------------------
和爬楼梯同一个递推。从下往上算，只保留前两个值：

    if n < 2: return n
    a, b = 0, 1          # F(0), F(1)
    for _ in range(2, n+1):
        a, b = b, a + b
    return b

（不要写朴素递归 F(n)=F(n-1)+F(n-2)，那样是指数级 O(2^n)，面试直接挂。）

流程示意（n=6，a/b 滚动）
--------------------------------------------------------------------------------
  初始: a=0(F0), b=1(F1)
  i=2: a=1, b=1   (F2=1)
  i=3: a=1, b=2   (F3=2)
  i=4: a=2, b=3   (F4=3)
  i=5: a=3, b=5   (F5=5)
  i=6: a=5, b=8   (F6=8)  → 返回 8

复杂度
------
时间 O(n)，空间 O(1)。

面试易错点
---------
1. 千万别写朴素递归（指数复杂度），面试官最忌讳这个。
2. F(0)=0, F(1)=1 是基准；n<2 直接返回 n 即可。
3. 和 #66 爬楼梯是同一递推，记住「滚动双变量」模板，两题通吃。
"""


def fib(n: int) -> int:
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


# ============================================================
# 第 68 题：不同路径（LeetCode 62）
# ============================================================
r"""
题目描述
--------
一个 m 行 n 列的网格，一个机器人从左上角 (0,0) 出发，每次只能「向下」或「向右」走，
问到达右下角 (m-1, n-1) 共有多少条不同路径？

输入：m = 3, n = 7   输出：28
输入：m = 3, n = 2   输出：3    （路径：右右、右下、下右 → 3 种）

通用解法（二维动态规划）
---------------------------------------------------
状态定义：dp[i][j] = 到达格子 (i,j) 的路径数。
转移：到 (i,j) 只能从「上方 (i-1,j)」或「左方 (i,j-1)」来：
    dp[i][j] = dp[i-1][j] + dp[i][j-1]
基准：第一行 / 第一列只有一种走法（一路右 / 一路下），都初始化为 1。

    dp = [[0]*n for _ in range(m)]
    第一行、第一列全填 1
    for i in 1..m-1:
      for j in 1..n-1:
        dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]

（进阶：答案其实就是组合数 C((m-1)+(n-1), m-1)，可直接用排列组合算。）

流程示意（m=3, n=2，dp 表）
--------------------------------------------------------------------------------
  起点(0,0)   (0,1)
   (1,0)      (1,1)终点
  dp 值：
   [1, 1]
   [1, 2]
  走到 (1,1) = dp[0][1] + dp[1][0] = 1 + 1 = 2？等下，n=2 时终点是 (2,1)：
  实际 3x2 网格dp：
   [1, 1]
   [1, 2]
   [1, 3]   → 终点 = 3 ✓ （C(2+1,2)=C(3,2)=3）

复杂度
------
时间 O(m*n)，空间 O(m*n)（可优化到 O(n)，只保留上一行）。

面试易错点
---------
1. 基准初始化：第一行、第一列都只能是 1（没有第二条路），不能全 0。
2. 下标别搞混 m 行 n 列，dp 是 `dp[m][n]`；循环 i 走行、j 走列。
3. 这题是「无障碍」，下一题 #69 加障碍，套路一样只是多一步判断。
"""


def unique_paths(m: int, n: int) -> int:
    dp = [[0] * n for _ in range(m)]
    for j in range(n):            # 第一行
        dp[0][j] = 1
    for i in range(m):            # 第一列
        dp[i][0] = 1
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]


# ============================================================
# 第 69 题：不同路径 II（LeetCode 63）
# ============================================================
r"""
题目描述
--------
在 #68 基础上，网格里有些格子是「障碍」（用 1 表示），机器人不能经过。
问从左上角到右下角共有多少条不同路径？障碍和空格分别用 1 和 0 表示。

输入：obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]   输出：2
输入：obstacleGrid = [[1,0]]                     输出：0（起点就是障碍）
输入：obstacleGrid = [[0,0],[0,1]]               输出：0（终点被挡）

通用解法（二维 DP + 障碍判断）
---------------------------------------------------
思路和 #68 完全一致，只是：
  - 起点若是障碍 → 直接返回 0（根本走不了）
  - 第一行/列传播时，一旦遇到障碍，后面就全是 0（被挡死了）
  - 任意格子若是障碍 → dp[i][j] = 0（不经过它）

    dp = [[0]*n for _ in range(m)]
    if grid[0][0] == 1: return 0
    dp[0][0] = 1
    第一行：dp[0][j] = dp[0][j-1] if 无障 else 0
    第一列：dp[i][0] = dp[i-1][0] if 无障 else 0
    for i,j: if 无障: dp[i][j] = dp[i-1][j] + dp[i][j-1]  （else 保持 0）

流程示意（[[0,0,0],[0,1,0],[0,0,0]]，障碍在 (1,1)）
--------------------------------------------------------------------------------
  dp 表（障碍格标 X）：
   [1, 1, 1]
   [1, X, 1]      ← (1,1) 是障碍=0，但 (1,2) 仍能从 (0,2) 下来
   [1, 1, 2]      ← 终点 = 上(1)+左(1)=2 ✓
  总路径 2 条（绕开中间的障碍）

复杂度
------
时间 O(m*n)，空间 O(m*n)（可优化到 O(n)）。

面试易错点
---------
1. 起点是障碍要特判返回 0；很多实现忘这步会返回 1 错。
2. 第一行/列遇到障碍后，后面的要「清零并保持 0」，不能用简单的全 1 初始化。
3. 障碍格本身 dp 必须是 0（不累加），否则会把死路算进去。
4. 这是 #68 的「加料版」，先写通 #68 再改这题最稳。
"""


def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    m = len(obstacle_grid)
    n = len(obstacle_grid[0])
    dp = [[0] * n for _ in range(m)]
    if obstacle_grid[0][0] == 1:        # 起点就被挡 → 走不了
        return 0
    dp[0][0] = 1
    for j in range(1, n):               # 第一行传播
        dp[0][j] = dp[0][j - 1] if obstacle_grid[0][j] == 0 else 0
    for i in range(1, m):               # 第一列传播
        dp[i][0] = dp[i - 1][0] if obstacle_grid[i][0] == 0 else 0
    for i in range(1, m):
        for j in range(1, n):
            if obstacle_grid[i][j] == 0:     # 无障碍才累加
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]


# ============================================================
# 测试运行：全部跑通即说明代码正确
# ============================================================
def _run_tests() -> None:
    print("=" * 66)
    print("LeetCode 必刷100题 · Day 14 自测")
    print("=" * 66)

    print("\n第 60 题：验证二叉搜索树（LeetCode 98）")
    v1 = is_valid_bst(build_tree([2, 1, 3]))
    ok1 = v1 is True
    print(f"  [2,1,3]              -> {v1}  期望 True  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    v2 = is_valid_bst(build_tree([5, 1, 4, None, None, 3, 6]))
    ok2 = v2 is False
    print(f"  [5,1,4,null,null,3,6]-> {v2}  期望 False [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    v3 = is_valid_bst(build_tree([2, 2, 2]))
    ok3 = v3 is False
    print(f"  [2,2,2]              -> {v3}  期望 False [{'PASS' if ok3 else 'FAIL'}]"); assert ok3
    v4 = is_valid_bst(build_tree([]))
    ok4 = v4 is True
    print(f"  []                   -> {v4}  期望 True  [{'PASS' if ok4 else 'FAIL'}]"); assert ok4

    print("\n第 61 题：二叉树的所有路径（LeetCode 257）")
    p1 = binary_tree_paths(build_tree([1, 2, 3, None, 5]))
    ok1 = set(p1) == {"1->2->5", "1->3"}
    print(f"  [1,2,3,null,5]       -> {p1}  期望 ['1->2->5','1->3']  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    p2 = binary_tree_paths(build_tree([1]))
    ok2 = p2 == ["1"]
    print(f"  [1]                  -> {p2}  期望 ['1']  [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    p3 = binary_tree_paths(build_tree([1, 2, None, 3]))
    ok3 = p3 == ["1->2->3"]
    print(f"  [1,2,null,3]         -> {p3}  期望 ['1->2->3']  [{'PASS' if ok3 else 'FAIL'}]"); assert ok3

    print("\n第 62 题：二叉搜索树中的搜索（LeetCode 700）")
    bst = build_tree([4, 2, 7, 1, 3])
    s1 = search_bst(bst, 2)
    ok1 = s1 is not None and to_level(s1) == [2, 1, 3]
    print(f"  [4,2,7,1,3], val=2   -> {to_level(s1) if s1 else None}  期望 [2,1,3]  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    s2 = search_bst(bst, 5)
    ok2 = s2 is None
    print(f"  [4,2,7,1,3], val=5   -> {s2}  期望 None  [{'PASS' if ok2 else 'FAIL'}]"); assert ok2

    print("\n第 63 题：删除二叉搜索树中的节点（LeetCode 450）")
    t63 = build_tree([5, 3, 6, 2, 4, None, None, 1])
    d1 = delete_node(t63, 4)     # 删叶子
    ok1 = to_level(d1) == [5, 3, 6, 2, None, None, None, 1]
    print(f"  删 key=4（叶子）     -> {to_level(d1)}  期望 [5,3,6,2,null,null,null,1]  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    t63b = build_tree([5, 3, 6, 2, 4, None, None, 1])
    d2 = delete_node(t63b, 3)    # 删两孩子节点
    ok2 = to_level(d2) == [5, 4, 6, 2, None, None, None, 1]
    print(f"  删 key=3（双孩子）   -> {to_level(d2)}  期望 [5,4,6,2,null,null,null,1]  [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    t63c = build_tree([5, 3, 6, 2, 4, None, None, 1])
    d3 = delete_node(t63c, 5)    # 删根
    ok3 = to_level(d3) == [6, 3, None, 2, 4, 1]
    print(f"  删 key=5（根）       -> {to_level(d3)}  期望 [6,3,null,2,4,1]  [{'PASS' if ok3 else 'FAIL'}]"); assert ok3

    print("\n第 64 题：二叉树展开为链表（LeetCode 114）")
    t64 = build_tree([1, 2, 5, 3, 4, None, 6])
    flatten(t64)
    ok1 = to_list(t64) == [1, 2, 3, 4, 5, 6]
    print(f"  [1,2,5,3,4,null,6]   -> {to_list(t64)}  期望 [1,2,3,4,5,6]  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    t64b = build_tree([1])
    flatten(t64b)
    ok2 = to_list(t64b) == [1]
    print(f"  [1]                  -> {to_list(t64b)}  期望 [1]  [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    t64c = build_tree([])
    flatten(t64c)
    ok3 = to_list(t64c) == []
    print(f"  []                   -> {to_list(t64c)}  期望 []  [{'PASS' if ok3 else 'FAIL'}]"); assert ok3

    print("\n第 65 题：从前序与中序遍历构造二叉树（LeetCode 105）")
    c1 = build_tree_from_pre_in([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])
    ok1 = to_level(c1) == [3, 9, 20, None, None, 15, 7]
    print(f"  pre=[3,9,20,15,7]    -> {to_level(c1)}  期望 [3,9,20,null,null,15,7]  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    c2 = build_tree_from_pre_in([1], [1])
    ok2 = to_level(c2) == [1]
    print(f"  pre=[1]              -> {to_level(c2)}  期望 [1]  [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    c3 = build_tree_from_pre_in([1, 2, 3], [3, 2, 1])
    ok3 = to_level(c3) == [1, 2, None, 3]
    print(f"  pre=[1,2,3]          -> {to_level(c3)}  期望 [1,2,null,3]  [{'PASS' if ok3 else 'FAIL'}]"); assert ok3

    print("\n第 66 题：爬楼梯（LeetCode 70）")
    a1 = climb_stairs(2)
    ok1 = a1 == 2
    print(f"  n=2                  -> {a1}  期望 2  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    a2 = climb_stairs(3)
    ok2 = a2 == 3
    print(f"  n=3                  -> {a2}  期望 3  [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    a3 = climb_stairs(5)
    ok3 = a3 == 8
    print(f"  n=5                  -> {a3}  期望 8  [{'PASS' if ok3 else 'FAIL'}]"); assert ok3
    a4 = climb_stairs(1)
    ok4 = a4 == 1
    print(f"  n=1                  -> {a4}  期望 1  [{'PASS' if ok4 else 'FAIL'}]"); assert ok4

    print("\n第 67 题：斐波那契数（LeetCode 509）")
    f1 = fib(0)
    ok1 = f1 == 0
    print(f"  n=0                  -> {f1}  期望 0  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    f2 = fib(2)
    ok2 = f2 == 1
    print(f"  n=2                  -> {f2}  期望 1  [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    f3 = fib(10)
    ok3 = f3 == 55
    print(f"  n=10                 -> {f3}  期望 55  [{'PASS' if ok3 else 'FAIL'}]"); assert ok3

    print("\n第 68 题：不同路径（LeetCode 62）")
    u1 = unique_paths(3, 7)
    ok1 = u1 == 28
    print(f"  m=3,n=7              -> {u1}  期望 28  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    u2 = unique_paths(3, 2)
    ok2 = u2 == 3
    print(f"  m=3,n=2              -> {u2}  期望 3  [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    u3 = unique_paths(1, 1)
    ok3 = u3 == 1
    print(f"  m=1,n=1              -> {u3}  期望 1  [{'PASS' if ok3 else 'FAIL'}]"); assert ok3

    print("\n第 69 题：不同路径 II（LeetCode 63）")
    o1 = unique_paths_with_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    ok1 = o1 == 2
    print(f"  [[0,0,0],[0,1,0],..] -> {o1}  期望 2  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    o2 = unique_paths_with_obstacles([[1, 0]])
    ok2 = o2 == 0
    print(f"  [[1,0]]              -> {o2}  期望 0  [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    o3 = unique_paths_with_obstacles([[0, 0], [0, 1]])
    ok3 = o3 == 0
    print(f"  [[0,0],[0,1]]        -> {o3}  期望 0  [{'PASS' if ok3 else 'FAIL'}]"); assert ok3

    print("\n" + "=" * 66)
    print("Day 14 全部 10 题测试通过！（共 68/100 题已完成）")
    print("下次（Day 15）预告：#70 最小路径和 / #71 三角形最小路径和 / #72 子集 / #73 子集 II")
    print("                   / #74 组合总和 / #75 组合总和 II（按总表 #70–#79 起手，补齐 10 道）")
    print("=" * 66)


if __name__ == "__main__":
    _run_tests()
