from pprint import PrettyPrinter
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from ..utils import get_loader

register = template.Library()


def filter_by_extension(bundle, extension):
    '''Return only files with the given extension'''
    for chunk in bundle:
        if chunk['name'].endswith('.{0}'.format(extension)):
            yield chunk


def render_as_tags(bundle, type):
    tags = []

    pp = PrettyPrinter(indent=4, width=80)

    if type is 'static':
        urlFormat = "{{% static '{0}' %}}"
    else:
        urlFormat = '{0}'

    print 'type:'
    print type
    print 'bundle instance: {}'
    print type(bundle)

    for chunk in bundle:
        if chunk['name'].endswith('.js'):
            tagString = '<script type="text/javascript" src="%s"></script>'%urlFormat
            tags.append((tagString).format(chunk['url']))
        elif chunk['name'].endswith('.css'):
            tagString = '<link type="text/css" href="%s" rel="stylesheet"/>'%urlFormat
            tags.append((tagString).format(chunk['url']))

    print 'tags: \n%s' % "*" * 80
    pp.pprint(tags)

    print "*" * 80

    return mark_safe('\n'.join(tags))


def _get_bundle(bundle_name, extension, config):
    print "Hi Thalida - look at me now."
    bundle = get_loader(config).get_bundle(bundle_name)
    if extension:
        bundle = filter_by_extension(bundle, extension)
    return bundle


@register.simple_tag
def render_bundle(bundle_name, extension=None, format_type=None, config='DEFAULT'):
    return render_as_tags(_get_bundle(bundle_name, extension, config), format_type)


@register.simple_tag
def webpack_static(asset_name, config='DEFAULT'):
    return "{0}{1}".format(
        get_loader(config).get_assets().get(
            'publicPath', getattr(settings, 'STATIC_URL')
        ),
        asset_name
    )


@register.assignment_tag
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
    return list(_get_bundle(bundle_name, extension, config))
