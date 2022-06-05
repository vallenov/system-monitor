import subprocess as sb


class Monitor:
    block_message = {
        'ssh': {},
        'used_space': {}
    }

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
        output = sb.check_output(r"ifconfig | tail | grep 'inet ' | awk '{print $2}'", shell=True)
        if output:
            output = output.decode()
            output = output.split('\n')
            output = list(filter(lambda ip: ip, output))
            output = output[-1]
            return output
        else:
            return None

    @staticmethod
    def get_ssh_connections() -> list:
        output = sb.check_output(r"ss -o state established '( dport = :ssh or sport = :ssh )' | awk '{print $5}'", shell=True)
        output = output.decode().split('\n')
        output = output[1:-1]
        return output
