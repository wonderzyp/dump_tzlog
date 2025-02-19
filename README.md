## Extract TZ log

### Intro
This tool support extract tz raw log from QNX Ramdump/Minidump. 

### Usage
```bash
# Ramdump
./decode_tz.sh ./OCIMEM.BIN 

# Minidump
./decode_tz.sh ./md_TZ_IMEM.BIN
```
The raw tz log will generate as ./tz_resu/tz_log_raw.txt


If you want to decode tz raw log, the following files is necessary:
```bash
.
├── decode_tz.sh
├── errorCodesDict.txt
├── get_raw_tzlog.py
├── noc_err_decode.py
├── NoC_Error_Decode_QNOC4
│   ├── data_makena.py
│   ├── DDRSS_error_decode.py
│   ├── NoC_error_decode_log.py
│   └── NoC_error_decode.py
├── qcom_func.py
├── tz_diag_parser.py
├── tz_log_decoder.py
```
After preparation, you can enable the some lines in `decode_tz.sh`, and re-execute that.

Some useful files will be generated in tz_resu:
```bash
noc_res.txt
tz_diag_log.txt
tz_log_decode.txt
```

