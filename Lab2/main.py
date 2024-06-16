import subprocess
import click


def do_command(command):
    return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

def try_packet_size(host, packet, verbose):
    print(f"Now trying to ping {host} with {packet} size payload")
    command = f"ping -M do -c 1 -s {packet} {host}"
    response = do_command(command)
    answer = True
    for line in iter(response.stdout.readline, b''):
        line = line.decode(encoding='utf-8')
        if verbose:
            print(line)
        bad_patterns = {"too long", "too large", "100.0% packet loss"}
        for pattern in bad_patterns:
            if pattern in line:
                answer = False
    if answer:
        print("Size is OK")
    else:
        print("Size is not OK")
    print()
    return answer


@click.command()
@click.option("--host", required=True, type=str)
@click.option("--verbose", required=False, type=bool)
def main(host, verbose=False):
    starting_size = 1 
    while try_packet_size(host, starting_size, verbose):
        starting_size *= 2

    r = starting_size
    l = starting_size // 2
    while r - l > 1:
        m = (l + r) // 2
        if try_packet_size(host, m, verbose):
            l = m
        else:
            r = m
    #28 is the headers size
    print(f"Found MTU, it is {l + 28}")

main()
