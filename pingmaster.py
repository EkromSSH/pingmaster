#!/usr/bin/python
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from time import time
import os
from tqdm import tqdm
from ping3 import ping

# ตั้งค่าตัวแปรพื้นฐาน
TIMEOUT = 30  # ระยะเวลารอการเชื่อมต่อ
VERBOSE = True  # แสดงข้อมูลเพิ่มเติม
DEBUG = False  # แสดงข้อความดีบัก
PROXY = 'http://1.1.1.1:80'  # พร็อกซี (หากจำเป็น)

class เครือข่าย:
    def __init__(self, a=1, b=1, c=1, d=1):
        """
        ตัวอย่าง: 192.168.0.100
        a.b.c.d
        :param a: บิตแรก 8 บิต
        :param b: บิตที่สอง 8 บิต
        :param c: บิตที่สาม 8 บิต
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

    def ตั้งค่าจุดสิ้นสุด(self, end_a, end_b, end_c, end_d):
        self.end_a = int(end_a)
        self.end_b = int(end_b)
        self.end_c = int(end_c)
        self.end_d = int(end_d)

    def ตั้งค่าซับเน็ต(self, subnet_mask):
        """
        :param subnet_mask: จำนวนบิตของเครือข่าย (0-31), ประเภท: int
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
        return self.a > other.aและ self.b > other.bและ self.c > other.cและ self.d > other.d

    def __lt__(self, other):
        return self.a < other.aและ self.b < other.bและ self.c < other.cและ self.d < other.d

    def __eq__(self, other):
        return self.a == other.aและ self.b == other.bและ self.c == other.cและ self.d == other.d

    def __str__(self):
        return f'{self.a}.{self.b}.{self.c}.{self.d}'

    def __repr__(self):
        return f'<เครือข่าย เริ่มต้น: {self.start_a}.{self.start_b}.{self.start_c}.{self.start_d} สิ้นสุด: {self.end_a}.{self.end_b}.{self.end_c}.{self.end_d}>'

    def __len__(self):
        return (self.end_a - self.start_a or 1) * (self.end_b - self.start_b or 1) * \
               (self.end_c - self.start_c or 1) * (self.end_d - self.start_d or 1)

    @property
    def ip_สิ้นสุด(self):
        return f'{self.end_a}.{self.end_b}.{self.end_c}.{self.end_d}'

    @property
    def ip_เริ่มต้น(self):
        return f'{self.start_a}.{self.start_b}.{self.start_c}.{self.start_d}'

    def รีเซ็ต(self):
        self.a = self.start_a
        self.b = self.start_b
        self.c = self.start_c
        self.d = self.start_d


def สแกน(ip_host):
    try:
        ค่า_ping = ping(ip_host, size=8)
    except Exception as e:
        ค่า_ping = None
        if DEBUG:
            print(ip_host, e)
        

    if ค่า_ping is not None:
        การตอบสนอง = None
        try:
            การตอบสนอง = urllib.request.urlopen('http://' + ip_host, timeout=TIMEOUT)
            รหัสสถานะ = การตอบสนอง.getcode()
            ผลลัพธ์ = ip_host
         
        except urllib.error.HTTPError as e:
            ผลลัพธ์ = ip_host
        except Exception as e:
            if DEBUG:
                print(e)
            ผลลัพธ์ = ip_host
            

        finally:
            if การตอบสนอง is not None:
                การตอบสนอง.close()
        return ผลลัพธ์
    else:
        return

# การแสดงผลหน้าจอ
print("\033[1;35m╔═══╗──────╔═╗╔═╗─────╔╗\n║╔═╗║──────║║╚╝║║────╔╝╚╗\n║╚═╝╠╦═╗╔══╣╔╗╔╗╠══╦═╩╗╔╬══╦═╗\n║╔══╬╣╔╗╣╔╗║║║║║║╔╗║══╣║║║═╣╔╝\n║║──║║║║║╚╝║║║║║║╔╗╠══║╚╣║═╣║\n╚╝──╚╩╝╚╩═╗╠╝╚╝╚╩╝╚╩══╩═╩══╩╝\n────────╔═╝║\n────────╚══╝\033[0m")
print("▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄")
print("░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░")
print("\033[1;36mพัฒนาโดย: EKROMVPN\033[0m")
print("\033[1;32mTelegram: @Akucinta\033[0m")
print("\033[1;34mYouTube: @EKROM\033[0m")
print("▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄▄ ▄")
print("\n")
ip_เริ่มต้น = input("\033[1;31mกรุณาใส่ IP โฮสต์: \033[0m").split('.')

if len(ip_เริ่มต้น[-1].split('/')) == 2:
    ซับเน็ต = ip_เริ่มต้น[-1].split('/')[1]
    ip_เริ่มต้น[-1] = ip_เริ่มต้น[-1].split('/')[0]
    ip = เครือข่าย(*ip_เริ่มต้น)
    ip.ตั้งค่าซับเน็ต(ซับเน็ต)
else:
    ip_สิ้นสุด = input('กรุณาใส่ IP สุดท้ายของเครือข่าย: ').split('.')
    ip = เครือข่าย(*ip_เริ่มต้น)
    ip.ตั้งค่าจุดสิ้นสุด(*ip_สิ้นสุด)

print("\033[1;33m<...กำลังสแกน {ip.เริ่ม_ip}-{ip.สิ้นสุด_ip}...>\033[0m\n")

การตอบสนอง = []
เริ่ม = time()

with ThreadPoolExecutor(max_workers=(os.cpu_count() or 1) * 50) as executor:
    for i in tqdm(executor.map(สแกน, ip), total=len(ip), unit=' IP'):
        if i:
            การตอบสนอง.append(i)
            if VERBOSE:
                print("\033[1;92m" + f"{i}" + "\033[0m",end="")
                print("\033[1;33m" + " สแกนสำเร็จ ✓" + "\033[0m")
                with open('ping.txt', 'a') as f:
                    f.write(f"{i}\n")

สิ้นสุด = time()
ใช้เวลา = int(สิ้นสุด - เริ่ม)
print("\n")
print("\033[1;35m⌚ เวลาในการดำเนินการ: \033[0m", end="")
print("\033[1;36m" + f" {ใช้เวลา} วินาที" + "\033[0m")
print("\033[2;32mผลลัพธ์สะสม >> สิ้นสุดการสแกน\033[0m")
