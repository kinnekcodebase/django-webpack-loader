from django import template, VERSION
from django.conf import settings
from django.utils.safestring import mark_safe
from .. import utils

register = template.Library()


def filter_by_extension(bundle, extension):
    '''Return only files with the given extension'''
    for chunk in bundle:
        if chunk['name'].endswith('.{0}'.format(extension)):
            yield chunk


def render_as_tags(bundle):
    tags = []
    for chunk in bundle:
        if chunk['name'].endswith('.js'):
            tags.append((
                '<script type="text/javascript" src="{0}"></script>'
            ).format(chunk['url']))
        elif chunk['name'].endswith('.css'):
            tags.append((
                '<link type="text/css" href="{0}" rel="stylesheet"/>'
            ).format(chunk['url']))
    return mark_safe('\n'.join(tags))


def _get_bundle(bundle_name, extension, config):
    bundle = utils.get_loader(config, bundle_name).get_bundle(bundle_name)
    if extension:
        bundle = filter_by_extension(bundle, extension)
    return bundle


@register.simple_tag
def render_bundle(bundle_name, extension=None, config='DEFAULT', attrs=''):
    tags = utils.get_as_tags(bundle_name, extension=extension, config=config, attrs=attrs)
    return mark_safe('\n'.join(tags))


@register.simple_tag
def webpack_static(asset_name, config='DEFAULT'):
    return utils.get_static(asset_name, config=config)


assignment_tag = register.simple_tag if VERSION >= (1, 9) else register.assignment_tag


@assignment_tag
def get_files(bundle_name, extension=None, config='DEFAULT'):
    """
    Returns all chunks in the given bundle.
    Example usage::

        {% get_files 'editor' 'css' as editor_css_chunks %}
        CKEDITOR.config.contentsCss = '{{ editor_css_chunks.0.publicPath }}';

    :param bundle_name: The name of the bundle
    :param extension: (optional) filter by extension
    :param config: (optional) the name of the configuration
    :return: a list of matching chunks
    """
    return utils.get_files(bundle_name, extension=extension, config=config)


@register.assignment_tag
def get_url(bundle_name, extension=None, config='DEFAULT'):
    """
    Returns first file url
    """
    return utils.get_first_url(bundle_name, extension=extension, config=config)
