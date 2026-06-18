```python
def is_palindrome(s, case_sensitive=True, ignore_non_alphanumeric=False):
    if s is None:
        raise ValueError("Input string cannot be None")
    
    left, right = 0, len(s) - 1
    while left < right:
        l_char = s[left]
        r_char = s[right]
        
        if ignore_non_alphanumeric:
            if not l_char.isalnum():
                left += 1
                continue
            if not r_char.isalnum():
                right -= 1
                continue
        
        if not case_sensitive:
            l_char = l_char.lower()
            r_char = r_char.lower()
        
        if l_char != r_char:
            return False
        
        left += 1
        right -= 1
    
    return True


def is_palindrome_default(s):
    return is_palindrome(s)
```