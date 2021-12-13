# salt-ssh-setup

Setup salt-ssh to run as a non-root user.


## Installation

Assume you have already installed salt-ssh.

```shell
test -d ./workdir || mkdir -p ./workdir
git clone git@github.com:dzolnierz/salt-ssh-setup.git ./workdir/salt-ssh-setup
cd ./workdir/salt-ssh-setup
cp ./etc/salt/master.example ./etc/salt/master
touch ./etc/salt/roster
```

And add your minions to roster.


## Usage

```shell
source salt.bash  # or salt.zsh
salt-ssh '*' test.ping
```
