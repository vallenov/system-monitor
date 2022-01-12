import subprocess as sb


class Monitor:
    block_message = {}

    @staticmethod
    def get_temperature() -> str and int:
        name = sb.check_output("uname -n", shell=True).decode()[:-1]
        output = sb.check_output("cat `find /sys/ -name temp 2>/dev/null`", shell=True)
        temp_list = output.decode().split()
        temp_list = list(map(lambda t: int(t), temp_list))
        temp = (sum(temp_list) // len(temp_list)) // 1000
        return name, temp
