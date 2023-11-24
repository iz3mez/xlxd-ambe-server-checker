# AMBE Server IP Checker
# This script in Python 3 restarts the xlxd service if the public ip address of the ambed server changes.
# It is useful in case both servers are not installed on the same server as xlxd.
# The service creates log files to monitor the public IP address range.
# 73 de IZ3MEZ Francesco
import socket
import subprocess
import time

def get_ip_address(domain):
    return socket.gethostbyname(domain)

def restart_service(service):
    subprocess.run(["/etc/init.d/" + service, "restart"])

def log_ip_change(log_file, old_ip, new_ip):
    with open(log_file, 'a') as f:
        f.write(f'IP changed from {old_ip} to {new_ip} at {time.ctime()}\n')

def main():
    domain = 'ambeserver.mydomain.org' # FQDN contained in xlxd start script
    service = 'xlxd'
    log_file = '/xlxd/xlxd-ambe-server-checker/ambe_ipchanges.log'

    ip_address = get_ip_address(domain)
    while True:
        time.sleep(120)  # check seconds
        new_ip_address = get_ip_address(domain)
        if new_ip_address != ip_address:
            restart_service(service)
            log_ip_change(log_file, ip_address, new_ip_address)
            ip_address = new_ip_address

if __name__ == "__main__":
    main()
