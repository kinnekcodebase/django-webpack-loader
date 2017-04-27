from .loader import WebpackLoader


_loaders = {}


def get_loader(config_name, bundle_name=None):
    key = config_name + bundle_name
    if key not in _loaders:
        _loaders[key] = WebpackLoader(config_name, bundle_name)
    return _loaders[key]
