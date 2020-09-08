DIFFERS = {}


def differ(name):
    def inner(func):
        DIFFERS[name] = func
        return func
    return inner
