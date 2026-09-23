# 最大子数组和 动态规划 cur表示以当前位置i结尾的最大子数组和
# 对于每个数：num可以选择连接前面的数 或者不连接
# cur = max(num, num+cur)
# 最大值每轮维护：ans = max(ans, cur)
def max_sub_array(nums: list[int]) -> int:
    ans = float('-inf')
    cur = 0
    for num in nums:
        cur = max(num, cur+num)
        ans = max(ans, cur)
    return ans

# 合并区间 排序 遍历 将排好序且合并的区间放置到res中 然后res[-1]
# 继续与下一个遍历到的区间比较
# 注意列表是否为空的判断
# 注意append时添加的是副本
def merge(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda x:x[0])
    res = []
    for it in intervals:
        if res and res[-1][1] >= it[0]:
            res[-1][1] = max(res[-1][1], it[1])
        else:
            res.append(it[:])
    return res

# 轮转数组 三次翻转 第一次整体翻转 第二次翻转0~k-1，第三次翻转 k~最后
# 这道题不能使用[::-1]，因为它会创建新列表，不是原地翻转了
# k 可能大于数组长度，先对 n 取模 k %= n。否则会报越界错误
def rotate(nums: list[int], k: int) -> None:
    def fanzhuan(l, r):
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1
    k %= len(nums)
    fanzhuan(0,len(nums)-1)
    fanzhuan(0,k-1)
    fanzhuan(k,len(nums)-1)

# 除自身以外数组的乘积 前后缀乘积 一次左扫一次右扫 left做左侧累积
# right做右侧累积
# res用作返回
def product_except_self(nums: list[int]) -> list[int]:
    left = 1
    n = len(nums)
    res = [1] * n
    for i in range(n):
        res[i] = left
        left *= nums[i]
    right = 1
    for i in range(n-1, -1, -1):
        res[i] *= right
        right *= nums[i]
    return res

# 矩阵置零 首行首列做标记 遍历修改 
# 需要单独记下首行首列是否有零需要清除
# 否则后续不知道是否要清除
# 记住any里面判断是否有零的写法
def set_zeroes(matrix: list[list[int]]) -> None:
    m, n = len(matrix), len(matrix[0])

    row = any(matrix[0][j] == 0 for j in range(n))
    col = any(matrix[i][0] == 0 for i in range(m))
    for i in range(1,m):
        for j in range(1,n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0

    for i in range(1,m):
        for j in range(1,n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0

    if row:
        for j in range(n):
            matrix[0][j] = 0
    if col:
        for i in range(m):
            matrix[i][0] = 0
    
# 螺旋矩阵 边界收缩 逐圈遍历
# top表示当前圈最上面一行的下标 left表示当前圈最左面一列的下标...
# 当left == right时，说明只有一列数据可取，那么这一列数据也是需要读取的
# 故循环条件可以取=
def spiral_order(matrix: list[list[int]]) -> list[int]:
    m, n = len(matrix), len(matrix[0])
    left = top = 0
    right = n - 1
    bottom = m - 1
    res = []
    while left <= right and top <= bottom:
        for j in range(left, right + 1):
            res.append(matrix[top][j])
        top += 1
        for i in range(top, bottom + 1):
            res.append(matrix[i][right])
        right -= 1
        if top <= bottom:
            for j in range(right, left-1, -1):
                res.append(matrix[bottom][j])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top-1, -1):
                res.append(matrix[i][left])
            left += 1
    return res

# 旋转图像 顺时针旋转 = 矩阵上下翻转 + 转置
def rotate_image(matrix: list[list[int]]) -> None:
    n = len(matrix)
    matrix.reverse()
    for i in range(n):
        for j in range(i+1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]







