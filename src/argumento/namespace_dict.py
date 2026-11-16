class NamespaceDict(dict):
    def __init__(self, *args, **kwargs):
        super(NamespaceDict, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __getitem__(self, item):
        idx_dot = item.find('.')
        if idx_dot >= 0:
            curr_attr = item[:idx_dot]
            nested_attr = item[idx_dot + 1:]
            nested_map = self.get(curr_attr)
            if not isinstance(nested_map, dict):
                return None
            return nested_map.get(nested_attr)
        else:
            return self.get(item)

    def __setitem__(self, key, value):
        if isinstance(value, dict) and not isinstance(value, NamespaceDict):
            value = NamespaceDict(value)
        idx_dot = key.find('.')
        if idx_dot >= 0:
            attr = key[:idx_dot]
            nested_key = key[idx_dot + 1:]
            nested_map = self.get(attr)
            if not isinstance(nested_map, NamespaceDict):
                nested_map = NamespaceDict() if nested_map is None else NamespaceDict(nested_map)
            nested_map[nested_key] = value
            super(NamespaceDict, self).__setitem__(attr, nested_map)
            self.__dict__[attr] = nested_map
        else:
            super(NamespaceDict, self).__setitem__(key, value)
            self.__dict__[key] = value

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(NamespaceDict, self).__delitem__(key)
        self.__dict__.pop(key, None)