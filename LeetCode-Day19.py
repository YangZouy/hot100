# -*- coding: utf-8 -*-
"""
========================================================================
LeetCode-Day19.py  ——  AI Agent / 后端开发面试专项（数据结构设计 + 并发编程）
========================================================================

说明：
- 原「必刷 100 题」计划已于 Day18（2026-08-10）全部完结（100/100）。
- 本文件是 100 题之后的【专项补充】，聚焦 AI 应用/Agent 开发岗位面试里
  最爱深挖、但原 100 题偏算法而覆盖较少的两块：
      1) 数据结构设计（手写容器/迭代器，考察对底层结构的理解）
      2) 并发编程（多线程协调，和 Agent 里的 async/并发思想直接对应）
- 每题只给【一种通用解法】，带详细讲解 + ASCII 思路图 + 复杂度 + 面试易错点。
- 直接运行即可验证：  python LeetCode-Day19.py
  全部用例通过会打印 PASS 汇总；任一失败会打印具体断言。

题号与对应 LeetCode 编号：
  #1  LRU 缓存                (146)   设计
  #2  常数时间插入删除随机取  (380)   设计
  #3  数据流的中位数          (295)   设计 / 堆
  #4  Peeking 迭代器          (284)   设计 / 迭代器
  #5  扁平化嵌套列表迭代器    (341)   设计 / 栈
  #6  BST 迭代器              (173)   设计 / 栈
  #7  设计哈希映射            (706)   设计 / 哈希
  #8  按序打印                (1114)  并发 / 多线程
  #9  FooBar 交替打印         (1115)  并发 / 多线程
  #10 FizzBuzz 多线程         (1195)  并发 / 多线程
========================================================================
"""

import threading
import random
import heapq
from collections import OrderedDict


# ======================================================================
# #1  LRU 缓存  (LeetCode 146)
# ======================================================================
"""
题目：实现一个 LRUCache，capacity 给定容量，支持：
    get(key)  -> 命中返回值并把该 key 变成“最近使用”，未命中返回 -1
    put(key,value) -> 写入；若超容量，淘汰“最久没用过”的 key
要求 get/put 都是 O(1)。

为什么重要：AI Agent 里大量用到缓存（embedding 缓存、LLM 响应缓存、
工具结果缓存），LRU 是最经典的淘汰策略。手写 LRU 几乎是后端/Agent 岗标配题。

通用解法（Python 版，最简洁且面试可接受）：
用 collections.OrderedDict —— 它内部就是“哈希表 + 双向链表”，天然支持：
    move_to_end(key)  : 把一个已有 key 移到队尾（标记最近使用）O(1)
    popitem(last=False): 删队首（最久未用）O(1)
    d[key] = value     : 插入/更新 O(1)
对应 LRU 语义：队首 = 最久未用，队尾 = 最近使用。

        capacity = 3，依次操作：
        put(1)  ->  [1]
        put(2)  ->  [1, 2]          (2 在尾=最近)
        put(3)  ->  [1, 2, 3]
        get(1)  ->  1, 把 1 移到尾  [2, 3, 1]
        put(4)  ->  超容量，删队首2  [3, 1, 4]
        get(2)  ->  -1 (已被淘汰)

面试易错点：
- put 已存在的 key 也算“使用”，要先 move_to_end 再赋值（或赋值后再 move）。
- 超出容量时先 popitem 再返回；注意 popitem(last=False) 才删队首（最旧）。
- 进阶：若面试官要求“不能用 OrderedDict”，就得手写双向链表 + 哈希表，
  思路完全一样（哈希存 node，node 之间用 prev/next 串成链表，配 dummy 头尾）。
"""
class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.d = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.d:
            return -1
        self.d.move_to_end(key)        # 命中 -> 标记为最近使用
        return self.d[key]

    def put(self, key: int, value: int) -> None:
        if key in self.d:
            self.d.move_to_end(key)    # 已存在也算使用
        self.d[key] = value
        if len(self.d) > self.cap:
            self.d.popitem(last=False) # 淘汰最久未用的（队首）


# ======================================================================
# #2  常数时间插入、删除和获取随机元素  (LeetCode 380)
# ======================================================================
"""
题目：实现 RandomizedSet：
    insert(val)  -> 不存在则插入返回 True，已存在返回 False
    remove(val)  -> 存在则删除返回 True，不存在返回 False
    getRandom()  -> 等概率随机返回一个元素
要求三个操作平均 O(1)。

通用解法：数组 + 哈希表 双结构配合
    arr        : 存所有元素（保证 O(1) 随机取：random.choice(arr)）
    val_to_idx : val -> 在 arr 中的下标（保证 O(1) 查/删）
关键技巧在 remove：不能 array.pop(index) 因为中间删除是 O(n)。
做法：把“要删的元素”和“数组最后一个元素”交换位置，然后 pop 末尾（O(1)），
同时更新哈希表里“最后一个元素”的新下标。

        insert(1) insert(2) insert(3)
        arr = [1, 2, 3]   map = {1:0, 2:1, 3:2}
        remove(2):
            末尾是 3，把 arr[1] 换成 3 -> arr=[1,3]
            更新 map[3]=1，删 map[2] -> map={1:0,3:1}
            pop 末尾 -> arr=[1,3]   ✅ O(1)

面试易错点：
- remove 时“交换到末尾再 pop”，记得同步更新被挪动那个元素的哈希值。
- getRandom 用 random.choice(arr)，必须基于数组而不是字典（字典无序且不可索引）。
"""
class RandomizedSet:
    def __init__(self):
        self.arr = []
        self.val_to_idx = {}

    def insert(self, val: int) -> bool:
        if val in self.val_to_idx:
            return False
        self.val_to_idx[val] = len(self.arr)
        self.arr.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.val_to_idx:
            return False
        idx = self.val_to_idx[val]
        last = self.arr[-1]
        # 把末尾元素搬到 idx 位置，再删末尾
        self.arr[idx] = last
        self.val_to_idx[last] = idx
        self.arr.pop()
        del self.val_to_idx[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.arr)


# ======================================================================
# #3  数据流的中位数  (LeetCode 295)
# ======================================================================
"""
题目：MedianFinder 支持 addNum(num) 不断加入数字，findMedian() 返回当前
已加入数字的中位数。要求高效（不能每次排序）。

通用解法：双堆（大小顶堆）
    小顶堆 hi   : 存较大的一半（堆顶 = 这一半里最小的）
    大顶堆 lo   : 存较小的一半（用“负数”模拟，堆顶 = 这一半里最大的）
    维持不变式：len(lo) == len(hi) 或 len(lo) == len(hi)+1
    中位数 = 总数为奇时取 -lo[0]；为偶时取 (-lo[0] + hi[0]) / 2

        add 5 -> lo=[-5]        hi=[]
        add 2 -> lo=[-5]        hi=[2]      (2 进 hi 后失衡，弹回 lo 修平衡)
        add 3 -> lo=[-5,-3]     hi=[2]
        中位数 = -lo[0] = 3  ✅  (序列 2,3,5 中位数 3)

插入流程（每来一个数）：
    1) 先压进 lo（取负），再把 lo 堆顶弹到 hi  -> 保证新数先在大堆
    2) 若 hi 比 lo 多，把 hi 堆顶弹回 lo      -> 维持 lo 不比 hi 少超过 1

面试易错点：
- Python 没有大顶堆，用“负值” trick：heappush(lo, -x) 表示大顶堆。
- 平衡条件写反是最常见 bug：目标是 len(lo) >= len(hi)，且差值不超过 1。
- 偶数时中位数要 /2.0，注意浮点。
"""
class MedianFinder:
    def __init__(self):
        self.lo = []   # 大顶堆（存负数）
        self.hi = []   # 小顶堆

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2.0


# ======================================================================
# #4  Peeking Iterator  (LeetCode 284)
# ======================================================================
"""
题目：给定只提供 hasNext()/next() 的迭代器，包装出一个支持 peek() 的迭代器：
    peek()  -> 返回下一个元素，但不“消耗”它（再调用 next 仍拿到同一个）
    next()  -> 正常前进
    hasNext()-> 是否还有

通用解法：缓存一个“预读”元素
    用 _peeked 标记是否已预读，_next_val 存预读的值。
    - peek()  : 若没预读过，就调用底层 next() 存起来；返回它。
    - next()  : 若已预读，直接返回并清空标记；否则调底层 next()。
    - hasNext(): 已预读 或 底层还有  -> 都算有。

        it: [1, 2, 3]
        peek() -> 调底层 next() 得到 1，缓存，返回 1   (it 指针没动)
        peek() -> 已有缓存 1，直接返回 1
        next() -> 返回缓存 1，清空缓存
        next() -> 没缓存，调底层得到 2

面试易错点：
- peek 多次只能预读一次，必须靠 _peeked 标记防重复消费。
- hasNext 在“已预读但未消费”时也要返回 True。
"""
class PeekingIterator:
    def __init__(self, iterator):
        self._it = iterator
        self._peeked = False
        self._val = None

    def peek(self):
        if not self._peeked:
            self._val = self._it.next()
            self._peeked = True
        return self._val

    def next(self):
        if not self._peeked:
            return self._it.next()
        self._peeked = False
        return self._val

    def hasNext(self):
        return self._peeked or self._it.hasNext()


# 底层迭代器（用于自测，模拟 LeetCode 的 Iterator 接口）
class _ListIterator:
    def __init__(self, data):
        self.data = data
        self.i = 0
    def hasNext(self):
        return self.i < len(self.data)
    def next(self):
        v = self.data[self.i]
        self.i += 1
        return v


# ======================================================================
# #5  扁平化嵌套列表迭代器  (LeetCode 341)
# ======================================================================
"""
题目：输入是“嵌套整数”列表，每个元素要么是整数，要么是（嵌套的）列表。
实现一个迭代器，按深度优先顺序逐个吐出所有整数。
例如 [[1,1],2,[1,1]] -> 1,1,2,1,1

通用解法：用栈（Stack），从右往左压栈，保证弹出顺序是从左到右。
    关键：只有当“栈顶不是整数”时才展开——这就是惰性展开（lazy），
    只在需要 next 时才把列表摊开，省内存、也符合迭代器语义。

        init: 栈里(从底到顶) = [ [1,1], 2, [1,1] ]  (逆序压入)
        调用 next:
          栈顶 [1,1] 不是整数 -> 弹出，逆序压入 1,1 -> 栈顶变 1(整数)
          弹出 1 ... 如此递归，直到遇到整数才返回

面试易错点：
- 必须在 next()/hasNext() 里“先展开到栈顶是整数”再取值，不能初始化时全摊平。
- 展开时“逆序压回栈”这一步最容易漏，漏了顺序就反了。
"""
class NestedIterator:
    def __init__(self, nestedList):
        self.stack = []
        for item in reversed(nestedList):   # 逆序压栈 -> 弹出即从左到右
            self.stack.append(item)

    def _normalize(self):
        # 把栈顶所有“列表”摊开，直到栈顶是整数或无元素
        while self.stack and not self.stack[-1].isInteger():
            top = self.stack.pop()
            for item in reversed(top.getList()):
                self.stack.append(item)

    def next(self):
        self._normalize()
        return self.stack.pop().getInteger()

    def hasNext(self):
        self._normalize()
        return bool(self.stack)


# 嵌套整数占位类（LeetCode 提供 NestedInteger 接口，这里自测用）
class _NI:
    def __init__(self, val=None, lst=None):
        if lst is not None:
            self._is_int = False
            self._lst = lst
        else:
            self._is_int = True
            self._val = val
    def isInteger(self):
        return self._is_int
    def getInteger(self):
        return self._val
    def getList(self):
        return self._lst


# ======================================================================
# #6  BST 迭代器（中序遍历） (LeetCode 173)
# ======================================================================
"""
题目：给一棵二叉搜索树，实现一个迭代器，按“中序（升序）”逐个返回节点值，
next()/hasNext() 都是 O(1)（摊还），且只用 O(h) 空间（h=树高）。

通用解法：迭代式中序遍历 + 栈（惰性）
    初始化：把根节点一路向左压栈（模拟递归“先到最左”）。
    next()：弹出栈顶（当前最小），若该节点有右子树，把右子树一路向左压栈。
    hasNext()：栈非空即还有。

        BST:       3
                 /   \
                1     4
                 \
                  2
        初始化栈: [3,1]        (1 在最顶=当前最小)
        next()->1, 1 有右孩2 -> 压 2 -> 栈[3,2]
        next()->2
        next()->3, 3 有右孩4 -> 压4 -> 栈[4]
        next()->4   返回 1,2,3,4  ✅ 升序

面试易错点：
- 是“摊还 O(1)”不是“严格 O(1)”：一次 next 可能压一串左链，但每条边最多
  进出栈一次，均摊下来是 O(1)。
- 别在初始化时把整棵树展开成数组（那要 O(n) 空间，不符合要求）。
"""
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class BSTIterator:
    def __init__(self, root: TreeNode):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        node = self.stack.pop()
        self._push_left(node.right)   # 右子树的最左链
        return node.val

    def hasNext(self) -> bool:
        return bool(self.stack)


# ======================================================================
# #7  设计哈希映射  (LeetCode 706)
# ======================================================================
"""
题目：不借助语言自带 dict，实现一个 MyHashMap：put(key,value)/get(key)/remove(key)。
key,value 都是非负整数。

通用解法：数组分桶 + 链地址法（拉链）
    buckets = [[] for _ in range(SIZE)]，SIZE 取一个质数/固定值（如 1000）。
    _hash(key) = key % SIZE -> 定位到某个桶。
    每个桶里存 [(k,v), (k,v), ...]，冲突时就往桶里追加，查/删时线性扫桶。
    （真实哈希表还会扩容 rehash，面试一般不用写，理解分桶思想即可）

        SIZE=1000, put(1,10) -> 桶1: [(1,10)]
        put(1001,99) -> 1001%1000=1 -> 桶1: [(1,10),(1001,99)]  (哈希冲突，拉链)
        get(1001) -> 扫桶1找到 1001 -> 99

面试易错点：
- 冲突处理：同一个桶里可能有多个 key，必须用“key 相等”判断，不能只看桶。
- put 已存在的 key 要“更新”而不是重复插入。
- remove 用 del 按索引删，避免遍历错位。
"""
class MyHashMap:
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key):
        return key % self.size

    def put(self, key: int, value: int) -> None:
        h = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[h]):
            if k == key:
                self.buckets[h][i] = (key, value)
                return
        self.buckets[h].append((key, value))

    def get(self, key: int) -> int:
        h = self._hash(key)
        for k, v in self.buckets[h]:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        h = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[h]):
            if k == key:
                del self.buckets[h][i]
                return


# ======================================================================
# #8  按序打印  (LeetCode 1114)  —— 并发 / 多线程
# ======================================================================
"""
题目：三个线程分别调用 first/second/third，要求无论线程以什么顺序启动，
最终打印顺序一定是 first -> second -> third。

为什么重要：这是并发协调的“Hello World”，对应 Agent 里“步骤必须按
依赖顺序执行”（如先检索再生成）。思想完全适用于 async 的 await 顺序。

通用解法：用两个 threading.Event 串成“链条”
    e1: first 完成后 set -> second 才能过
    e2: second 完成后 set -> third 才能过
    first 不需要等，直接执行。

        线程乱序启动:  third等e2, second等e1, first直接跑
        first 跑完 -> e1.set() -> second 放行 -> e2.set() -> third 放行
        结果永远 "firstsecondthird"

面试易错点：
- 不要用 time.sleep 强行排序（靠运气、不严谨）。
- Event 比 Lock 更契合“一次性放行”语义；这里用 wait/set 即可。
"""
class Foo:
    def __init__(self):
        self.e1 = threading.Event()
        self.e2 = threading.Event()

    def first(self, printFirst):
        printFirst()
        self.e1.set()

    def second(self, printSecond):
        self.e1.wait()
        printSecond()
        self.e2.set()

    def third(self, printThird):
        self.e2.wait()
        printThird()


# ======================================================================
# #9  FooBar 交替打印  (LeetCode 1115)  —— 并发 / 多线程
# ======================================================================
"""
题目：两个线程，foo 调用 n 次、bar 调用 n 次，要求输出严格交替 foo bar foo bar...
（共 2n 个字符），不能出现 foo foo 或 bar bar。

通用解法：两把锁，初始时“锁住 bar”那把，形成交替闸门
    foo_lock  : 控制 foo 能否打印
    bar_lock  : 控制 bar 能否打印，初始化时先 acquire() 锁住
    流程：foo 拿到 foo_lock -> 打印 -> 释放 bar_lock（放行 bar）
          bar 拿到 bar_lock -> 打印 -> 释放 foo_lock（放行 foo）
    如此你放我、我放你，天然交替。

        foo_lock=开, bar_lock=锁
        foo打印"f" -> 开bar_lock -> bar打印"b" -> 开foo_lock -> ...
        输出: f b f b f b ...

面试易错点：
- 必须“先初始化就锁住 bar_lock”，否则可能两个线程同时冲进来乱序。
- 用两把锁互锁比一把锁 + 状态变量更不易写出 bug。
"""
class FooBar:
    def __init__(self, n):
        self.n = n
        self.foo_lock = threading.Lock()
        self.bar_lock = threading.Lock()
        self.bar_lock.acquire()   # bar 先等着，等 foo 释放

    def foo(self, printFoo):
        for _ in range(self.n):
            self.foo_lock.acquire()
            printFoo()
            self.bar_lock.release()

    def bar(self, printBar):
        for _ in range(self.n):
            self.bar_lock.acquire()
            printBar()
            self.foo_lock.release()


# ======================================================================
# #10  FizzBuzz 多线程  (LeetCode 1195)  —— 并发 / 多线程
# ======================================================================
"""
题目：四个线程分别负责：
    fizz()     打印能被 3 整除但不能被 5 整除的数
    buzz()     打印能被 5 整除但不能被 3 整除的数
    fizzbuzz() 打印能被 15 整除的数
    number()   打印其余数
它们共享 1..n，要求最终拼出的字符串和单线程 FizzBuzz 完全一致。

通用解法：一个共享计数器 i + 一把 Condition（条件变量）
    四个线程循环：i 未越界时，按“自己负责的规则”判断当前 i 是否轮到自己；
    轮到自己就打印、i+=1、notify_all() 唤醒其他线程重新判断；
    不轮到自己就 cv.wait() 让出，等别人推进后再来抢。
    （Condition 比裸 Lock 忙等优雅：wait 时线程挂起，不空转）

        i=1 -> number 负责 -> 打印"1", i=2
        i=2 -> number -> "2"
        i=3 -> fizz -> "f"  (3%3==0且不被5整除)
        i=4 -> number -> "4"
        i=5 -> buzz -> "B"
        ... i=15 -> fizzbuzz -> "F"

面试易错点：
- 判断“是否轮到自己”必须用 while 循环（被唤醒后要重新检查，可能条件变了）。
- 打印后必须 notify_all，否则其他线程可能在 wait 上永久挂起（死锁）。
- 越界判断（i>n）要放在 while 循环里，确保线程能正常退出。
"""
class FizzBuzz:
    def __init__(self, n):
        self.n = n
        self.i = 1
        self.cv = threading.Condition()

    def _step(self, predicate):
        with self.cv:
            while True:
                if self.i > self.n:
                    return
                if predicate(self.i):
                    return  # 轮到我了，调用方负责打印并 i+=1、notify
                self.cv.wait()

    def fizz(self, printFizz):
        while True:
            with self.cv:
                if self.i > self.n:
                    return
                while self.i <= self.n and not (self.i % 3 == 0 and self.i % 5 != 0):
                    self.cv.wait()
                if self.i > self.n:
                    return
                printFizz()
                self.i += 1
                self.cv.notify_all()

    def buzz(self, printBuzz):
        while True:
            with self.cv:
                if self.i > self.n:
                    return
                while self.i <= self.n and not (self.i % 5 == 0 and self.i % 3 != 0):
                    self.cv.wait()
                if self.i > self.n:
                    return
                printBuzz()
                self.i += 1
                self.cv.notify_all()

    def fizzbuzz(self, printFizzBuzz):
        while True:
            with self.cv:
                if self.i > self.n:
                    return
                while self.i <= self.n and not (self.i % 15 == 0):
                    self.cv.wait()
                if self.i > self.n:
                    return
                printFizzBuzz()
                self.i += 1
                self.cv.notify_all()

    def number(self, printNumber):
        while True:
            with self.cv:
                if self.i > self.n:
                    return
                while self.i <= self.n and (self.i % 3 == 0 or self.i % 5 == 0):
                    self.cv.wait()
                if self.i > self.n:
                    return
                printNumber()
                self.i += 1
                self.cv.notify_all()


# ======================================================================
#  自测区：直接运行本文件会跑下面所有用例，全过即验证正确
# ======================================================================
def _run_tests():
    passed = 0
    failed = 0

    def check(name, cond):
        nonlocal passed, failed
        if cond:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            failed += 1
            print(f"  [FAIL] {name}")

    # ---- #1 LRU ----
    print("\n[#1 LRU 缓存 146]")
    lc = LRUCache(2)
    lc.put(1, 1); lc.put(2, 2)
    check("get(1)==1", lc.get(1) == 1)
    lc.put(3, 3)                      # 淘汰 key2
    check("get(2)==-1 (被淘汰)", lc.get(2) == -1)
    lc.put(4, 4)                      # 淘汰 key1
    check("get(1)==-1 (被淘汰)", lc.get(1) == -1)
    check("get(3)==3", lc.get(3) == 3)
    check("get(4)==4", lc.get(4) == 4)

    # ---- #2 RandomizedSet ----
    print("\n[#2 常数时间集合 380]")
    rs = RandomizedSet()
    check("insert(1)", rs.insert(1) is True)
    check("remove(2) 不存在", rs.remove(2) is False)
    check("insert(2)", rs.insert(2) is True)
    check("getRandom 在集合内", rs.getRandom() in (1, 2))
    check("remove(1)", rs.remove(1) is True)
    check("insert(2) 已存在", rs.insert(2) is False)
    check("getRandom==2", rs.getRandom() == 2)
    # 验证删除后随机仍只命中剩余元素
    ok = all(rs.getRandom() == 2 for _ in range(50))
    check("删除后只命中剩余元素", ok)

    # ---- #3 MedianFinder ----
    print("\n[#3 数据流中位数 295]")
    mf = MedianFinder()
    mf.addNum(1);  check("中位数(1)=1", abs(mf.findMedian() - 1) < 1e-9)
    mf.addNum(2);  check("中位数(1,2)=1.5", abs(mf.findMedian() - 1.5) < 1e-9)
    mf.addNum(3);  check("中位数(1,2,3)=2", abs(mf.findMedian() - 2) < 1e-9)
    mf.addNum(4);  check("中位数(1..4)=2.5", abs(mf.findMedian() - 2.5) < 1e-9)
    mf.addNum(5);  check("中位数(1..5)=3", abs(mf.findMedian() - 3) < 1e-9)

    # ---- #4 PeekingIterator ----
    print("\n[#4 Peeking 迭代器 284]")
    pit = PeekingIterator(_ListIterator([1, 2, 3]))
    check("hasNext", pit.hasNext() is True)
    check("peek==1", pit.peek() == 1)
    check("peek 再 peek 仍 ==1", pit.peek() == 1)
    check("next==1", pit.next() == 1)
    check("next==2", pit.next() == 2)
    check("peek==3", pit.peek() == 3)
    check("next==3", pit.next() == 3)
    check("hasNext False", pit.hasNext() is False)

    # ---- #5 NestedIterator ----
    print("\n[#5 扁平化嵌套列表 341]")
    nested = [_NI(1), _NI(lst=[_NI(2), _NI(3)]), _NI(4)]
    nit = NestedIterator(nested)
    out = []
    while nit.hasNext():
        out.append(nit.next())
    check("扁平化 [1,2,3,4]", out == [1, 2, 3, 4])
    nested2 = [_NI(lst=[_NI(lst=[_NI(1)]), _NI(2)]), _NI(3)]
    nit2 = NestedIterator(nested2)
    out2 = [nit2.next() for _ in range(3)]
    check("深层嵌套 [1,2,3]", out2 == [1, 2, 3])

    # ---- #6 BSTIterator ----
    print("\n[#6 BST 迭代器 173]")
    root = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))
    bit = BSTIterator(root)
    out = []
    while bit.hasNext():
        out.append(bit.next())
    check("中序升序 [1,2,3,4]", out == [1, 2, 3, 4])

    # ---- #7 MyHashMap ----
    print("\n[#7 设计哈希映射 706]")
    hm = MyHashMap()
    hm.put(1, 1); hm.put(2, 2)
    check("get(1)==1", hm.get(1) == 1)
    hm.put(1, 10); check("put 更新 -> get(1)==10", hm.get(1) == 10)
    check("get(3)==-1", hm.get(3) == -1)
    hm.remove(2);  check("remove(2) -> get(2)==-1", hm.get(2) == -1)
    hm.put(1001, 99); check("哈希冲突桶 get(1001)==99", hm.get(1001) == 99)

    # ---- #8 Foo 按序打印 ----
    print("\n[#8 按序打印 1114]")
    foo = Foo()
    out = []
    out_lock = threading.Lock()
    def mk(ch):
        def p():
            with out_lock:
                out.append(ch)
        return p
    t3 = threading.Thread(target=foo.third, args=(mk('t'),))
    t1 = threading.Thread(target=foo.first, args=(mk('f'),))
    t2 = threading.Thread(target=foo.second, args=(mk('s'),))
    t3.start(); t1.start(); t2.start()   # 故意乱序启动
    t3.join(); t1.join(); t2.join()
    check("顺序永远是 f-s-t", ''.join(out) == 'fst')

    # ---- #9 FooBar 交替 ----
    print("\n[#9 FooBar 交替 1115]")
    fb = FooBar(3)
    out = []
    fb_lock = threading.Lock()
    def pf():
        with fb_lock: out.append('f')
    def pb():
        with fb_lock: out.append('b')
    a = threading.Thread(target=fb.foo, args=(pf,))
    b = threading.Thread(target=fb.bar, args=(pb,))
    a.start(); b.start(); a.join(); b.join()
    # 注意：回调里只追加了 'f' 和 'b'，故期望是 'fb' 交替 3 次
    check("交替 fb*3", ''.join(out) == 'fb' * 3)

    # ---- #10 FizzBuzz 多线程 ----
    print("\n[#10 FizzBuzz 多线程 1195]")
    def expected_fb(n):
        s = ''
        for i in range(1, n + 1):
            if i % 15 == 0: s += 'F'
            elif i % 3 == 0: s += 'f'
            elif i % 5 == 0: s += 'B'
            else: s += str(i)
        return s
    fzbz = FizzBuzz(15)
    out = []
    fb_lock = threading.Lock()
    def pf():
        with fb_lock: out.append('f')
    def pB():
        with fb_lock: out.append('B')
    def pF():
        with fb_lock: out.append('F')
    def pn():
        with fb_lock: out.append(str(fzbz.i))   # 打印瞬间读取当前 i
    ts = [
        threading.Thread(target=fzbz.fizz, args=(pf,)),
        threading.Thread(target=fzbz.buzz, args=(pB,)),
        threading.Thread(target=fzbz.fizzbuzz, args=(pF,)),
        threading.Thread(target=fzbz.number, args=(pn,)),
    ]
    for t in ts: t.start()
    for t in ts: t.join()
    check("多线程 FizzBuzz==单线程", ''.join(out) == expected_fb(15))

    print("\n" + "=" * 56)
    print(f"测试结果：{passed} 通过 / {failed} 失败  （共 {passed+failed} 项）")
    print("=" * 56)
    if failed:
        print("存在失败用例，请检查上方 [FAIL] 项。")
    else:
        print("全部用例通过 ✅  直接 python LeetCode-Day19.py 即可复现。")


if __name__ == "__main__":
    _run_tests()
