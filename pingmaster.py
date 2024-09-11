from concurrent.futures import ThreadPoolExecutor
from time import time
import os
from tqdm import tqdm
from ping3 import ping

TIMEOUT = 5  # ลดเวลาการ timeout เพื่อลดเวลาสแกน
VERBOSE = True
DEBUG = False

class เครือข่าย:
    def __init__(self, a=1, b=1, c=1, d=1):
        self.a = int(a)
        self.b = int(b)
        self.c = int(c)
        self.d = int(d)
        self.start_a = int(a)
        self.start_b = int(b)
        self.start_c = int(c)
        self.start_d = int(d)
        self.end_a = 255
        self.end_b = 255
        self.end_c = 255
        self.end_d = 255

    def กำหนดจุดสิ้นสุด(self, end_a, end_b, end_c, end_d):
        self.end_a = int(end_a)
        self.end_b = int(end_b)
        self.end_c = int(end_c)
        self.end_d = int(end_d)

    def __iter__(self):
        return self

    def __next__(self):
        self.d += 1
        if self.d > 255:
            self.d = 0
            self.c += 1
            if self.c > 255:
                self.c = 0
                self.b += 1
                if self.b > 255:
                    self.b = 0
                    self.a += 1
                    if self.a > 255:
                        raise StopIteration
        if self.a == self.end_a and self.b == self.end_b and self.c == self.end_c and self.d == self.end_d:
            raise StopIteration
        return f'{self.a}.{self.b}.{self.c}.{self.d}'

    def __str__(self):
        return f'{self.a}.{self.b}.{self.c}.{self.d}'

    def __repr__(self):
        return f'<เครือข่าย เริ่มต้น: {self.start_a}.{self.start_b}.{self.start_c}.{self.start_d}  ' \
               f'สิ้นสุด: {self.end_a}.{self.end_b}.{self.end_c}.{self.end_d}>'

    def __len__(self):
        return (self.end_a - self.start_a or 1) * (self.end_b - self.start_b or 1) * \
               (self.end_c - self.start_c or 1) * (self.end_d - self.start_d or 1)

def สแกน(ip_host):
    try:
        ping_val = ping(ip_host, size=4, timeout=TIMEOUT)  # ลดขนาดแพ็กเก็ตและ timeout
    except Exception as e:
        ping_val = None
        if DEBUG:
            print(ip_host, e)
    return ip_host if ping_val is not None else None

GREEN = "\033[32m"
RESET = "\033[0m"

print(f"{GREEN}███████╗██╗  ██╗██████╗  ██████╗ ███╗   ███╗{RESET}")
print(f"{GREEN}██╔════╝██║ ██╔╝██╔══██╗██╔═══██╗████╗ ████║{RESET}")

ip_start = input("\033[31m" + "กรุณาใส่ ไอพีโฮสต์:" + "\033[0m").split('.')

ip_end = input('กรุณาใส่ IP สุดท้ายของเครือข่าย: ').split('.')
ip = เครือข่าย(*ip_start)
ip.กำหนดจุดสิ้นสุด(*ip_end)

print("\033[33m" + f"<...กำลังสแกน {ip.start_ip}-{ip.end_ip}...>" + "\033[0m\n")

การตอบสนอง = []
เริ่ม = time()

with ThreadPoolExecutor(max_workers=(os.cpu_count() or 1) * 100) as executor:  # เพิ่มจำนวนเธรดเป็น 100
    for i in tqdm(executor.map(สแกน, ip), total=len(ip), unit=' IP'):
        if i:
            การตอบสนอง.append(i)
            if VERBOSE:
                print("\033[1;92m" + f"{i}" + "\033[0m",end="")
                print("\033[33m" + " สแกนสำเร็จ ✓" + "\033[0m")

สิ้นสุด = time()
ใช้เวลา = int(สิ้นสุด - เริ่ม)
print("\n")
print(f"⌚ เวลาที่ใช้ในการดำเนินการ: {ใช้เวลา} วินาที")
