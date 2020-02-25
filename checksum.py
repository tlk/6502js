#!/usr/bin/python3
#
# This script calculates a checksum.
#
# Simulate checksum calculation with the Visual 6502 Simulator:
# - r: reset vector (program start) set to 0x82c
# - steps: run until the last loop
# http://www.visual6502.org/JSSim/expert.html?graphics=false&logmore=Execute&r=082c&steps=41134&a=0&d=000000000000000000000000000000000000000000000000&a=0800&d=78d8a09ca200cad0fd88d0f88589a9aaa2009500d500d034e8e040d0f5a955a2009500d500d025e8e040d0f5a9008539a8a908853a187139c8d0fbe63aa63ae010d0f369ff8539d0074c8b08a200f00ea2339a248f5005a2ab20e608a901aa9aa000a9f78580baa9ff858098186901d0fc88d0f8a9f7858098186901d0fc88d0f8ca10e3e0f4d0f04c0e08a2339aa218868fa2208685a24e8688a000843c843d84358438a2ff86368683868186828aa209950b9515ca10f9a22d8634a2f78680a5875800eac43cf008b6008638a000843cc43cf0fcb60020e608c8c43cd0f6a000843c4cd108863948a580c580d0fa2903c903d0f40878a58029080943858020c60a0983858020c60aa208a90066396a6a09b7853aa5802908053a858020c60aa580297f0903858020c60aa58009c38580cad0d785892868604898488a48248f500fa2aa20e608a638f00320e6084cb20aa000a9ff8582a58029ff09378580a582c582d0ec29c00908853ba580c580d0fa2934053b8537c536f068a536853ba537c80a243bb008100e20c0094cb309302220c0094cb30948b9f30fc535d013c634d00fa535a63ce00bb03420d20aa904853468063bc006d0c8a53785364ce30948b9f30f243b30020980a63ce00bb00d20d20a2980d004a92d853468606868684cb20aa9ffa2099515ca10fba000843d853f85820a853e858120ba0aa2074ab01748863bb98c0fa63de00a9004684c2d0a9515e63da63b68c8ca10e238263e263fa53e8581a53f8582c068d0cca009a209b50bc9fff030d91500f00588304510f6853ba9ff991500a53bc535d017c634d013a535863ba63ce00bb05620d20aa63ba9048534a009ca10c7a009b91500c9ffd027f00ab91500950ba9ff9915008810ea302e863ba63ce00bb026098020d20aa63ba9ff950b4c650aa63ce00bb01220d20aa92d8534a209b50bc9fff0c6ca10f7a58768aa68a86840a20ea583c583d0f8cad0f760488a48a204cad0fd68aa6860c9bad00a48a58049080903858068950029ff30028535e8863c60e900&a=0f8c&d=4c5e49020f1e5341204a0103101f524f29523b0411202c5356533c0512212d5357513d0613222e5b45503e0714232f5c464f3f081524305d624b400916253949614c410a1726314e604d420b1827325a5f49430c192833595448440d1a2034580e47552b1b1c3537381d363a522a390900083909

import mmap
import random
import string

filename = "EPROM_C900KBD_R2_3_29_05_84.bin"
data = ''.join(random.choices(string.ascii_uppercase + string.digits, k=0x470)).encode()
data_location = 0x300
data_location_end = data_location + len(data)
checksum_addr = 0x7f9

def early_checksum(rom):
    checksum = 0x8
    for high in range(0x0, 0x8):
        carry = 0 # cpx clears carry
        for low in range(0x0, 0x100):
            addr = (high << 8) | low
            if addr == checksum_addr:
                return (checksum, carry)
            checksum = rom[addr] + checksum + carry
            carry = checksum >> 8
            checksum &= 0xff
    return (checksum, carry)

def complete_checksum(rom, checksum, carry):
    first_iteration = True

    for high in range((checksum_addr >> 8), 0x8):
        if first_iteration:
            first_iteration = False
        else:
            carry = 0 # cpx clears carry

        for low in range((checksum_addr & 0xff), 0x100):
            addr = (high << 8) | low
            #print("addr", hex(addr))
            checksum = rom[addr] + checksum + carry
            carry = checksum >> 8
            checksum &= 0xff
    return (checksum, carry)

def validate_checksum(rom):
    checksum = 0x8
    for high in range(0x0, 0x8):
        carry = 0 # cpx clears carry
        for low in range(0x0, 0x100):
            addr = (high << 8) | low
            checksum = rom[addr] + checksum + carry
            carry = checksum >> 8
            checksum &= 0xff

    result = checksum + 0xff + carry
    result &= 0xff

    if result == 0:
        print("Done!")
    else:
        print("!mismatch", hex(checksum), carry)

with open(filename, "r+b") as f:
    print("Patching", filename)
    print(" data:", data)
    print(" checksum address:", hex(checksum_addr))

    mm = mmap.mmap(f.fileno(), 0)
    mm[data_location:data_location_end] = data

    (checksum, carry) = early_checksum(mm)

    print(' searching ', end='')
    for val in range(0x0, 0x100):
        print('.', end='')
        mm[checksum_addr] = val
        (chk, ca) = complete_checksum(mm, checksum, carry)
        if chk == 0 and ca == 1:
            break

    print("")
    print(" checksum patch:", hex(mm[checksum_addr]))

    validate_checksum(mm)

    mm.flush()
    mm.close()
