import logging
import salt.utils.json
from salt.utils.decorators.jinja import jinja_filter


log = logging.getLogger(__name__)


@jinja_filter('pretty_json')
def pretty_json(obj, indent=2):
    try:
        return salt.utils.json.dumps(obj, indent=indent)
    except Exception:
        log.exception("Failed to serialize object '%s'", obj)
    return '{}'
