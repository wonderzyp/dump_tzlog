#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <PATH-To-OCIMEM.BIN>"
    exit 1
fi

res_dir="tz_resu"

if [ -d "$res_dir" ]; then
    echo "Clean the res dir"
    rm -rf "$res_dir"
fi

mkdir "$res_dir"

ocimem_file=$1
./get_raw_tzlog.py $1

# Enable the following lines after preparation
# python3 ./tz_log_decoder.py -e ./errorCodesDict.txt -l "./$res_dir/tz_log_raw.txt" -o "./$res_dir/tz_log_decode.txt"
# python3 ./noc_err_decode.py -i $res_dir/tz_log_decode.txt -o $res_dir/noc_res.txt -c makena -n ./NoC_Error_Decode_QNOC4/NoC_error_decode_log.py

# python3 ./tz_diag_parser.py $ocimem_file
# mv ./tz_diag_log.txt $res_dir/
# mv ./tz_debug_scan_out.txt $res_dir/

echo "The result is generated in ./tz_resu/"