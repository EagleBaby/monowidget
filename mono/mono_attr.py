class MonoAttr:
    """MonoAttr 类，用于管理单个参数属性"""
    
    def __init__(self, name, value, type_hint=None, **kwargs):
        """
        初始化MonoAttr对象
        
        Args:
            name: 参数名称
            value: 参数值
            type_hint: 类型提示
            **kwargs: 其他属性
        """
        self.name = name
        self.value = value
        self.type_hint = type_hint
        self.kwargs = kwargs
        
    def to_dict(self):
        """将MonoAttr转换为字典"""
        return {
            'name': self.name,
            'value': self.value,
            'type_hint': self.type_hint,
            **self.kwargs
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建MonoAttr"""
        return cls(
            name=data['name'],
            value=data['value'],
            type_hint=data.get('type_hint'),
            **{k: v for k, v in data.items() if k not in ['name', 'value', 'type_hint']}
        )