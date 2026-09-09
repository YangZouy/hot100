"""
LeetCode 必刷100题 · Day 13（2026-07-30）
========================================
面试方向：AI 应用 / Agent 开发
今日题目（共 10 道，对应必刷表 #50–#59）：
  - 第 50 题：二叉树的最大深度            LeetCode 104   简单   频率 ⭐⭐⭐⭐⭐  （DFS 递归）
  - 第 51 题：对称二叉树                  LeetCode 101   简单   频率 ⭐⭐⭐⭐⭐  （双指针递归 / 镜像）
  - 第 52 题：路径总和                    LeetCode 112   简单   频率 ⭐⭐⭐⭐    （DFS 自顶向下）
  - 第 53 题：翻转二叉树                  LeetCode 226   简单   频率 ⭐⭐⭐⭐⭐  （递归交换 / 迭代）
  - 第 54 题：相同的树                    LeetCode 100   简单   频率 ⭐⭐⭐⭐    （双树同步递归）
  - 第 55 题：二叉搜索树的最近公共祖先     LeetCode 235   简单   频率 ⭐⭐⭐⭐⭐  （利用 BST 性质）
  - 第 56 题：二叉树的最近公共祖先         LeetCode 236   中等   频率 ⭐⭐⭐⭐⭐  （后序递归返回）
  - 第 57 题：二叉树的右视图              LeetCode 199   中等   频率 ⭐⭐⭐⭐    （层序取最右）
  - 第 58 题：二叉树的锯齿形层序遍历       LeetCode 103   中等   频率 ⭐⭐⭐⭐    （层序 + 奇偶翻转）
  - 第 59 题：将有序数组转换为二叉搜索树   LeetCode 108   简单   频率 ⭐⭐⭐⭐    （分治取中点）

运行方式：
    python LeetCode-Day13.py
会自动执行所有测试用例并打印 PASS / FAIL，全部通过即说明代码正确。

每个题目都包含：① 思路讲解 ② 流程示意图（ASCII）③ 可运行代码 ④ 复杂度分析 ⑤ 面试易错点。
只给一种「通用解法」，方便记忆和手撕。

今日主题：二叉树递归 / 性质篇章（#50–#59）。
Day 12 打好了「三序遍历 + 层序」的地基，今天这 10 题是地基上的第一层应用：
- #50 最大深度：最朴素的 DFS，所有树高/树形 DP 的基础。
- #51/#54 对称与相同：双树「同步递归」的模板，面试常连考。
- #52 路径总和：自顶向下带「当前累计值」的 DFS，回溯题的雏形。
- #53 翻转：改树的指针，递归三行搞定，面试官最爱拿它考察「是否敢改结构」。
- #55/#56 LCA（最近公共祖先）：树里最经典的一类题，#55 吃 BST 性质 O(h)，#56 通用 O(n)。
- #57/#58：都是「层序遍历」的变体（取最右 / 之字形），把 Day 12 的 level_order 改一下即可。
- #59 有序数组转 BST：分治 + 取中点，构造平衡树的经典手法。
"""

from collections import deque


# ============================================================
# 通用工具：TreeNode 定义 + 建树 / 序列化的辅助函数
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
    """按值找节点（测试里给 LCA 题型准备 p / q 的引用用）。"""
    if not root:
        return None
    if root.val == val:
        return root
    return find_node(root.left, val) or find_node(root.right, val)


# ============================================================
# 第 50 题：二叉树的最大深度（LeetCode 104）
# ============================================================
r"""
题目描述
--------
给定一个二叉树，返回它的最大深度（从根节点到最远叶子节点的最长路径上的节点数）。

输入：[3,9,20,None,None,15,7]   输出：3
       树：      3
              /   \
             9    20
                 /  \
                15   7
输入：[]                 输出：0
输入：[1,2,3,4,5]        输出：3（1→2→4 这条链，3 层）

通用解法（DFS 递归，最直观）
---------------------------------------------------
核心思想：一棵树的深度 = 1（自己这层）+ 左右子树里「更深的那棵」的深度。
这是典型的「自底向上」递归：先让左右子树各自报出自己的深度，我再 +1 上报。

    maxDepth(node) = 0                         ，如果 node 是空
                   1 + max(maxDepth(左), maxDepth(右))，否则

流程示意（示例树，标注每个节点返回的深度）
--------------------------------------------------------------------------------
           3 ── 返回 1+max(1,2)=3
          / \
  9 ── 1  └── 20 ── 返回 1+max(1,1)=2
               /  \
    15 ── 1   └── 7 ── 1

递归先「沉到底」：叶子 9/15/7 都返回 1；
20 拿到左右都是 1 → 返回 2；
3 拿到左=1、右=2 → 返回 3 = 最大深度。

复杂度
------
时间 O(n)：每个节点恰好访问一次。
空间 O(h)：递归栈深度 = 树高 h，最坏退化为链 O(n)，平衡树 O(log n)。

面试易错点
---------
1. 空树返回 0，不是 1。根节点本身算 1 层，所以「没有节点」才是 0。
2. 是 max(左, 右) 取较大值，不是相加。很多新手会写成 left+right，那是数节点数不是深度。
3. 这题是「后序」思想（先子后父），和前序遍历顺序相反，写的时候别混。
"""


def max_depth(root: "TreeNode | None") -> int:
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


# ============================================================
# 第 51 题：对称二叉树（LeetCode 101）
# ============================================================
r"""
题目描述
--------
判断一棵二叉树是否「中心对称」（即左子树是右子树的镜像）。

输入：[1,2,2,3,4,4,3]   输出：True
       树：      1
              /   \
             2     2
            / \   / \
           3   4 4   3        ← 以 1 为轴左右镜像，对称

输入：[1,2,2,None,3,None,3]  输出：False
       树：      1
              /   \
             2     2
              \     \
               3     3        ← 左子树的 3 在右边，右子树的 3 也在右边，不对称

通用解法（双指针递归 / 镜像比较）
---------------------------------------------------
思路：树对称 ⇔ 它的左子树 和 右子树「互为镜像」。
我们写一个助手 is_mirror(a, b)，判断两棵树是否镜像：
  1. a、b 都为空 → 对称（True）
  2. 只有一个为空 → 不对称（False）
  3. a.val ≠ b.val → 不对称（False）
  4. 关键：a 的左要对应 b 的右，a 的右要对应 b 的左：
         return is_mirror(a.left, b.right) and is_mirror(a.right, b.left)
顶层：整棵树对称 ⇔ is_mirror(root.left, root.right)。

流程示意（[1,2,2,3,4,4,3]，比较配对关系）
--------------------------------------------------------------------------------
        1
      /   \
   L=2     R=2
  比较 (L,R)：
    L.left=3  ↔  R.right=3    ✓
    L.right=4 ↔  R.left=4     ✓
  再各自比较 3↔3、4↔4（都是叶子，且值相等）→ 全 True → 对称

（注意箭头是「交叉」的：左孩子的左 对 右孩子的右，这就是为什么叫镜像。）

复杂度
------
时间 O(n)，空间 O(h)（递归栈）。

面试易错点
---------
1. 镜像比较是「交叉配对」：a.left 配 b.right，写反成 a.left 配 b.left 就变成「相同树」了（见 #54）。
2. 空树、只有根节点都算对称（True）。顶层调用前先判空。
3. 很多人会想「直接比较左右子树是否相等」，那是错的——对称是镜像不是相等。
"""


def is_symmetric(root: "TreeNode | None") -> bool:
    def is_mirror(a: "TreeNode | None", b: "TreeNode | None") -> bool:
        if not a and not b:
            return True
        if not a or not b:
            return False
        if a.val != b.val:
            return False
        # 交叉配对：左配右、右配左
        return is_mirror(a.left, b.right) and is_mirror(a.right, b.left)

    if not root:
        return True
    return is_mirror(root.left, root.right)


# ============================================================
# 第 52 题：路径总和（LeetCode 112）
# ============================================================
r"""
题目描述
--------
判断是否存在一条从「根节点到叶子节点」的路径，使得路径上所有节点值之和等于目标值 targetSum。
「叶子节点」= 没有左右孩子的节点。

输入：[5,4,8,11,None,13,4,7,2,None,None,None,1], targetSum = 22   输出：True
       树：      5
              /   \
             4     8
            /     / \
           11    13  4
          /  \        \
         7    2        1
   （5→4→11→2 = 22，存在）

输入：[1,2,3], targetSum = 5   输出：False（没有根到叶的路径和为 5）
输入：[1,2], targetSum = 1     输出：False（1 不是叶子，必须走到叶子）

通用解法（DFS 自顶向下，带着「剩余值」往下走）
---------------------------------------------------
核心思想：从根往下走，每经过一个节点，就把 targetSum 减去当前节点值，
当走到「叶子」时，看剩余值是否正好减到 0。

    hasPathSum(node, remain):
      若 node 为空 → False（走到空了，没路）
      若 node 是叶子（无左右孩子）→ 返回 remain == node.val
      否则 → 去左子树找 (remain - node.val) 或 去右子树找 (remain - node.val)

「或」表示：左子树能找到 或 右子树能找到 都算存在。

流程示意（示例树，标注每个节点的 remain = 22 - 已走路径和）
--------------------------------------------------------------------------------
  5 (remain 22)
  ├─ 4 (remain 17)
  │   └─ 11 (remain 6)
  │        ├─ 7 (remain -1) → 叶子, -1≠7 ✗
  │        └─ 2 (remain 0)  → 叶子, 0==2? 实际 remain 到 2 是 0 → ✓ 找到!
  └─ 8 ...（左边已找到，直接返回 True，右边不用再走）

复杂度
------
时间 O(n)，空间 O(h)。

面试易错点
---------
1. 必须是「到叶子」才算数！常见 bug：在根节点就 return remain==0，但根可能不是叶子。
   一定要先判断「是否叶子」再判等。
2. 用 remain - node.val 往下传，而不是重新累加，避免维护全局变量。
3. 用「或」连接左右子树的结果；只要任一条路径满足即返回 True。
"""


def has_path_sum(root: "TreeNode | None", target_sum: int) -> bool:
    if not root:
        return False
    # 走到叶子：判断剩余值是否正好等于当前叶子的值
    if not root.left and not root.right:
        return root.val == target_sum
    rest = target_sum - root.val
    return has_path_sum(root.left, rest) or has_path_sum(root.right, rest)


# ============================================================
# 第 53 题：翻转二叉树（LeetCode 226）
# ============================================================
"""
题目描述
--------
翻转一棵二叉树（每个节点的左右子树互换）。要求「原地」翻转，返回根节点。

输入：[4,2,7,1,3,6,9]   输出：[4,7,2,9,6,3,1]
       原树：       翻转后：
        4             4
      /   \         /   \
     2     7       7     2
    / \   / \     / \   / \
   1   3 6   9   9   6 3   1

通用解法（递归交换，最简洁）
---------------------------------------------------
思路：对当前节点，先递归把左右子树各自翻转好，再交换当前节点的左右指针。
顺序无所谓（先翻后换、或先换后翻都行，因为换的是指针）。

    invert(node):
      若 node 为空 → 返回 None
      翻转左子树：invert(node.left)
      翻转右子树：invert(node.right)
      交换 node.left 与 node.right
      返回 node

流程示意（示例树，递归到底再逐层交换）
--------------------------------------------------------------------------------
递归先到底：
  1、3、6、9 都是叶子 → 翻转后还是自己（无子树可换）
回到 2：左=1、右=3 → 交换 → 2 变成 (左3, 右1)
回到 7：左=6、右=9 → 交换 → 7 变成 (左9, 右6)
回到 4：左=2、右=7 → 交换 → 4 变成 (左7, 右2)
完成，根还是 4，但整棵树镜像了。

复杂度
------
时间 O(n)（每个节点访问一次），空间 O(h)（递归栈）。

面试易错点
---------
1. 递归版本只要 4 行，面试时先写这个；别一上来就纠结迭代版。
2. 交换的是「指针」（node.left, node.right 这两个引用），不是交换 val。
   如果交换 val，遇到非满树会出错。
3. 别忘了递归的「base case」：node 为空时直接返回 None，否则会段错误。
"""


def invert_tree(root: "TreeNode | None") -> "TreeNode | None":
    if not root:
        return None
    # 先（或后）翻转左右子树，再交换当前节点的左右指针
    left = invert_tree(root.left)
    right = invert_tree(root.right)
    root.left, root.right = right, left
    return root


# ============================================================
# 第 54 题：相同的树（LeetCode 100）
# ============================================================
"""
题目描述
--------
判断两棵二叉树是否「结构和节点值」完全相同。

输入：[1,2,3], [1,2,3]                 输出：True
输入：[1,2],   [1,None,2]             输出：False（结构不同）
输入：[1,2,1], [1,1,2]                输出：False（值不同）

通用解法（双树同步递归）
---------------------------------------------------
和 #51 的镜像比较是「兄弟题」，区别只是这里不交叉：
两个节点 p、q 相同 ⇔
  1. 都为空 → True
  2. 只有一个为空 → False
  3. p.val ≠ q.val → False
  4. p.left 与 q.left 相同 且 p.right 与 q.right 相同

流程示意（[1,2,3] vs [1,2,3]）
--------------------------------------------------------------------------------
  比较 (1,1) ✓ → 再比较 (2,2) 和 (3,3)
    (2,2) ✓ → 比较 (None,None)✓、(None,None)✓ → True
    (3,3) ✓ → 比较 (None,None)✓、(None,None)✓ → True
  全 True → 两树相同

对比 [1,2] vs [1,None,2]：
  比较 (1,1)✓ → 比较 (2, None)✗（一个为空一个不为空）→ 直接 False

复杂度
------
时间 O(n)（n 为较小树的节点数），空间 O(h)。

面试易错点
---------
1. 是「不交叉」配对：p.left 配 q.left。写成交叉（p.left 配 q.right）就变成了判断镜像。
2. 不仅要值相同，结构也必须相同：一个空一个不空，直接判 False。
3. #51 对称 本质是 is_mirror(root.left, root.right)；这题是 is_same(p, q) 比较两个独立树，
   联系起来记不容易混。
"""


def is_same_tree(p: "TreeNode | None", q: "TreeNode | None") -> bool:
    if not p and not q:
        return True
    if not p or not q:
        return False
    if p.val != q.val:
        return False
    # 不交叉：左配左、右配右
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)


# ============================================================
# 第 55 题：二叉搜索树的最近公共祖先（LeetCode 235）
# ============================================================
"""
题目描述
--------
给定一棵「二叉搜索树（BST）」和两个节点 p、q，找到它们的最近公共祖先（LCA）。
BST 性质：左子树所有值 < 根值 < 右子树所有值。

输入：树 [6,2,8,0,4,7,9,3,5]，p = 2，q = 8   输出：6（根 6 就是 2 和 8 的公共祖先，且最近）
输入：同上，p = 2，q = 4                       输出：2（2 本身就是 4 的祖先）

通用解法（利用 BST 性质，一次向下走）
---------------------------------------------------
关键观察：从根往下，p、q 的 LCA 是「第一个让 p、q 分叉」的节点——
  - 若当前节点值比 p、q 都大 → p、q 都在左子树 → 往左走
  - 若当前节点值比 p、q 都小 → p、q 都在右子树 → 往右走
  - 否则（当前节点落在 p、q 之间，或等于其中之一）→ 当前节点就是 LCA

设 a = min(p.val, q.val)，b = max(p.val, q.val)：
    while root:
        if root.val < a:  root = root.right
        elif root.val > b: root = root.left
        else: return root

流程示意（树 [6,2,8,0,4,7,9,3,5]，p=2, q=8，a=2, b=8）
--------------------------------------------------------------------------------
  root=6: 6 在 [2,8] 之间（2≤6≤8）→ 命中，LCA = 6 ✓

  （换 p=2, q=4，a=2, b=4）
  root=6: 6 > 4 → 往左，root=2
  root=2: 2 在 [2,4] 之间 → 命中，LCA = 2 ✓

复杂度
------
时间 O(h)（h 为树高，平衡 BST 为 O(log n)），空间 O(1)（迭代，无递归栈）。

面试易错点
---------
1. 这题是 BST，才能用「比大小往一边走」的 O(h) 写法。若换成普通二叉树（#56）不能用这招。
2. 先把 p、q 的值归一化成 a=min, b=max，否则「谁大谁小」的分支会写乱。
3. 命中条件是「root.val 落在 [a,b] 闭区间内（含端点）」，等于 p 或 q 也算命中。
"""


def lowest_common_ancestor_bst(root: "TreeNode | None", p: "TreeNode",
                                q: "TreeNode") -> "TreeNode | None":
    a, b = min(p.val, q.val), max(p.val, q.val)
    while root:
        if root.val < a:
            root = root.right
        elif root.val > b:
            root = root.left
        else:
            return root
    return None


# ============================================================
# 第 56 题：二叉树的最近公共祖先（LeetCode 236）
# ============================================================
"""
题目描述
--------
给定一棵「普通二叉树」和两个节点 p、q，找到它们的最近公共祖先。
（注意：这题没有 BST 性质，不能用 #55 的比大小写法。）

输入：树 [3,5,1,6,2,0,8,None,None,7,4]，p = 5，q = 1   输出：3
输入：同上，p = 5，q = 4                             输出：5（5 是 4 的祖先）

通用解法（后序递归，自底向上返回）
---------------------------------------------------
思路：从叶子往根回传信息。对每个节点：
  - 如果当前节点就是 p 或 q，直接把自己返回（找到了目标之一）。
  - 否则，去左右子树各找一遍：
        left  = 在左子树里找 p/q
        right = 在右子树里找 p/q
  - 如果 left 和 right 都非空 → 说明 p、q 分别在当前节点的两侧 → 当前节点就是 LCA。
  - 如果只有一个非空 → 把那个非空结果继续往上传（LCA 还在更上层或就是它）。

    lca(node):
        if node is None or node is p or node is q: return node
        left  = lca(node.left)
        right = lca(node.right)
        if left and right: return node      # p、q 分居两侧，命中
        return left or right                 # 否则把找到的那边往上带

流程示意（树 [3,5,1,6,2,0,8,None,None,7,4]，p=5, q=1）
--------------------------------------------------------------------------------
       3
     /   \
    5     1
   / \   / \
  6   2 0   8
     / \
    7   4

  lca(5,...) 因为 5 就是 p → 返回 5
  lca(1,...) 因为 1 就是 q → 返回 1
  lca(3,...): left=5, right=1 → 两边都非空 → 返回 3 = LCA ✓

  （若 p=5, q=4：lca(5) 返回 5（命中 p）；lca(4) 返回 4；
   lca(2) 拿到 left=空, right=4 → 返回 4 往上带；
   lca(5) 拿到 left=空, right=4 → 但 5 本身就是 p 已先返回 5。
   最终 5 是 LCA ✓）

复杂度
------
时间 O(n)（最多遍历全树），空间 O(h)（递归栈）。

面试易错点
---------
1. 比较节点要用「身份 is」（node is p），不是比 val——值可能重复，比 val 会错。
2. 这是「后序」：先递归左右，再根据左右结果决策，千万别写成前序。
3. 和 #55 的区别：#55 吃 BST 性质 O(h) 迭代；#56 通用但需 O(n) 递归。面试被问「BST 版怎么优化」就答 #55。
"""


def lowest_common_ancestor(root: "TreeNode | None", p: "TreeNode",
                            q: "TreeNode") -> "TreeNode | None":
    if root is None or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:          # p、q 分居左右 → 当前节点就是 LCA
        return root
    return left or right        # 否则把找到的那边继续往上传


# ============================================================
# 第 57 题：二叉树的右视图（LeetCode 199）
# ============================================================
r"""
题目描述
--------
从右侧看一棵二叉树，能看到的节点自上而下组成列表（即每一层「最右边」的那个节点）。

输入：[1,2,3,None,5,None,4]   输出：[1,3,4]
       树：      1
              /   \
             2     3
              \     \
               5     4
  第1层看到 1，第2层看到 3，第3层看到 4。

通用解法（层序遍历 BFS，每层取最后一个）
---------------------------------------------------
Day 12 我们写好了 level_order（按层分组）。右视图就是：对每一层，取该层列表的最后一个元素。
（也可以 DFS 按深度记录第一次遇到的节点，但 BFS 最直观、最好记。）

    res = []
    BFS 逐层：每层 level 列表 → res.append(level[-1])

流程示意（[1,2,3,None,5,None,4]，queue 用「左|右」）
--------------------------------------------------------------------------------
初始队列: [1]                    第1层 [1]          → 右视图取 1
           加入 2,3 → [2,3]
第2层: 弹出 [2,3]                → 取最后 3
           加入 5（2的右）, 4（3的右）→ [5,4]
第3层: 弹出 [5,4]                → 取最后 4
           无孩子，队列空
结果：[1, 3, 4]  ✓

复杂度
------
时间 O(n)，空间 O(n)（队列存一层）。

面试易错点
---------
1. 取的是「每层最后一个」，不是「最深的右链」。比如某层右节点为空，最右其实是中/左节点。
2. 建立在「正确的层序遍历」之上，所以 Day 12 的 level_order 必须先写对。
3. 空树返回 []。
"""


def right_side_view(root: "TreeNode | None") -> list[int]:
    if not root:
        return []
    res = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):          # 用 size 锁住本层边界
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(level[-1])            # 每层最右一个
    return res


# ============================================================
# 第 58 题：二叉树的锯齿形层序遍历（LeetCode 103）
# ============================================================
r"""
题目描述
--------
层序遍历，但相邻两层方向相反：第 0 层从左往右，第 1 层从右往左，第 2 层从左往右……

输入：[3,9,20,None,None,15,7]   输出：[[3],[20,9],[15,7]]
       树：      3
              /   \
             9     20
                 /  \
                15   7
  第0层 [3]（左→右），第1层 [20,9]（右→左），第2层 [15,7]（左→右）。

通用解法（层序遍历 + 按层号翻转）
---------------------------------------------------
在普通层序遍历基础上，加一个层号 i：
  - 若 i 是奇数（第 1、3、5…层）→ 把该层列表反转（变成从右往左）。
  - 偶数层保持原样。

    for i, level in enumerate(各层):
        if i % 2 == 1: level.reverse()
        res.append(level)

流程示意（[3,9,20,None,None,15,7]）
--------------------------------------------------------------------------------
level 0: [3]            i=0 偶 → 不翻 → [3]
level 1: [9,20]         i=1 奇 → 翻   → [20,9]
level 2: [15,7]         i=2 偶 → 不翻 → [15,7]
结果：[[3],[20,9],[15,7]]  ✓

复杂度
------
时间 O(n)，空间 O(n)。

面试易错点
---------
1. 是「每层整体翻转」，不是「每个元素交替」。很多人会误解成 [3,20,9,7,15] 这种平铺交替，错。
2. 层号从 0 开始：0 偶、1 奇，所以判断用 `i % 2 == 1`。
3. 同样建立在正确的层序遍历之上。
"""


def zigzag_level_order(root: "TreeNode | None") -> list[list[int]]:
    if not root:
        return []
    res = []
    q = deque([root])
    i = 0
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        if i % 2 == 1:          # 奇数层从右往左 → 翻转
            level.reverse()
        res.append(level)
        i += 1
    return res


# ============================================================
# 第 59 题：将有序数组转换为二叉搜索树（LeetCode 108）
# ============================================================
"""
题目描述
--------
给定一棵「升序」数组，把它转换成一棵「高度平衡」的二叉搜索树（BST）。
高度平衡：每个节点的左右子树高度差不超过 1。

输入：[-10,-3,0,5,9]   输出：[0,-3,9,-10,None,5]（层序，有多种合法答案，取中点的一种）
       树：        0
                /   \
              -3     9
              /     /
            -10     5

输入：[1,2,3]   输出：[2,1,3]

通用解法（分治，每次取中点做根）
---------------------------------------------------
升序数组天然满足 BST 的中序遍历。要让树平衡，就「每次取区间中点」当根，
这样左右子树分到的元素数量几乎相等，自然平衡。
    build(nums):
        if 空: return None
        mid = len(nums) // 2
        root = TreeNode(nums[mid])
        root.left  = build(nums[:mid])        # 左半边（都比 mid 小）
        root.right = build(nums[mid+1:])      # 右半边（都比 mid 大）
        return root

为什么平衡且是 BST：中点做根 → 左右子树规模差 ≤1；左半边都更小、右半边都更大 → 满足 BST。

流程示意（nums = [-10,-3,0,5,9]，长度 5，mid=2 → 根 0）
--------------------------------------------------------------------------------
  [-10,-3 | 0 | 5,9]
   左半 [-10,-3]  mid=1 → 根 -3，左 [-10]、右 空
   右半 [5,9]     mid=1 → 根 9，  左 [5]、  右 空
  拼起来：
          0
        /   \
      -3     9
      /     /
    -10     5
  层序表示：[0,-3,9,-10,None,5,None]（尾部 None 裁掉后 = [0,-3,9,-10,None,5]）

复杂度
------
时间 O(n)（每个元素恰好成为一次根），空间 O(log n)（递归深度 = 树高，平衡树 O(log n)）。

面试易错点
---------
1. 答案不唯一（取上中点 / 下中点都行），面试官看的是「平衡 + BST」而非固定形态。
2. 切片 nums[:mid] 和 nums[mid+1:] 别写成 nums[:mid-1] 之类，会漏元素或重复。
3. 必须用「升序」数组才能这么干；若数组无序，此法不成立。
"""


def sorted_array_to_bst(nums: list[int]) -> "TreeNode | None":
    if not nums:
        return None
    mid = len(nums) // 2
    root = TreeNode(nums[mid])
    root.left = sorted_array_to_bst(nums[:mid])
    root.right = sorted_array_to_bst(nums[mid + 1:])
    return root


# ============================================================
# 测试运行：全部跑通即说明代码正确
# ============================================================
def _run_tests() -> None:
    print("=" * 66)
    print("LeetCode 必刷100题 · Day 13 自测")
    print("=" * 66)

    print("\n第 50 题：二叉树的最大深度（LeetCode 104）")
    d1 = max_depth(build_tree([3, 9, 20, None, None, 15, 7]))
    ok1 = d1 == 3
    print(f"  [3,9,20,null,null,15,7] -> {d1}  期望 3   [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    d2 = max_depth(build_tree([]))
    ok2 = d2 == 0
    print(f"  []                   -> {d2}  期望 0   [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    d3 = max_depth(build_tree([1, 2, 3, 4, 5]))
    ok3 = d3 == 3
    print(f"  [1,2,3,4,5]          -> {d3}  期望 3   [{'PASS' if ok3 else 'FAIL'}]"); assert ok3
    d4 = max_depth(build_tree([1]))
    ok4 = d4 == 1
    print(f"  [1]                  -> {d4}  期望 1   [{'PASS' if ok4 else 'FAIL'}]"); assert ok4

    print("\n第 51 题：对称二叉树（LeetCode 101）")
    s1 = is_symmetric(build_tree([1, 2, 2, 3, 4, 4, 3]))
    ok1 = s1 is True
    print(f"  [1,2,2,3,4,4,3]      -> {s1}  期望 True  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    s2 = is_symmetric(build_tree([1, 2, 2, None, 3, None, 3]))
    ok2 = s2 is False
    print(f"  [1,2,2,null,3,null,3]-> {s2}  期望 False [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    s3 = is_symmetric(build_tree([1]))
    ok3 = s3 is True
    print(f"  [1]                  -> {s3}  期望 True  [{'PASS' if ok3 else 'FAIL'}]"); assert ok3
    s4 = is_symmetric(build_tree([]))
    ok4 = s4 is True
    print(f"  []                   -> {s4}  期望 True  [{'PASS' if ok4 else 'FAIL'}]"); assert ok4

    print("\n第 52 题：路径总和（LeetCode 112）")
    p_tree = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
    h1 = has_path_sum(p_tree, 22)
    ok1 = h1 is True
    print(f"  [5,4,8,11,..],sum=22 -> {h1}  期望 True  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    h2 = has_path_sum(build_tree([1, 2, 3]), 5)
    ok2 = h2 is False
    print(f"  [1,2,3],sum=5        -> {h2}  期望 False [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    h3 = has_path_sum(build_tree([1, 2]), 1)
    ok3 = h3 is False
    print(f"  [1,2],sum=1          -> {h3}  期望 False [{'PASS' if ok3 else 'FAIL'}]"); assert ok3
    h4 = has_path_sum(build_tree([1, 2]), 3)
    ok4 = h4 is True
    print(f"  [1,2],sum=3          -> {h4}  期望 True  [{'PASS' if ok4 else 'FAIL'}]"); assert ok4

    print("\n第 53 题：翻转二叉树（LeetCode 226）")
    inv = invert_tree(build_tree([4, 2, 7, 1, 3, 6, 9]))
    ok1 = to_level(inv) == [4, 7, 2, 9, 6, 3, 1]
    print(f"  [4,2,7,1,3,6,9]      -> {to_level(inv)}  期望 [4,7,2,9,6,3,1]  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    inv2 = invert_tree(build_tree([]))
    ok2 = to_level(inv2) == []
    print(f"  []                   -> {to_level(inv2)}  期望 []  [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    inv3 = invert_tree(build_tree([1]))
    ok3 = to_level(inv3) == [1]
    print(f"  [1]                  -> {to_level(inv3)}  期望 [1]  [{'PASS' if ok3 else 'FAIL'}]"); assert ok3

    print("\n第 54 题：相同的树（LeetCode 100）")
    a1 = is_same_tree(build_tree([1, 2, 3]), build_tree([1, 2, 3]))
    ok1 = a1 is True
    print(f"  [1,2,3] vs [1,2,3]   -> {a1}  期望 True  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    a2 = is_same_tree(build_tree([1, 2]), build_tree([1, None, 2]))
    ok2 = a2 is False
    print(f"  [1,2] vs [1,null,2]  -> {a2}  期望 False [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    a3 = is_same_tree(build_tree([1, 2, 1]), build_tree([1, 1, 2]))
    ok3 = a3 is False
    print(f"  [1,2,1] vs [1,1,2]   -> {a3}  期望 False [{'PASS' if ok3 else 'FAIL'}]"); assert ok3

    print("\n第 55 题：二叉搜索树的最近公共祖先（LeetCode 235）")
    bst = build_tree([6, 2, 8, 0, 4, 7, 9, 3, 5])
    l1 = lowest_common_ancestor_bst(bst, find_node(bst, 2), find_node(bst, 8))
    ok1 = l1.val == 6
    print(f"  p=2,q=8             -> {l1.val if l1 else None}  期望 6   [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    l2 = lowest_common_ancestor_bst(bst, find_node(bst, 2), find_node(bst, 4))
    ok2 = l2.val == 2
    print(f"  p=2,q=4             -> {l2.val if l2 else None}  期望 2   [{'PASS' if ok2 else 'FAIL'}]"); assert ok2

    print("\n第 56 题：二叉树的最近公共祖先（LeetCode 236）")
    bt = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    m1 = lowest_common_ancestor(bt, find_node(bt, 5), find_node(bt, 1))
    ok1 = m1.val == 3
    print(f"  p=5,q=1             -> {m1.val if m1 else None}  期望 3   [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    m2 = lowest_common_ancestor(bt, find_node(bt, 5), find_node(bt, 4))
    ok2 = m2.val == 5
    print(f"  p=5,q=4             -> {m2.val if m2 else None}  期望 5   [{'PASS' if ok2 else 'FAIL'}]"); assert ok2

    print("\n第 57 题：二叉树的右视图（LeetCode 199）")
    r1 = right_side_view(build_tree([1, 2, 3, None, 5, None, 4]))
    ok1 = r1 == [1, 3, 4]
    print(f"  [1,2,3,null,5,null,4]-> {r1}  期望 [1,3,4]  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    r2 = right_side_view(build_tree([1, None, 3]))
    ok2 = r2 == [1, 3]
    print(f"  [1,null,3]          -> {r2}  期望 [1,3]  [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    r3 = right_side_view(build_tree([]))
    ok3 = r3 == []
    print(f"  []                   -> {r3}  期望 []  [{'PASS' if ok3 else 'FAIL'}]"); assert ok3

    print("\n第 58 题：二叉树的锯齿形层序遍历（LeetCode 103）")
    z1 = zigzag_level_order(build_tree([3, 9, 20, None, None, 15, 7]))
    ok1 = z1 == [[3], [20, 9], [15, 7]]
    print(f"  [3,9,20,null,null,15,7] -> {z1}  期望 [[3],[20,9],[15,7]]  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    z2 = zigzag_level_order(build_tree([]))
    ok2 = z2 == []
    print(f"  []                   -> {z2}  期望 []  [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    z3 = zigzag_level_order(build_tree([1]))
    ok3 = z3 == [[1]]
    print(f"  [1]                  -> {z3}  期望 [[1]]  [{'PASS' if ok3 else 'FAIL'}]"); assert ok3

    print("\n第 59 题：将有序数组转换为二叉搜索树（LeetCode 108）")
    b1 = sorted_array_to_bst([-10, -3, 0, 5, 9])
    ok1 = to_level(b1) == [0, -3, 9, -10, None, 5]
    print(f"  [-10,-3,0,5,9]       -> {to_level(b1)}  期望 [0,-3,9,-10,null,5]  [{'PASS' if ok1 else 'FAIL'}]"); assert ok1
    b2 = sorted_array_to_bst([])
    ok2 = to_level(b2) == []
    print(f"  []                   -> {to_level(b2)}  期望 []  [{'PASS' if ok2 else 'FAIL'}]"); assert ok2
    b3 = sorted_array_to_bst([1, 2, 3])
    ok3 = to_level(b3) == [2, 1, 3]
    print(f"  [1,2,3]              -> {to_level(b3)}  期望 [2,1,3]  [{'PASS' if ok3 else 'FAIL'}]"); assert ok3

    print("\n" + "=" * 66)
    print("Day 13 全部 10 题测试通过！（共 58/100 题已完成）")
    print("下次（Day 14）预告：#60 验证二叉搜索树 / #61 二叉树的所有路径 / #62 二叉搜索树中的搜索")
    print("                   / #63 删除二叉搜索树中的节点 / #64 二叉树展开为链表 / #65 从前序与中序构造二叉树")
    print("=" * 66)


if __name__ == "__main__":
    _run_tests()
