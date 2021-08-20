# -*- coding: utf-8 -*-

# @Time    : 2021/8/19 5:21 下午 
# @Author  : cyq
# @File    : mac.py
import os

from utils.Shell import Shell
from utils.worker import Worker


class Mac:

    def __init__(self, catch_time: int = 0):
        """
        init
        :param catch_time: 测试时间 xh
        """
        self.ctime = catch_time * 60 * 60

    def catch(self):
        path = os.path.join(os.path.dirname(__file__), "mac_out.txt")
        if os.path.exists(path):
            os.remove(path)

        _cmd = "top  -l 10 -s 1 -ncols 10 | grep -E 'rzpaas_examp' | awk '{print  $2,\"cpu=\"$3,\"mem=\"$8 }'  >> " + path
        print("测试开始。 请确认已开启 paastest")
        while self.ctime > 0:
            Shell.invoke(_cmd)
            self.ctime -= 1
            print(f"step {self.ctime} ..")
        print("测试结束，生成测试报告中。。。。")

        info = Worker.read(path)
        cpu = []
        mem = []
        for i in info:
            if i[0] != "0.0":
                cpu.append(float(i[0]) / 8)
                mem.append(float(i[1].split("M")[0]))

        cpuNum = [i for i in range(len(cpu))]
        cpuPic = os.path.join(os.path.dirname(__file__), "mac_cpu.jpg")
        memNum = [i for i in range(len(mem))]
        memPic = os.path.join(os.path.dirname(__file__), "mac_mem.jpg")

        cpu_avg = f"{round(sum(cpu) / len(cpu), 2)}%"
        mem_avg = f"{round(sum(mem) / len(mem), 2)}M"

        Worker.paint(title="MAC_CPU", avg=cpu_avg, y_label="CPU(%)", x_label="Time", x=cpuNum, y=cpu, savefig=cpuPic)
        Worker.paint(title="MAC_MEM", avg=mem_avg, y_label="Mem(M)", x_label="Time", x=memNum, y=mem, savefig=memPic)


if __name__ == '__main__':
    Mac(10).catch()