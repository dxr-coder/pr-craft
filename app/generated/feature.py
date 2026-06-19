```python
from functools import lru_cache

@lru_cache(maxsize=128)
def factorial(n: int) -> int:
    """计算非负整数 n 的阶乘。"""
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```