#!/usr/bin/python
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from time import time
import os
from tqdm import tqdm
from ping3 import ping

TIMEOUT = 30
VERBOSE = True
DEBUG = False
PROXY = 'http://1.1.1.1:80'


class เครือข่าย:
    def __init__(self, a=1, b=1, c=1, d=1):
        """
        192.168.0.100
         a . b .c. d
        :param a: บิตแรก 8 บิต
        :param b: บิตถัดไป 8 บิต
        :param c: บิตถัดไป 8 บิต
        :param d: บิตสุดท้าย 8 บิต
        """

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

    def กำหนดซับเน็ต(self, subnet_mask):
        """
        :param subnet_mask: จำนวนบิตเครือข่าย (0-31), ประเภท: int
        """
        subnet_mask = int(subnet_mask)
        sub_a = ''
        sub_b = ''
        sub_c = ''
        sub_d = ''
        byte = 0
        while byte < 32:
            if 0 <= byte <= 7:
                if byte < subnet_mask:
                    sub_a += '0'
                else:
                    sub_a += '1'
            elif 8 <= byte <= 15:
                if byte < subnet_mask:
                    sub_b += '0'
                else:
                    sub_b += '1'
            elif 16 <= byte <= 23:
                if byte < subnet_mask:
                    sub_c += '0'
                else:
                    sub_c += '1'
            elif 24 <= byte <= 31:
                if byte < subnet_mask:
                    sub_d += '0'
                else:
                    sub_d += '1'
            byte += 1
        self.end_a = int(sub_a, 2) | self.start_a
        self.end_b = int(sub_b, 2) | self.start_b
        self.end_c = int(sub_c, 2) | self.start_c
        self.end_d = int(sub_d, 2) | self.start_d

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

    def __gt__(self, other):
        return self.a > other.a and self.b > other.b and self.c > other.c and self.d > other.d

    def __lt__(self, other):
        return self.a < other.a and self.b < other.b and self.c < other.v and self.d < other.d

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.c == other.c and self.d == other.d

    def __str__(self):
        return f'{self.a}.{self.b}.{self.c}.{self.d}'

    def __repr__(self):
        return f'<เครือข่าย เริ่มต้น: {self.start_a}.{self.start_b}.{self.start_c}.{self.start_d}  ' \
               f'สิ้นสุด: {self.end_a}.{self.end_b}.{self.end_c}.{self.end_d}>'

    def __len__(self):
        return (self.end_a - self.start_a or 1) * (self.end_b - self.start_b or 1) * \
               (self.end_c - self.start_c or 1) * (self.end_d - self.start_d or 1)

    @property
    def end_ip(self):
        return f'{self.end_a}.{self.end_b}.{self.end_c}.{self.end_d}'

    @property
    def start_ip(self):
        return f'{self.start_a}.{self.start_b}.{self.start_c}.{self.start_d}'

    def รีเซ็ต(self):
        self.a = self.start_a
        self.b = self.start_b
        self.c = self.start_c
        self.d = self.start_d


def สแกน(ip_host):
    try:
        ping_val = ping(ip_host, size=8)
    except Exception as e:
        ping_val = None
        if DEBUG:
            print(ip_host, e)
        

    if ping_val is not None:
        response = None
        try:
            response = urllib.request.urlopen(
                'http://' + ip_host, timeout=TIMEOUT)
            status_code = response.getcode()
            rv = ip_host
         
        except urllib.error.HTTPError as e:
            rv = ip_host
        except Exception as e:
            if DEBUG:
                print(e)
            rv = ip_host
            

        finally:
            if response is not None:
                response.close()
        return rv
    else:
        return



GREEN = "\033[32m"  # สีเขียวเข้ม
RESET = "\033[0m"  # รีเซ็ตสีกลับเป็นค่าเริ่มต้น

print(f"{GREEN}███████╗██╗  ██╗██████╗  ██████╗ ███╗   ███╗{RESET}")
print(f"{GREEN}██╔════╝██║ ██╔╝██╔══██╗██╔═══██╗████╗ ████║{RESET}")
print(f"{GREEN}█████╗  █████╔╝ ██████╔╝██║   ██║██╔████╔██║{RESET}")
print(f"{GREEN}██╔══╝  ██╔═██╗ ██╔══██╗██║   ██║██║╚██╔╝██║{RESET}")
print(f"{GREEN}███████╗██║  ██╗██║  ██║╚██████╔╝██║ ╚═╝ ██║{RESET}")
print(f"{GREEN}╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝{RESET}")

GREEN = "\033[32m"  # สีเขียว
RESET = "\033[0m"    # รีเซ็ตสีกลับเป็นค่าเริ่มต้น

print(f"{GREEN}▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄{RESET}")
print(f"{GREEN}░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░{RESET}")
BLUE = "\033[34m"  # สีน้ำเงิน (ฟ้า)
RESET = "\033[0m"  # รีเซ็ตสีกลับเป็นค่าเริ่มต้น

print(f"{BLUE}พัฒนาโดย:EKROMVPN{RESET}")
print(f"{BLUE}ID LINE rinnahkap {RESET}")
print(f"{BLUE}FB เครื่องฟื้นฟูแบตเตอรี่{RESET}")

LIGHT_YELLOW = "\033[93m"  # สีเหลืองอ่อน
RESET = "\033[0m"  # รีเซ็ตสีกลับเป็นค่าเริ่มต้น

print(f"{LIGHT_YELLOW}▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄{RESET}")
print ("\n")
ip_start=input("\033[31m" + "กรุณาใส่ ไอพีโฮสต์:" + "\033[0m").split('.')


if len(ip_start[-1].split('/')) == 2:
    subnet = ip_start[-1].split('/')[1]
    ip_start[-1] = ip_start[-1].split('/')[0]
    ip = เครือข่าย(*ip_start)
    ip.กำหนดซับเน็ต(subnet)
else:
    ip_end = input('กรุณาใส่ IP สุดท้ายของเครือข่าย: ').split('.')
    ip = เครือข่าย(*ip_start)
    ip.กำหนดจุดสิ้นสุด(*ip_end)


print("\033[33m" + f"<...กำลังสแกน {ip.start_ip}-{ip.end_ip}...>" + "\033[0m\n")



การตอบสนอง = []
เริ่ม = time()

with ThreadPoolExecutor(max_workers=(os.cpu_count() or 1) * 50) as executor:
    for i in tqdm(executor.map(สแกน, ip), total=len(ip), unit=' IP'):
        if i:
            การตอบสนอง.append(i)
            if VERBOSE:
                print("\033[1;92m" + f"{i}" + "\033[0m",end="")
                print("\033[33m" + " สแกนสำเร็จ ✓" + "\033[0m")
                f=open('ping.txt','a')
                f.write("\033[32m" + f"{i}" + "\033[0m\n")
                f.close()

สิ้นสุด = time()
ใช้เวลา = int(สิ้นสุด - เริ่ม)
print ("\n")
print("\033[35m" + f"⌚ เวลาที่ใช้ในการดำเนินการ:" + "\033[0m",end="")

print("\033[36m" + f" {ใช้เวลา} วินาที" + "\033[0m")
print("\033[2;32m" + "ผลลัพธ์ทั้งหมดถูกบันทึกใน >> ping.txt" + "\033[0m")

