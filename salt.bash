if salt --version >/dev/null 2>&1 ; then
    if salt-ssh --version >/dev/null 2>&1 ; then
        function salt-ssh()
        {
            local SALT_SSH_DIR=$HOME/salt-ssh-setup
            test -d $SALT_SSH_DIR && {
                pushd $SALT_SSH_DIR
                /usr/bin/salt-ssh $@
				popd
            }
        }
    fi

	__sudo_defaults='--preserve-env=JC_PARSER'
    alias salt="sudo $__sudo_defaults salt"
    alias salt-cp="sudo $__sudo_defaults salt-cp"
    alias salt-key="sudo $__sudo_defaults salt-key"
    alias salt-call="sudo $__sudo_defaults salt-call"
    alias salt-run="sudo $__sudo_defaults salt-run"
    unset __sudo_defaults
fi
