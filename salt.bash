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

    alias salt='sudo salt'
    alias salt-cp='sudo salt-cp'
    alias salt-key='sudo salt-key'
    alias salt-call='sudo salt-call'
    alias salt-run='sudo salt-run'
fi
