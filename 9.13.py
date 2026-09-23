# 移动零 双指针
def move_zeroes(nums: list[int]) -> None:
    p0 = 0
    for cur in range(len(nums)):
        if nums[cur] != 0:
            nums[p0], nums[cur] = nums[cur], nums[p0]
            p0 += 1

# 合并两个有序数组
def merge_sorted_array(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    k = m + n - 1
    i, j = m-1, n-1
    while i >=0 and j >= 0:
        if nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
    while j >= 0:
        nums1[k] = nums2[j]
        k -= 1
        j -= 1

# 相交链表 是否有环 快慢指针 相同时有环
def get_intersection_node(headA: "ListNode | None", headB: "ListNode | None") -> "ListNode | None":
    fast, slow = headA, headB
    while fast is not slow:
        fast = fast.next if fast else headB
        slow = slow.next if slow else headA
    return fast

# 反转链表 cur是正在处理的节点 prev是已经反转好部分的头
def reverse_list(head: "ListNode | None") -> "ListNode | None":
    pre = None
    cur = head
    while cur:
        nxt = cur.next
        cur.next = pre
        pre = cur
        cur = nxt
    return pre

# 回文链表 辅助栈或者快慢指针+反转后半段
def is_palindrome(head: "ListNode | None") -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    def reverse(head):
        pre = None
        cur = head
        while cur:
            nxt = cur.next
            cur.next = pre
            pre = cur
            cur = nxt
    se = reverse(slow.next if fast else slow)
    p = head
    while se:
        if p.val != se.val:
            return False
        p = p.next
        se = se.next
    return True

# 环形链表
def has_cycle(head: "ListNode | None") -> bool:
    fast = slow = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

# 合并两个有序链表
def merge_two_lists(l1: "ListNode | None", l2: "ListNode | None") -> "ListNode | None":
    dummy = ListNode(0)
    p = dummy
    while l1 and l2:
        if l1.val < l2.val:
            p.next = l1
            l1 = l1.next
        else:
            p.next = l2
            l2 = l2.next
        p = p.next
    p.next = l1 if l1 else l2
    return dummy.next

# 二叉树的中序遍历 1、递归 2、栈
def inorder_traversal(root: "TreeNode | None") -> list[int]:
    res = []
    cur = root
    s = []
    while cur or s:
        while cur:
            s.append(cur)
            cur = cur.left
        cur = s.pop()
        res.append(cur)
        cur = cur.right
    return res

# 二叉树的最大深度 层序遍历 递归
def max_depth(root: "TreeNode | None") -> int:
    if not root:
        return 0
    return max(max_depth(root.left), max_depth(root.right)) + 1

# 翻转二叉树 递归交换左右子树 天然后序 对于每个节点 先把它的左右子树分别翻转好
def invert_tree(root: "TreeNode | None") -> "TreeNode | None":
    if not root:
        return 
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root

# 对称二叉树 递归 
def is_symmetric(root: "TreeNode | None") -> bool:
    def mirror(a,b):
        if not a and not b:
            return True
        if not a or not b:
            return False
        return a.val == b.val and mirror(a.right, b.left) and mirror(a.left, b.right)
    return mirror(root, root)




    







        

        



        


