class IdOrderedDict(dict):
    """
    保持键插入顺序的有序字典
    基于插入顺序维护键的顺序
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._keys = []
        self.update(*args, **kwargs)
    
    def __setitem__(self, key, value):
        if key not in self:
            self._keys.append(key)
        super().__setitem__(key, value)
    
    def __delitem__(self, key):
        super().__delitem__(key)
        self._keys.remove(key)
    
    def __iter__(self):
        return iter(self._keys)
    
    def keys(self):
        return self._keys
    
    def values(self):
        return [self[key] for key in self._keys]
    
    def items(self):
        return [(key, self[key]) for key in self._keys]
    
    def update(self, *args, **kwargs):
        if args:
            other = args[0]
            if hasattr(other, "items"):
                for key, value in other.items():
                    self[key] = value
            else:
                for key, value in other:
                    self[key] = value
        for key, value in kwargs.items():
            self[key] = value
    
    def clear(self):
        super().clear()
        self._keys.clear()
    
    def pop(self, key, *args):
        result = super().pop(key, *args)
        if key in self._keys:
            self._keys.remove(key)
        return result
    
    def popitem(self):
        if not self._keys:
            raise KeyError("dictionary is empty")
        key = self._keys.pop()
        value = super().pop(key)
        return key, value
    
    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]
    
    def move_to_end(self, key, last=True):
        """将键移动到末尾或开头"""
        if key not in self:
            raise KeyError(key)
        
        self._keys.remove(key)
        if last:
            self._keys.append(key)
        else:
            self._keys.insert(0, key)
    
    def move_to_start(self, key):
        """将键移动到开头"""
        self.move_to_end(key, last=False)