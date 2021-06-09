import subprocess

def physical_cpus():
    ids = subprocess.run("grep 'physical id' /proc/cpuinfo | sort | uniq | cut -d\  -f3", stdout=subprocess.PIPE, shell=True).stdout.splitlines()
    grains = {}
    grains['cpu_physical_ids'] = ids
    return grains
