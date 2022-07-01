import logging
import requests
import json


log = logging.getLogger(__name__)
# Define the module's virtual name
__virtualname__ = "vaultmod"


def __virtual__():
    return __virtualname__


def unseal(keys, vault_url=None, verify=False):
    """
    Unseal Vault server

    This function uses the 'unseal_keys' from the 'vault' pillar to unseal vault server

    vault:
      unseal_keys:
        - n63/TbrQuL3xaIW7ZZpuXj/tIfnK1/MbVxO4vT3wYD2A
        - S9OwCvMRhErEA4NVVELYBs6w/Me6+urgUr24xGK44Uy3
        - F1j4b7JKq850NS6Kboiy5laJ0xY8dWJvB3fcwA+SraYl
        - 1cYtvjKJNDVam9c7HNqJUfINk4PYyAXIpjkpN/sIuzPv
        - 3pPK5X6vGtwLhNOFv1U2elahECz3HpRUfNXJFYLw6lid

    .. note: This function will send unsealed keys until the api returns back
             that the vault has been unsealed

    CLI Examples:

    .. code-block:: bash

        salt-call vaultmod.unseal
    """
    resource = "v1/sys/unseal"
    url = "{}/{}".format(vault_url, resource)
    for key in keys:
        log.debug("Debug key '%s'", key)
        ret = requests.put(url, data=json.dumps({"key": key}), verify=verify).json()
        log.debug("Debug ret '%s'", ret['sealed'])
        if ret["sealed"] is False:
            return True
    return False
