# =============================================================
# LeetCode 面试手撕 · Day 20（AI Application / Agent 开发专项）
# =============================================================
# 说明：
#   原「必刷 100 题」已于 Day18 完结（Day1-9 每日 2 题、Day10-17 每日 10 题、
#   Day18 收官合并 K 个升序链表），Day19 补充了手写容器 + 并发编程。
#   本文件（Day20）是 100 题之外的【AI 应用 / Agent 开发岗专项】，聚焦经典 LeetCode
#   没覆盖、但 AI 工程师面试极爱手撕的「工程能力题」：
#     调 LLM 的健壮性（重试/限流）、RAG 检索、Prompt 模板、解析模型输出、
#     多 Agent 协作（事件总线）、配置合并……
#   每题：思路讲解 + ASCII 流程图 + 一种通用解法（可运行）+ 复杂度 + 自测。
#   运行：  python LeetCode-Day20.py   （全部断言通过即验证正确）
# =============================================================

import time
import math
import re
import heapq
import urllib.parse


# =============================================================
# 第 1 题：指数退避重试（Retry with Exponential Backoff）
# 场景：调用 LLM / 外部 API 经常偶发失败（限流 429、网络抖动），
#       需要「失败就重试，且越重试等得越久 + 加随机抖动」避免惊群。
# =============================================================
# 【思路讲解】
# 核心三件事：
#   1) 最多重试 max_retries 次（首次调用算第 0 次，所以循环 range(max_retries+1)）。
#   2) 每次失败后等待时间 = base_delay * 2**attempt（指数增长：0.1s → 0.2s → 0.4s）。
#   3) 加一点随机 jitter，防止多个请求在同一时刻一起重试（「惊群效应」）。
# 注意：最后一次失败后【不再 sleep】，直接抛出最后一个异常，让调用方感知失败。
#
# 【流程图】
#   for attempt in 0..max_retries:
#        try: return func()          ← 成功就直接返回
#        except:
#            if attempt == max_retries: break   ← 最后一次，不睡了，准备抛异常
#            sleep(base * 2**attempt + jitter)  ← 指数退避 + 抖动
#   raise 最后一个异常
#
# 【代码】
def with_retry(func, max_retries=3, base_delay=0.1, jitter=0.05):
    last_exc = None
    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as e:           # 捕获所有异常，统一重试
            last_exc = e
            if attempt == max_retries:    # 已经是最后一次，不再等待
                break
            delay = base_delay * (2 ** attempt) + random_uniform(0, jitter)
            time.sleep(delay)
    raise last_exc                       # 全部失败，把最后的异常抛出去


def random_uniform(low, high):
    """极简随机，避免引入额外依赖；面试里直接写 random.uniform 即可。"""
    import random
    return random.uniform(low, high)


# 【复杂度】时间：最坏 O(max_retries) 次调用；空间 O(1)。
# 【面试易错点】① 把 max_retries 当成「总调用次数」导致少调一次；
#              ② 忘记在最后一次 break，多睡一次还抛异常；
#              ③ 重试时把「成功返回值」也 sleep 了（应 try 里直接 return）。


# =============================================================
# 第 2 题：令牌桶限流器（Token Bucket Rate Limiter）
# 场景：限制对 LLM 的 QPS（比如最多 5 次/秒），超了就拒绝 / 排队。
# =============================================================
# 【思路讲解】
# 令牌桶模型：想象一个桶，每秒往里放 refill_rate 个令牌，最多装 capacity 个。
#   每次请求来：先把「这段时间该补的令牌」算上（懒更新，不用后台线程），
#   再看桶里够不够；够就扣 1 个令牌放行，不够就拒绝。
# 懒更新关键：用 last 记录上次补令牌的时间，补的量 = (now - last) * refill_rate。
#
# 【流程图】
#   allow():
#       now = now()
#       tokens += (now - last) * refill_rate   ← 先补桶
#       tokens  = min(tokens, capacity)        ← 不超过容量
#       last = now
#       if tokens >= 1: tokens -= 1; return True
#       else: return False
#
# 【代码】
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity          # 桶容量（最大令牌数）
        self.refill_rate = refill_rate    # 每秒补充的令牌数
        self.tokens = float(capacity)     # 初始满桶
        self.last = time.time()

    def allow(self, n=1):
        now = time.time()
        # 1) 懒补充：按流逝时间把令牌加回来
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.refill_rate)
        self.last = now
        # 2) 够就放行
        if self.tokens >= n:
            self.tokens -= n
            return True
        return False


# 【复杂度】时间 O(1)；空间 O(1)。
# 【面试易错点】① 忘记 min 截断导致令牌可无限累积；
#              ② 用后台线程补令牌（过度设计，面试用懒更新即可）；
#              ③ 多进程/多线程下 self.tokens 非线程安全（面试先说「单线程 / 加锁」）。


# =============================================================
# 第 3 题：带过期时间的缓存（TTL Cache）
# 场景：缓存 LLM 回答 / Embedding 向量，过一段时间自动失效，省 token。
# =============================================================
# 【思路讲解】
# 最简方案：字典存 {key: (value, expire_at)}，expire_at 是绝对过期时间戳。
#   get 时：没过期就返回值；过期了就顺手删掉返回 None（惰性淘汰）。
#   set 时：ttl 为 None 表示永不过期（expire_at=None）。
# 为什么存「绝对时间」而不是「剩余秒数」？因为绝对时间不依赖后台定时清理。
#
# 【流程图】
#   set(k,v,ttl):  expire = None if ttl is None else now+ttl
#                  store[k] = (v, expire)
#   get(k):
#       if k in store:
#           v, exp = store[k]
#           if exp is None or exp > now: return v
#           del store[k]                 ← 惰性淘汰
#       return None
#
# 【代码】
class TTLCache:
    def __init__(self):
        self.store = {}                  # key -> (value, expire_at | None)

    def get(self, key):
        if key in self.store:
            value, expire = self.store[key]
            if expire is None or expire > time.time():
                return value
            del self.store[key]          # 惰性淘汰过期项
        return None

    def set(self, key, value, ttl=None):
        expire = None if ttl is None else time.time() + ttl
        self.store[key] = (value, expire)


# 【复杂度】时间 O(1)；空间 O(n)。
# 【面试易错点】① 惰性淘汰漏写，导致过期数据一直返回；
#              ② ttl=0 时应立即过期（now+0 == now，exp>now 为 False → 正确返回 None）。


# =============================================================
# 第 4 题：余弦相似度 + Top-K 文档检索（最朴素的 RAG Retriever）
# 场景：RAG 里把 query 和文档都转成向量，召回最相似的 K 篇。
# =============================================================
# 【思路讲解】
# 余弦相似度 = 两向量点积 / (各自模长之积)，范围 [-1, 1]，越大越相似。
#   分子 dot = Σ aᵢ·bᵢ；分母 = |a|·|b|，其中 |a|=√(Σaᵢ²)。
#   任一方模长为 0（空向量）→ 返回 0.0，避免除零。
# Top-K：对每篇文档算分数，按分数降序取前 K 个下标即可。
#
# 【流程图】
#   cosine(a,b):  dot=Σaᵢbᵢ ; na=√Σaᵢ² ; nb=√Σbᵢ²
#                 return 0 if na==0 or nb==0 else dot/(na*nb)
#   top_k(query, docs, k):
#       分数 = [(cosine(query, vec), i) for i,(_,vec) in enumerate(docs)]
#       按分数降序排序 → 取前 k 个对应的文档
#
# 【代码】
def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def top_k_docs(query_vec, docs, k):
    # docs: [(vector, payload), ...]  payload 可以是文档原文等
    scored = [(cosine_similarity(query_vec, vec), i) for i, (vec, _) in enumerate(docs)]
    scored.sort(key=lambda t: t[0], reverse=True)        # 降序
    return [docs[i][1] for _, i in scored[:k]]


# 【复杂度】时间 O(N·d)（N 文档数，d 向量维度）；空间 O(N)。
# 【面试易错点】① 忘记归一化导致长文档占便宜；
#              ② 真实场景向量维度高（768/1536），要用 numpy；面试手写展示原理即可。


# =============================================================
# 第 5 题：从 Markdown 提取代码块（解析 LLM 输出）
# 场景：Agent 让模型返回 ```python ... ```，需要把代码抠出来执行。
# =============================================================
# 【思路讲解】
# Markdown 代码块格式：```lang\n内容\n```，三反引号成对出现。
# 用「找下一个 ```」的方式扫描（不用正则也能写清楚）：
#   1) 找到开头的 ```，其后是语言标识（到下一个 \n 为止）。
#   2) 内容从 \n 后开始，到下一个 ``` 结束。
#   3) 指针跳到结束的 ``` 之后，继续找下一对。
# 注意：内容末尾常带一个 \n，去掉更干净。
#
# 【流程图】
#   i = 0
#   loop:
#       fence = find("```", i)
#       if 没找到: break
#       lang  = 开头``` 到 下一个\n 之间的文字
#       end   = 从内容起点再找 "```"
#       content = 中间那段（去尾随 \n）
#       收集 (lang, content)
#       i = end + 3
#
# 【代码】
def extract_code_blocks(md):
    blocks = []
    i = 0
    n = len(md)
    while i < n:
        fence = md.find("```", i)
        if fence == -1:
            break
        start = fence + 3
        nl = md.find("\n", start)
        if nl == -1:
            break
        lang = md[start:nl].strip()
        content_start = nl + 1
        end = md.find("```", content_start)
        if end == -1:
            break
        content = md[content_start:end]
        if content.endswith("\n"):
            content = content[:-1]
        blocks.append((lang, content))
        i = end + 3
    return blocks


# 【复杂度】时间 O(n)（n 为文本长度，每次 find 线性但指针单向前进）；
#          空间 O(结果大小)。
# 【面试易错点】① 内部代码里出现 ``` 会误判（面试可说「假设代码块不含裸 ```」）；
#              ② 忘记处理「无语言标识」的纯 ``` 块（lang 应为空字符串）。


# =============================================================
# 第 6 题：提示词模板变量替换（Prompt Templating）
# 场景：把 "Hello {{name}}" 里的占位符替换成真实值，做 Prompt 工程。
# =============================================================
# 【思路讲解】
# 模板用 {{key}} 占位。用正则 \{\{(\w+)\}\} 找到所有占位符，
#   替换函数里：key 在变量表里就换成值；不在就【保留原样】而不是报错
#   （更稳健，避免一个漏填的变量把整条 Prompt 搞崩）。
# \w+ 匹配字母/数字/下划线组成的变量名；(\w+) 捕获组供替换使用。
#
# 【流程图】
#   render(tpl, vars):
#       return re.sub(r"\{\{(\w+)\}\}", 替换函数, tpl)
#       替换函数(m):  key = m.group(1)
#                     return str(vars[key]) if key in vars else m.group(0)  ← 保留
#
# 【代码】
def render_template(tpl, variables):
    def repl(m):
        key = m.group(1).strip()
        return str(variables[key]) if key in variables else m.group(0)
    return re.sub(r"\{\{(\w+)\}\}", repl, tpl)


# 【复杂度】时间 O(n)（n 为模板长度，正则单次扫描）；空间 O(结果)。
# 【面试易错点】① 直接 str.replace 处理多变量易出错，正则更稳；
#              ② 缺失变量报错会拖垮整体，保留原样更工程化；
#              ③ 变量值要 str() 一下，否则数字拼接报类型错。


# =============================================================
# 第 7 题：字典深度合并（Deep Merge，常用于合并配置）
# 场景：把「默认配置」和「用户配置」合并，用户的值覆盖默认，嵌套要递归。
# =============================================================
# 【思路讲解】
# 浅合并 dict(a, **b) 只会替换整个子字典，做不到「只改其中一项」。
# 深度合并规则：
#   对 b 的每个 key：若 a、b 该 key 都是 dict → 递归合并；否则 b 直接覆盖 a。
# 注意：不要原地改 a（可能外面还在用），返回新字典更干净。
#
# 【流程图】
#   deep_merge(a, b):
#       result = copy(a)
#       for k, v in b.items():
#           if k in result and 两边都是 dict:
#               result[k] = deep_merge(result[k], v)   ← 递归
#           else:
#               result[k] = v                          ← 覆盖
#       return result
#
# 【代码】
def deep_merge(a, b):
    result = dict(a)                      # 浅拷贝，避免改坏原对象
    for k, v in b.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result


# 【复杂度】时间 O(两字典总 key 数)；空间 O(结果大小)（递归栈深度 = 嵌套层数）。
# 【面试易错点】① 漏掉 isinstance 判断，把 list 也当 dict 递归导致异常；
#              ② 原地修改 a，外层逻辑被意外改变。


# =============================================================
# 第 8 题：发布订阅事件总线（EventBus / Pub-Sub）
# 场景：多 Agent 协作时，一个 Agent 完成事件（如「检索完成」）要通知其他模块。
# =============================================================
# 【思路讲解】
# 事件总线 = 话题(topic) → 订阅者列表 的映射。
#   subscribe(topic, callback)：把回调塞进该话题的列表。
#   publish(topic, data)：遍历该话题所有回调并调用，把 data 传进去。
# 这是观察者模式的极简实现，解耦「谁触发」和「谁响应」。
#
# 【流程图】
#   subscribe(topic, cb):  subs[topic].append(cb)
#   publish(topic, data):  for cb in subs[topic]: cb(data)
#
# 【代码】
class EventBus:
    def __init__(self):
        self.subs = {}                    # topic -> [callback, ...]

    def subscribe(self, topic, callback):
        self.subs.setdefault(topic, []).append(callback)

    def publish(self, topic, data):
        for cb in self.subs.get(topic, []):
            cb(data)


# 【复杂度】时间 subscribe O(1)、publish O(订阅者数)；空间 O(总订阅数)。
# 【面试易错点】① 用 list 当订阅表要防重复订阅（可加去重）；
#              ② publish 时某个回调抛异常会中断后续（可加 try/except 隔离）。


# =============================================================
# 第 9 题：流式 Top-K（最小堆维持最大的 K 个）
# 场景：Rerank 阶段从大量候选里挑最相关的 K 个，数据可能一边来一边处理。
# =============================================================
# 【思路讲解】
# 维护一个大小为 K 的【最小堆】：
#   堆顶是「当前 K 个里最小的」。新元素比堆顶大 → 弹出堆顶、压入新元素，
#   这样堆里始终留着最大的 K 个。比「全部排序」省内存（尤其数据流式到达）。
# 最后把堆排个序返回（降序）。
#
# 【流程图】
#   heap = []
#   for x in stream:
#       if len(heap) < k:      heappush(heap, x)
#       elif x > heap[0]:      heapreplace(heap, x)   ← 弹最小、压 x
#   return sorted(heap, reverse=True)
#
# 【代码】
def top_k_stream(stream, k):
    heap = []
    for x in stream:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:                  # 比当前最小的还小就忽略
            heapq.heapreplace(heap, x)     # 弹出堆顶，压入 x
    return sorted(heap, reverse=True)


# 【复杂度】时间 O(N·log K)（N 元素数，每次堆操作 log K）；空间 O(K)。
# 【面试易错点】① 用最大堆会留下最小的 K 个，方向反了；
#              ② heapreplace 比先 pop 再 push 少一次堆调整，更高效。


# =============================================================
# 第 10 题：URL 查询参数解析（parse query string）
# 场景：Agent 调用 HTTP 工具 / Web 搜索，要解析 ?q=...&page=... 这类参数。
# =============================================================
# 【思路讲解】
# 查询串形如 "a=1&b=2&a=3"，按 & 切分，每段按第一个 = 拆成 key/value。
#   同一 key 出现多次 → 用列表收集（如 a=[1,3]）。
#   还要做 URL 解码（%20 → 空格，用 urllib.parse.unquote）。
# 空串 / 无 = 的情况（如 "flag"）也要兜底处理。
#
# 【流程图】
#   parse(s):
#       result = {}
#       for pair in s.split("&"):
#           if 空: continue
#           k, v = pair.split("=", 1) 或 (pair, "")
#           k = unquote(k); v = unquote(v)
#           result[k].append(v)         ← 同一 key 收集成列表
#       return result
#
# 【代码】
def parse_query_string(s):
    result = {}
    if not s:
        return result
    for pair in s.split("&"):
        if not pair:
            continue
        if "=" in pair:
            k, v = pair.split("=", 1)
        else:
            k, v = pair, ""
        k = urllib.parse.unquote(k)
        v = urllib.parse.unquote(v)
        result.setdefault(k, []).append(v)
    return result


# 【复杂度】时间 O(n)（n 为串长）；空间 O(结果)。
# 【面试易错点】① 用 split("=") 而非 split("=",1)，value 含 = 会错位；
#              ② 忘记 URL 解码，%20 没变成空格；
#              ③ 单值场景返回列表可能不符合调用方预期（可再包一层取首个）。


# =============================================================
# 自测（运行 python LeetCode-Day20.py 全部断言通过即正确）
# =============================================================
if __name__ == "__main__":
    # --- 第1题：重试 ---
    calls = {"n": 0}
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ValueError("临时失败")
        return "ok"
    assert with_retry(flaky, max_retries=3, base_delay=0, jitter=0) == "ok"
    assert calls["n"] == 3

    def always_fail():
        raise RuntimeError("boom")
    try:
        with_retry(always_fail, max_retries=2, base_delay=0, jitter=0)
        assert False, "应当抛出最后一个异常"
    except RuntimeError:
        pass

    # --- 第2题：令牌桶 ---
    tb = TokenBucket(capacity=3, refill_rate=1.0)
    assert tb.allow() and tb.allow() and tb.allow()   # 前 3 次放行
    assert not tb.allow()                              # 第 4 次被限流
    tb.last = time.time() - 2                          # 模拟过去 2 秒，应补 ~2 令牌
    assert tb.allow()                                  # 又能放行

    # --- 第3题：TTL 缓存 ---
    c = TTLCache()
    c.set("a", 1, ttl=1)
    assert c.get("a") == 1
    c.set("b", 2, ttl=0)                               # 立即过期
    assert c.get("b") is None
    c.set("c", 3)                                      # 永不过期
    assert c.get("c") == 3

    # --- 第4题：余弦相似度 + Top-K ---
    q = [1, 0]
    docs = [([1, 0], "A"), ([0, 1], "B"), ([1, 1], "C")]
    assert abs(cosine_similarity([1, 0], [1, 0]) - 1.0) < 1e-9
    assert abs(cosine_similarity([1, 0], [0, 1]) - 0.0) < 1e-9
    assert top_k_docs(q, docs, 2) == ["A", "C"]

    # --- 第5题：Markdown 代码块 ---
    md = "intro\n```python\nprint(1)\n```\nmid\n```\nraw\n```\nend"
    assert extract_code_blocks(md) == [("python", "print(1)"), ("", "raw")]

    # --- 第6题：模板替换 ---
    assert render_template("Hi {{name}}, age {{age}}", {"name": "Bob", "age": 30}) == "Hi Bob, age 30"
    assert render_template("{{x}} and {{y}}", {"x": "A"}) == "A and {{y}}"   # 缺失保留

    # --- 第7题：深度合并 ---
    a = {"db": {"host": "h1"}, "debug": True}
    b = {"db": {"port": 5432}, "name": "app"}
    assert deep_merge(a, b) == {"db": {"host": "h1", "port": 5432}, "debug": True, "name": "app"}

    # --- 第8题：事件总线 ---
    bus = EventBus()
    log = []
    bus.subscribe("done", lambda d: log.append(d))
    bus.publish("done", 42)
    assert log == [42]

    # --- 第9题：流式 Top-K ---
    assert top_k_stream([1, 5, 2, 8, 3], 3) == [8, 5, 3]
    assert top_k_stream([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 4) == [10, 9, 8, 7]

    # --- 第10题：URL 解析 ---
    assert parse_query_string("a=1&b=2&a=3") == {"a": ["1", "3"], "b": ["2"]}
    assert parse_query_string("name=hello%20world") == {"name": ["hello world"]}

    print("✅ Day 20 全部 10 题自测通过（AI Agent / 后端手撕专项）")
