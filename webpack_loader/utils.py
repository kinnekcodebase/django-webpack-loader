from .loader import WebpackLoader


_loaders = {}


def get_loader(config_name, bundle_name=None):
    key = config_name + bundle_name
    if key not in _loaders:
        _loaders[key] = WebpackLoader(config_name, bundle_name)
    return _loaders[key]


def _filter_by_extension(bundle, extension):
    '''Return only files with the given extension'''
    for chunk in bundle:
        if chunk['name'].endswith('.{0}'.format(extension)):
            yield chunk


def _get_bundle(bundle_name, extension, config):
    bundle = get_loader(
        config, bundle_name=bundle_name).get_bundle(bundle_name)
    if extension:
        bundle = _filter_by_extension(bundle, extension)
    return bundle


def get_files(bundle_name, extension=None, config='DEFAULT'):
    '''Returns list of chunks from named bundle'''
    return list(_get_bundle(bundle_name, extension, config))

def get_url(bundle_name, extension=None, config='DEFAULT'):
    '''Returns first url of files from named bundle'''
    files = get_files(bundle_name, extension, config)
    return files[0].get('url') if files and files[0] and files[0].get('url') else None