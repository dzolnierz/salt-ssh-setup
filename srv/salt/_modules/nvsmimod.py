try:
    import nvsmi

    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

import salt.utils.json

from salt.utils.decorators import depends


# Define the module's virtual name
__virtualname__ = "nvsmimod"


def __virtual__():
    """
    Only return if nvsmi is installed
    """
    if HAS_LIBS:
        if __utils__["path.which"]("nvidia-smi") is not None:
            return __virtualname__
        else:
            return (
                False,
                "The nvsmi execution module cannot be loaded: "
                "nvsmi library requires the command nvidia-smi"
            )
    else: 
        return (
            False,
            "The nvsmi execution module cannot be loaded: "
            "nvsmi library not available.",
        )

@depends('nvsmi')
def get_gpus():
    gpus = []
    ret = []
    try:
        gpus = nvsmi.get_gpus()
    except:
        pass
    for gpu in gpus:
        ret.append(salt.utils.json.loads(gpu.to_json()))
    return ret
