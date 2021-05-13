import json
import pexpect
import os
from packages import hpcs as hpcs
from packages import custom as custom
import re
import subprocess

# --------------------------------------------
# GET INPUTS From Null resource
# --------------------------------------------
# inputfile = os.environ.get("INPUT_FILE","")
tke_files_path=os.environ.get("CLOUDTKEFILES","")
hpcs_guid = os.environ.get("HPCS_GUID","")
admin1_name = os.environ.get("ADMIN1_NAME", "")
admin1_password = os.environ.get("ADMIN1_PASSWORD", "")
admin2_name = os.environ.get("ADMIN2_NAME", "")
admin2_password = os.environ.get("ADMIN2_PASSWORD", "")
admin_num = os.environ.get("ADMIN_NUM", "")
threshold_value = os.environ.get("THRESHOLD_VALUE", "")
rev_threshold_value = os.environ.get("REV_THRESHOLD_VALUE", "")

# Get HPCS instance number
cmd_exe = subprocess.run(["chmod", "u+x", "hpcs_inst_num.sh"], capture_output=True)
run_command = "./hpcs_inst_num.sh '%s'" % (str(hpcs_guid))
os.system(run_command)
out = subprocess.run(["cat", "./temp.txt"], capture_output=True)
out_num = out.stdout.decode("utf-8")
inst_num = str(out_num.strip())
deletetempfile = subprocess.run(["rm", "-r", "./temp.txt"], capture_output=True)

# print(pexpect.run('ibmcloud iam oauth-tokens'))
# if inputfile == "":
#     print("[ERROR] Unable to read file or Provided file is empty")
# try:
#     with open(inputfile) as complex_data:
#         d = complex_data.read()
#         data = json.loads(d)
#         # print(data)
# except Exception as error:
#     print("[ERROR] Unable to read data from  input file", error)
# else:

#     # --------------------------------------------
#     # Declare JSON input key-values
#     # --------------------------------------------
#     admin1_name=str(data["admin_name"][0])
#     admin1_password=str(data["admin_password"][0])
#     admin2_name=str(data["admin_name"][1])
#     admin2_password=str(data["admin_password"][1])
#     admin_num=str(len(data["admin_name"]))
#     threshold_value = str(data["threshold"])
#     rev_threshold_value = str(data["rev_threshold"])
    
# ----------------------------------------------------------------------------------------
# Create custom directory in the output path provided inorder to avoid misplacement of data
# ----------------------------------------------------------------------------------------
resultDir = custom.custom_tke_files_path(tke_files_path,hpcs_guid)
os.environ['CLOUDTKEFILES'] = resultDir
os.system("echo [INFO] TKE Files will be located at $CLOUDTKEFILES")

# -----------------------------------------------------------------------------------
# List Crypto units and format the output to get guid-crypto_unit_num key-val pair
# -----------------------------------------------------------------------------------
cu_list= hpcs.list_crypto_units()

cu_num_dict = custom.conv_cu_list_dict(cu_list)

cu_num = custom.get_cu_num(hpcs_guid,cu_num_dict)

# --------------------------------------------
# Add Crypto unit
# --------------------------------------------
hpcs.crypto_unit_add(cu_num)

# --------------------------------------------
# HPCS instance initialization with auto-init
# --------------------------------------------
auto_init = hpcs.auto_init(inst_num,threshold_value,rev_threshold_value,admin_num,admin1_name,admin1_password,admin2_name,admin2_password)

