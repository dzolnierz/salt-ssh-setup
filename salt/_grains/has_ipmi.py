import stat
import os

def has_ipmi():
    grains = {}
    grains['has_ipmi'] = False
    try:
        grains['has_ipmi'] = stat.S_ISCHR(os.stat("/dev/ipmi0").st_mode)
    except:
        pass
    return grains
