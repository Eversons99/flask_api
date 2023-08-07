from telnetlib import Telnet
import time, requests

def run(device_info):
    try:
        commands = format_commands(device_info)
        host = device_info['host']
        olt = requests.get(f'https://nmt.nmultifibra.com.br/files/single-host/{host}').json()
        username = olt[host]['management']['credentials']['username'] 
        password = olt[host]['management']['credentials']['password'] 
        host_address = olt[host]['management']['ipv4']['primary']
        
        try:
            applied_commands = apply_commands(host_address, username, password, commands)
            return applied_commands
        
        except Exception as err:
            return {
                "error": f'An error occurred while applying the commands in {host}. Err: {err}'
            }
        
    except Exception as err:
        return {
            "error": f'An error occurred while querying host information in NMT. Err: {err}'
        }
   
def format_commands(device_info):
    pon = device_info['pon']
    slot = pon.split('/')[1]
    port = pon.split('/')[2]
    id = device_info['id']
    
    commands = [
        f'interface gpon 0/{slot}',
        f'ont modify {port} {id} ont-lineprofile-id 10 ont-srvprofile-id 10',
        'quit',
        f'service-port vlan 319 gpon {pon} ont {id} gemport 3 multi-service user-vlan 103 tag-transform translate'
    ]

    return commands

def connect_host(host, user, password):
    try:
        tn = Telnet(host, '2323')
        tn.read_until(b"User name:")
        tn.write(user.encode('utf-8') + b"\n")

        tn.read_until(b"User password:")
        tn.write(password.encode('utf-8') + b"\n")
        time.sleep(1)

        tn.write("enable".encode('utf-8') + b"\n")
        tn.write("config".encode('utf-8') + b"\n")
        tn.write("cls".encode('utf-8') + b"\n")

        return tn
    except Exception as err:
        return { "error": f'Ocorreu um erro ao se conectar a OLT. Error: {err}'}

def apply_commands(host, user, password, commands):
    telnet_con = connect_host(host=host, user=user, password=password)
    logs = []
        
    try:
        for command in commands:
            telnet_con.write(command.encode('utf-8') + b"\n\n")
            telnet_con.write(b" " + b"\n\n")
            log = telnet_con.read_very_eager().decode('utf-8')
            time.sleep(2)

            logs.append({
                'command': command,
                'log': log
            })

        telnet_con.close()
        return logs
        
    except Exception as err:
        return {
            "error": f'An error occurred while applying the commands or connecting to host. Err: {err}'
        }
