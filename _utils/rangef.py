class rangef:
    """
    浮点数版本的range，支持浮点数步长
    
    示例:
        >>> for x in rangef(0, 1, 0.1):
        ...     print(x)
        0.0
        0.1
        0.2
        ...
    """
    
    def __init__(self, *args):
        """
        初始化rangef对象
        
        Args:
            start: 起始值 (默认为0)
            stop: 结束值 (不包含)
            step: 步长 (默认为1.0)
        """
        if len(args) == 1:
            self.start, self.stop, self.step = 0.0, float(args[0]), 1.0
        elif len(args) == 2:
            self.start, self.stop, self.step = float(args[0]), float(args[1]), 1.0
        elif len(args) == 3:
            self.start, self.stop, self.step = float(args[0]), float(args[1]), float(args[2])
        else:
            raise TypeError("rangef expected at most 3 arguments, got {}".format(len(args)))
        
        if self.step == 0:
            raise ValueError("rangef() step argument must not be zero")
    
    def __iter__(self):
        """返回迭代器"""
        current = self.start
        if self.step > 0:
            while current < self.stop:
                yield current
                current += self.step
        else:
            while current > self.stop:
                yield current
                current += self.step
    
    def __len__(self):
        """返回序列长度"""
        if self.step > 0:
            return max(0, int((self.stop - self.start) / self.step))
        else:
            return max(0, int((self.start - self.stop) / (-self.step)))
    
    def __getitem__(self, index):
        """支持索引访问"""
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            new_start = self.start + start * self.step
            new_stop = self.start + stop * self.step
            new_step = step * self.step
            return rangef(new_start, new_stop, new_step)
        
        length = len(self)
        if index < 0:
            index += length
        if not 0 <= index < length:
            raise IndexError("rangef object index out of range")
        
        return self.start + index * self.step
    
    def __repr__(self):
        """字符串表示"""
        if self.step == 1.0:
            return "rangef({}, {})".format(self.start, self.stop)
        else:
            return "rangef({}, {}, {})".format(self.start, self.stop, self.step)
    
    def __reversed__(self):
        """返回反向迭代器"""
        current = self.start + (len(self) - 1) * self.step
        for _ in range(len(self)):
            yield current
            current -= self.step
    
    def count(self, value):
        """计算值出现的次数"""
        value = float(value)
        if self.step > 0:
            if self.start <= value < self.stop:
                diff = value - self.start
                if abs(diff / self.step - round(diff / self.step)) < 1e-10:
                    return 1
        else:
            if self.stop < value <= self.start:
                diff = self.start - value
                if abs(diff / (-self.step) - round(diff / (-self.step))) < 1e-10:
                    return 1
        return 0
    
    def index(self, value):
        """返回值的索引"""
        value = float(value)
        if self.step > 0:
            if self.start <= value < self.stop:
                diff = value - self.start
                if abs(diff / self.step - round(diff / self.step)) < 1e-10:
                    return int(round(diff / self.step))
        else:
            if self.stop < value <= self.start:
                diff = self.start - value
                if abs(diff / (-self.step) - round(diff / (-self.step))) < 1e-10:
                    return int(round(diff / (-self.step)))
        raise ValueError("{} is not in rangef".format(value))