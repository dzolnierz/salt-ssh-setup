import logging
from salt.utils.decorators.jinja import jinja_filter
from salt._compat import ipaddress


log = logging.getLogger(__name__)


@jinja_filter('pop_element')
def pop_element(obj):
    try:
        return obj.pop()
    except Exception:
        log.exception("Failed to pop element from object '%s'", obj)
    return ''


@jinja_filter('network_address')
def network_address(value):
    try:
        return str(ipaddress.ip_network(value, False))
    except Exception:
        log.exception("Failed to determine network address from '%s'", value)
    return ''
