function salt-ssh()
{
    (
        local SALT_SSH_DIR=$HOME/workdir/salt-ssh-setup
        test -d $SALT_SSH_DIR && {
            cd $SALT_SSH_DIR
            /usr/bin/salt-ssh $@
        }
    )
}
