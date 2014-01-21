
def atoi(val, default=None):
    return _convert(val, default, int)

def atof(val, default=None):
    return _convert(val, default, float)

def _convert(val, default, func):
    try:
        return func(val)
    except ValueError:
        return default

def apply_transforms(transforms, d):
    for key, func in transforms:
        d[key] = func(d)