"""
Module for interacting with the GitLab v4 API.

:depends: python-gitlab python module

Configuration
-------------

Configure this module by specifing the name of a configuration
profile in the minion config, minion pillar, or master config. The module
will use the 'gitlab' key by default, if defined.

For example:

.. code-block:: yaml

    gitlab:
      url: https://gitlab.example.com
      private_token: PRIVATE_TOKEN
"""

import logging

import salt.utils.http
from salt.exceptions import CommandExecutionError

HAS_LIBS = False
try:
    import gitlab

    # pylint: enable=no-name-in-module
    HAS_LIBS = True
except ImportError:
    pass

log = logging.getLogger(__name__)

__virtualname__ = "gitlab"


def __virtual__():
    """
    Only load this modules if python-gitlab is installed on this minion.
    """
    if HAS_LIBS:
        return __virtualname__
    return (
        False,
        "The gitlab execution module cannot be loaded: "
        "python-gitlab library is not installed.",
    )


def _get_config_value(profile, config_name):
    """
    Helper function that returns a profile's configuration value based on
    the supplied configuration name.

    profile
        The profile name that contains configuration information.

    config_name
        The configuration item's name to use to return configuration values.
    """
    config = __salt__["config.option"](profile)
    if not config:
        raise CommandExecutionError(
            "Authentication information could not be found for the "
            "'{}' profile.".format(profile)
        )

    config_value = config.get(config_name)
    if config_value is None:
        raise CommandExecutionError(
            "The '{}' parameter was not found in the '{}' profile.".format(
                config_name, profile
            )
        )

    return config_value


def _get_client(profile):
    """
    Return the GitLab client, cached into __context__ for performance
    """
    url = _get_config_value(profile, "url")
    private_token = _get_config_value(profile, "private_token")
    key = "gitlab.{}:{}".format(private_token, url)

    if key not in __context__:
        __context__[key] = gitlab.Gitlab(url,
                                         private_token=private_token,
                                         pagination="keyset",
                                         order_by="id",
                                         per_page=100)
    return __context__[key]


def list_groups(profile="gitlab", ignore_cache=False):
    """
    List all groups.

    profile
        The name of the profile configuration to use. Defaults to ``gitlab``.

    ignore_cache
        Bypasses the use of cached groups.

    CLI Example:

    .. code-block:: bash

        salt myminion gitlab.list_groups
        salt myminion gitlab.list_groups profile='my-gitlab-profile'
    """
    private_token = _get_config_value(profile, "private_token")
    key = "gitlab.{}:groups".format(private_token)
    if key not in __context__ or ignore_cache:
        client = _get_client(profile)
        __context__[key] = [group.full_path for group in client.groups.list(iterator=True)]
    return __context__[key]


def list_users(profile="gitlab", active=False, external=False, exclude_external=False, blocked=False,
               ignore_cache=False):
    """
    List all users.

    profile
        The name of the profile configuration to use. Defaults to ``gitlab``.

    ignore_cache
        Bypasses the use of cached users.

    CLI Example:

    .. code-block:: bash

        salt myminion gitlab.list_users
        salt myminion gitlab.list_users profile='my-gitlab-profile'
    """
    private_token = _get_config_value(profile, "private_token")
    key = "gitlab.{}:users".format(private_token)
    if key not in __context__ or ignore_cache:
        client = _get_client(profile)
        __context__[key] = [users.username for users in client.users.list(active=active,
                                                                          external=external,
                                                                          exclude_external=exclude_external,
                                                                          blocked=blocked,
                                                                          iterator=True)]
    return __context__[key]


def get_user(user_search_term, profile="gitlab", ignore_cache=False):
    """
    Get user info.

    user_search_term
        The user's name, username, or public email.

    profile
        The name of the profile configuration to use. Defaults to ``gitlab``.

    ignore_cache
        Bypasses the use of cached users.

    CLI Example:

    .. code-block:: bash

        salt myminion gitlab.get_user john.doe@example.com
        salt myminion gitlab.get_user john.doe@example.com profile='my-gitlab-profile'
    """
    private_token = _get_config_value(profile, "private_token")
    key = "gitlab.{}:user:{}".format(private_token, user_search_term)
    if key not in __context__ or ignore_cache:
        client = _get_client(profile)
        try:
            user = client.users.list(search=user_search_term)[0]
            __context__[key] = {"id": user.id, "username": user.username, "email": user.email, "state": user.state, "2fa": user.two_factor_enabled}
        except IndexError:
            log.exception("User '{}' not found".format(user_search_term))
            return False
    return __context__[key]


def block_user(user_search_term, profile="gitlab"):
    """
    Set user state to ``blocked``.

    user_search_term
        The user's name, username, or public email.

    profile
        The name of the profile configuration to use. Defaults to ``gitlab``.

    CLI Example:

    .. code-block:: bash

        salt myminion gitlab.block_user john.doe@example.com
        salt myminion gitlab.block_user john.doe@example.com profile='my-gitlab-profile'
    """
    client = _get_client(profile)
    try:
        user = client.users.list(search=user_search_term)[0]
    except IndexError:
        log.exception("User '{}' not found".format(user_search_term))
        return False
    if user.state == "active":
        user.block()
    if user.two_factor_enabled:
        user.two_factor_enabled = False
    return not user.state == "active"


def delete_user_ssh_keys(user_search_term, profile="gitlab"):
    """
    Delete all SSH keys owned by the user.

    user_search_term
        The user's name, username, or public email.

    profile
        The name of the profile configuration to use. Defaults to ``gitlab``.

    CLI Example:

    .. code-block:: bash

        salt myminion gitlab.delete_user_ssh_keys john.doe@example.com
        salt myminion gitlab.delete_user_ssh_keys john.doe@example.com profile='my-gitlab-profile'
    """
    client = _get_client(profile)
    try:
        user = client.users.list(search=user_search_term)[0]
        [key.delete() for key in user.keys.list()]
    except IndexError:
        log.exception("User '{}' not found".format(user_search_term))
        return False
    return not user.keys.list()


def delete_personal_access_tokens(user_search_term, profile="gitlab"):
    """
    Delete all Personal Access Tokens owned by the user.

    user_search_term
        The user's name, username, or public email. 

    profile
        The name of the profile configuration to use. Defaults to ``gitlab``.

    CLI Example:

    .. code-block:: bash

        salt myminion gitlab.delete_personal_access_tokens john.doe@example.com
        salt myminion gitlab.delete_personal_access_tokens john.doe@example.com profile='my-gitlab-profile'
    """
    client = _get_client(profile)
    try:
        user = client.users.list(search=user_search_term)[0]
        [token.delete() for token in client.personal_access_tokens.list(user_id=user.id, state="active")]
    except IndexError:
        log.exception("User '{}' not found".format(user_search_term))
        return False
    return not client.personal_access_tokens.list(user_id=user.id, state="active")
