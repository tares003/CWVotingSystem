import sys
import os
import subprocess
from subprocess import Popen, PIPE
import threading


class LocalShell(object):
    def __init__(self):
        pass

    def run(self):
        env = os.environ.copy()
        p = Popen('/bin/bash', stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT, shell=True, env=env)
        sys.stdout.write("Started Local Terminal...\r\n\r\n")

        def writeall(p):
            while True:
                # print("read data: ")
                data = p.stdout.read(1).decode("utf-8")
                if not data:
                    break
                sys.stdout.write(data)
                sys.stdout.flush()

        writer = threading.Thread(target=writeall, args=(p,))
        writer.start()

        try:
            while True:
                d = sys.stdin.read(1)
                if not d:
                    break
                self._write(p, d.encode())

        except EOFError:
            pass

    def _write(self, process, message):
        process.stdin.write(message)
        process.stdin.flush()


shell = LocalShell()
shell.run()