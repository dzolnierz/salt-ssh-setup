# salt-ssh-setup

Setup salt-ssh to run as a non-root user.

## Installation

**NOTE**: Assume you have already installed the `salt-ssh` package. If not, please go to https://docs.saltproject.io/salt/install-guide/en/latest/topics/install-by-operating-system/index.html.

```shell
git clone git@github.com:dzolnierz/salt-ssh-setup.git
cd salt-ssh-setup
# See: https://docs.saltproject.io/en/latest/topics/ssh/index.html#advanced-options-with-salt-ssh
cp etc/salt/master.example etc/salt/master
```

And add your minion(s) to the [roster](https://docs.saltproject.io/en/latest/topics/ssh/index.html#salt-ssh-roster) file.

```shell
touch etc/salt/roster
```

## Usage

If configured correctly target minion(s) should respond to the `test.ping` module:

```shell
source salt.$(basename $SHELL)
salt-ssh \* test.ping
```

## Read more

 * https://docs.saltproject.io/en/latest/topics/ssh/index.html
