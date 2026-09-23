# 搜索二维矩阵 右上角开始 往左走就是缩小 往下走就是增大
def search_matrix_ii(matrix: list[list[int]], target: int) -> bool:
    m, n = len(matrix), len(matrix[0])
    i = 0
    j = n - 1
    while i<m and j>=0:
        if matrix[i][j] < target:
            i += 1
        elif matrix[i][j] > target:
            j -= 1
        else:
            return True
    return False

# 环形链表Ⅱ 判断有环 快慢指针 快慢指向同一个节点时 p指针指向头节点
# 当p指针与慢指针同时移动到相同节点时，说明有环，且相遇节点就是环的入口节点
def detect_cycle(head: "ListNode | None") -> "ListNode | None":
    fast = slow = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            p = head
            while p is not slow:
                p = p.next
                slow = slow.next
            return p
    return None

# 两数相加 哑节点 + 模拟进位相加
def add_two_numbers(l1: "ListNode | None", l2: "ListNode | None") -> "ListNode | None":
    dummy = ListNode(0)
    p = dummy
    carry = 0
    while l1 or l2 or carry:
        sum = (l1.val if l1 else 0) + (l2.val if l2 else 0) + carry
        p.next = ListNode(sum % 10)
        carry = sum // 10
        p = p.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next

# 删除链表的倒数第N个节点 快慢指针 快指针先走N步，然后快慢指针一起走
# 当快指针指向末尾时，慢指针刚好指向需要删除的指针前
def remove_nth_from_end(head: "ListNode | None", n: int) -> "ListNode | None":
    dummy = ListNode(0,head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next

# 两两交换链表中的节点 pre指向上一轮结束时的结束节点
# a指向当前交换的节点1 b指向待交换节点2 nxt指向下一轮开始的节点
def swap_pairs(head: "ListNode | None") -> "ListNode | None":
    dummy = ListNode(0, head)
    pre = dummy
    while pre.next and pre.next.next:
        a = pre.next
        b = a.next
        nxt = b.next
        # 交换
        a.next = nxt
        b.next = a
        pre.next = b
        pre = a
    return dummy.next

# 随机链表的复制 两次遍历 第一次存储map，key：原节点 value：新节点
# 第二次遍历 原节点的random和next关系拷贝到新节点中
# 记得p跳转到next中
def copy_random_list(head: "RandomListNode | None") -> "RandomListNode | None":
    d = {}
    p = head
    while p:
        d[p] = RandomListNode(p.val)
        p = p.next
    p = head
    while p:
        d[p].next = d.get(p.next)
        d[p].random = d.get(p.random)
        p = p.next
    return d[head]

# 排序列表 归并排序 递归 二分，左右两边递归，递归后将左右两边循环合并
# 二分找中点时，fast = head.next开始，这样结束循环时中点刚好在slow.next
def sort_list(head: "ListNode | None") -> "ListNode | None":
    if not head or not head.next:
        return head
    slow = head
    fast = head.next
    while fast and fast.next:
        fast = fast.next.next
        slow = slow.next
    p = head
    mid = slow.next
    slow.next = None
    left = sort_list(head)
    right = sort_list(mid)
    dummy = ListNode(0)
    node = dummy
    while left and right:
        if left.val < right.val:
            node.next = left
            left = left.next
        else:
            node.next = right
            right = right.next
        node = node.next
    node.next = left or right
    return dummy.next

    

        





    


        
        

    