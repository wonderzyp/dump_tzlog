import re

# Data type sizes 
H_WORD                         = 2
WORD                           = 4
D_WORD                         = 8
BYTE                           = 1


tzbsp_diag_struct_general_map = \
                     [["MAGIC NUMBER          ",'I',0], #0
                      ["VERSION               ",'I',0], #4
                      ["CPU COUNT             ",'I',0], #8
                      ["VMID INFO OFFSET      ",'I',0], #12
                      ["BOOT INFO OFFSET      ",'I',0], #16
                      ["RESET INFO OFFSET     ",'I',0], #20
                      ["INTERRUPT INFO OFFSET ",'I',0], #24
                      ["RING BUFFER OFFSET    ",'I',0], #28
                      ["RING BUFFER LENGTH    ",'I',0], #32
                      ["WAKEUP INFO OFFSET    ",'I',0]] #36



def build_unpack_structure_string(p_struct,p_type_pos,p_multiplier):
    l_little_end = "<" # Used to specify the target as little endian
    l_unpack_str = "" 
    l_struct_len = 0
    
    for l_var in p_struct:        
        if l_var[p_type_pos] == 'I': #4
            l_unpack_str += 'I'
            l_struct_len += WORD  
        elif 'I' in l_var[p_type_pos]: #4(*)
            match = re.match(r'I-(\d*)',l_var[p_type_pos])
            if match:
                byte_count = int(match.group(1)) * WORD
                l_struct_len += byte_count
                for index in range(0,int(match.group(1))):
                    l_unpack_str += 'I'
            else:
                return [0,0]
        elif l_var[p_type_pos] == 'B': #1
            l_unpack_str += 'B'
            l_struct_len += BYTE
        elif l_var[p_type_pos] == 'H': #2
            l_unpack_str += 'H'
            l_struct_len += H_WORD
        elif l_var[p_type_pos] == 'Q': #8
            l_unpack_str += 'Q'
            l_struct_len += D_WORD
        elif 'Q' in l_var[p_type_pos]: #8(*)
            match = re.match(r'Q-(\d*)',l_var[p_type_pos])
            if match:
                byte_count = int(match.group(1)) * D_WORD
                l_struct_len += byte_count
                for index in range(0,int(match.group(1))):
                    l_unpack_str += 'Q'
            else:
                return [0,0]
        elif 'S' in l_var[p_type_pos]: #1(*)            
            match = re.match(r'S-(\d*)',l_var[p_type_pos])
            if match:
                byte_count = match.group(1)
                l_struct_len += int(byte_count)                
                l_unpack_str += str(byte_count) + 's'
            else:
                return [0,0]
        else:             
             return [0,0]
    
    if p_multiplier > 1:
        l_tmp_unpack_repeater = l_unpack_str
        for multipler in range(0,p_multiplier-1):  
            l_unpack_str += l_tmp_unpack_repeater
            
        l_struct_len  = l_struct_len * p_multiplier

    l_unpack_str = l_little_end  + l_unpack_str 
    return [l_struct_len,l_unpack_str]       
            
#-------------------------------------------------------------------------------
# Fill unpacked structure at the specified offset of the list passed in
#-------------------------------------------------------------------------------
def fill_unpacked_data(p_container,p_unpacked_data,p_index):    
    l_unpack_index = 0
    for entry in p_container:        
        entry[p_index] = p_unpacked_data[l_unpack_index]
        l_unpack_index += 1