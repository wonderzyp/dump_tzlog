#!/usr/bin/python
'''
Author: wonderzyp
Date: 2024-12-05
Description: Extract TZ log from OCIMEM.BIN(QNX Ramdump)/md_TZ_IMEM.BIN(QNX minidump)
'''

from struct import unpack
import qcom_func as qc
import re
import sys

TZBSP_DIAG_MAGIC_NUM = 0x747A6461

RAW_DIAGBUF = []

RING_BUFFER_OFFSET = 0
RING_BUFFER_START_ADDR = 0
RING_BUFFER_END_ADDR = 0
RES_DIR="tz_resu"

RING_BUFFER_END_OFFSET = 0

def save_log(data, filename):
    with open(filename, "w") as file:
        for line in data:
            file.write(line + "\n")


def reorder_ringbuff(tzlog):
    global RING_BUFFER_START_ADDR
    global RING_BUFFER_END_ADDR
    global RES_DIR

    lines = tzlog.strip().split("\n")
    addresses = []

    first_line = lines[0]
    if not re.match(r'\[([0-9a-fA-Fx]+)\]', first_line):
        lines[-1] += first_line
    
    lines.pop(0)


    for line in lines:
        found_addresses = re.findall(r'\[([0-9a-fA-Fx]+)\]', line)
        addresses.extend(found_addresses)
    
    addresses_int = [int(addr, 16) for addr in addresses]
    for i in range(1, len(addresses_int)):
        if addresses_int[i] < addresses_int[i - 1]:
            print(f"first decreased addr: line {i + 1}, addr {hex(addresses_int[i])}")
            RING_BUFFER_START_ADDR = hex(addresses_int[i])
            RING_BUFFER_END_ADDR = hex(addresses_int[i-1])
            break
    
    print(f"RING_BUFFER_START_ADDR: {RING_BUFFER_START_ADDR}")
    print(f"RING_BUFFER_END_ADDR: {RING_BUFFER_END_ADDR}")

    tzlog_ordered = []
    front_half = []
    bottom_half = []
    bottom__half_flag = True

    for line in lines:
        if bottom__half_flag:
            bottom_half.append(line)
        else:
            front_half.append(line)

        # If the ring buffer is not overwritten, RING_BUFFER_END_ADDR = 0 will not change
        # need to deal with RING_BUFFER_END_ADDR = 0, or A syntax error occurred
        if (not isinstance(RING_BUFFER_END_ADDR, int)) and (f"[{RING_BUFFER_END_ADDR[2:].zfill(9)}]" in line):
            bottom__half_flag = False
    
    tzlog_ordered = front_half + bottom_half
    
    # print("=================After Reordered================")
    for line in tzlog_ordered:
        print(line)
    save_log(tzlog_ordered, f"{RES_DIR}/tz_log_raw.txt")
    

def decode_tz_ringbuf(buffer):
    tzlog = str(buffer[RING_BUFFER_OFFSET:RING_BUFFER_END_OFFSET], 'ascii', errors='ignore')
    tzlog = tzlog.replace("\r\n","\n")
    tzlog = tzlog.replace("\0","")       
    if len(tzlog) != 0:
        print(tzlog)
    
    reorder_ringbuff(tzlog)


def extra_tz_rawlog_buf(diag_buffer):

    buf_offset = 0
    step = 4
    cur_diagbuff = diag_buffer

    while buf_offset + step <= len(diag_buffer):
        if len(cur_diagbuff) >= 4:
            log_value = unpack('<L',cur_diagbuff[0:4])
            if log_value[0] == TZBSP_DIAG_MAGIC_NUM:
                    RAW_DIAGBUF.append(cur_diagbuff)        
                    break
            
        buf_offset += step
        cur_diagbuff = diag_buffer[buf_offset:-1]

    return cur_diagbuff


#----------------------------------------------------------------------------
# Get TZ Ringbuffer Offset and Length
#----------------------------------------------------------------------------
def get_tz_metainfo(buffer):
    global RING_BUFFER_OFFSET
    global RING_BUFFER_END_OFFSET
    unpack_info = qc.build_unpack_structure_string(qc.tzbsp_diag_struct_general_map,1,1)
    interim_data = unpack(unpack_info[1],buffer[0:unpack_info[0]])

    if len(interim_data) == 0:
        raise
    
    qc.fill_unpacked_data(qc.tzbsp_diag_struct_general_map, interim_data, 2)
    for general_info_entry in qc.tzbsp_diag_struct_general_map:
        # print(" %-14s -> [0x%08x]" %(general_info_entry[0],
        #                             general_info_entry[2]))

        if general_info_entry[0] == "RING BUFFER OFFSET    ":
             RING_BUFFER_OFFSET = general_info_entry[2]
        if general_info_entry[0] == "RING BUFFER LENGTH    ":
             RING_BUFFER_END_OFFSET = RING_BUFFER_OFFSET + general_info_entry[2]

if __name__ == "__main__":
    file_path = sys.argv[1]

    file_handle = open(file_path, "rb")
    binary_buff = file_handle.read() # OCIMEM.BIN is not huge, load all at once

    tzbuff = extra_tz_rawlog_buf(binary_buff)
    get_tz_metainfo(tzbuff)

    decode_tz_ringbuf(tzbuff)
