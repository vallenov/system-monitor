import subprocess as sb
import requests
import json
import config


class Monitor:

    @staticmethod
    def get_name_of_machine() -> str:
        """
        Get name of the current machine
        """
        return sb.check_output("uname -n", shell=True).decode()[:-1]

    @staticmethod
    def get_temperature() -> int:
        """
        Get temperature of cores
        """
        output = sb.check_output("cat `find /sys/ -name temp 2>/dev/null`", shell=True)
        temp_list = output.decode().split()
        temp_list = list(map(lambda t: int(t), temp_list))
        temp = (sum(temp_list) // len(temp_list)) // 1000
        return temp

    @staticmethod
    def get_used_space() -> dict:
        """
        Get used space on server
        """
        output = sb.check_output(r"df -h | grep [[:digit:]][[:lower:]][[:digit:]] | awk '{print $6, $5}'", shell=True)
        output = output.decode().split('\n')
        output = list(filter(lambda line: len(line) > 0, output))
        out_dict = {}
        for mount_point in output:
            tmp = mount_point.split()
            out_dict[tmp[0]] = int(tmp[1][:-1])
        return out_dict

    @staticmethod
    def get_self_ip() -> str or None:
        """
        Get server's ip
        """
        output = sb.check_output("ifconfig | "
                                 "grep `ifconfig -s | "
                                 "grep '\<w.*' | "
                                 "awk '{print $1}'` -A 1 | "
                                 "grep inet | "
                                 "awk '{print $2}'", shell=True)
        output = output.decode()
        return output[:-1] if output else None

    @staticmethod
    def get_ssh_connections() -> list:
        """
        Get list of server connections
        """
        output = sb.check_output(r"ss -o state established '( dport = :ssh or sport = :ssh )' "
                                 r"| awk '{print $5}' "
                                 r"| grep -v ssh", shell=True)
        output = output.decode().split('\n')
        output = output[1:-1]
        return output

    @staticmethod
    def get_ngrok_tunnels() -> list:
        """
        Get current ngrok tunnels
        """
        tunnels = []
        headers = {
            'Authorization': f"Bearer {config.NGROK_TOKEN}",
            'Ngrok-Version': '2'
        }
        data = requests.get(config.Url.ngrok_api + 'tunnels', headers=headers)
        if data.status_code == 200:
            res = json.loads(data.text)
            for tunnel in res['tunnels']:
                arr = tunnel['public_url'].split(':')
                url = ':'.join(arr[:2]).replace('tcp://', 'http://')
                port = arr[2]
                tunnels.append({
                    'url': url,
                    'port': port,
                    'protocol': tunnel['proto'],
                    'forwards_to': tunnel['forwards_to']
                })
        return tunnels

    @staticmethod
    def uptime() -> dict:
        """
        Get uptime info
        """
        output = sb.check_output('uptime')
        output = output.decode().split()
        data = {
            'server_time': output[0],
            'uptime': ' '.join(output[2:5]),
            'users': output[5],
            'load_average': ' '.join(output[9:])
        }
        return data
