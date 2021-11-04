import logging
from salt.utils.decorators.jinja import jinja_filter


log = logging.getLogger(__name__)


@jinja_filter('pop_element')
def pop_element(obj):
    try:
        return obj.pop()
    except Exception:
        log.exception("Failed to pop element from object '%s'", obj)
    return ''
