```python
def sum_1_to_10000_formula():
    """计算1到10000的和（等差数列求和公式，O(1)）"""
    n = 10000
    return n * (n + 1) // 2

def sum_1_to_10000_loop():
    """计算1到10000的和（循环累加，O(n)）"""
    total = 0
    for i in range(1, 10001):
        total += i
    return total

def sum_range(start, end):
    """计算 [start, end] 闭区间的整数和（等差数列公式）"""
    if start > end:
        return 0
    n = end - start + 1
    return n * (start + end) // 2

def calculate_sum():
    """计算 1 到 10000 的和（基于等差数列公式，最终交付）"""
    return 10000 * 10001 // 2
```