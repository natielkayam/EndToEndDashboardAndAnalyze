import re
import os
import shutil
from ftplib import FTP
import logging
import pandas as pd
def getFilecontent(filename):
    try:
        # Download the file
        with open(filename, 'wb') as local_file:
            ftp.retrbinary('RETR ' + filename, local_file.write)
        # Read the content of the file
        with open(filename, 'r') as file:
            file_content = file.read()
        logging.info("Get file content from "+filename+" successfully")
        return file_content
    except Exception as Argument:
        logging.exception("Error occurred in getFilecontent func "+Argument)
        return None
def getGlobal(filename):
    try :
        # regular expressions to find the value after "-GlobalLogFileName"
        match = re.search(r'-GlobalLogFileName\s*\s+(\S+)', getFilecontent(filename))
        if match:
            global_log_file_name = os.path.basename(match.group(1))
            os.remove(filename)
            logging.info("Get GlobalLogFileName successfully")
        else:
            os.remove(filename)
            logging.error("GlobalLogFileName not found in the file.")
        return global_log_file_name
    except Exception as Argument:
        logging.exception("Error occurred in getGlobal func")
        return None
def getTrxFolder(globaldata):
    try :
        value = None
        search_string = "Folder where all TRX and logs will be saved is: "
        # Read the content of the local file line by line
        for line in globaldata.splitlines():
            if search_string in line:
                value = line.split(search_string, 1)[1].strip()
                logging.info("Get foldertrx name successfully from globalfile : "+os.path.basename(value))
                break
        if value == None :
            logging.error("not find foldertrx name from global file")
        return os.path.basename(value)
    except Exception as Argument:
        logging.exception("Error occurred in getGlobal func "+Argument)
        return None
def getInstallations(globaldata):
    keys_to_extract = [
        "UiAutomationReleaseName",
        "StoreOfficeReleaseName",
        "CCMOfficeReleaseName",
        "GPosWebServerReleaseName",
        "PaymentEmulatorReleaseName",
        "POSClientReleaseName",
        "ForecourtReleaseName",
        "StoreGposReleaseName",
        "CCMGposReleaseName"
    ]
    extracted_values = {}
    # Use regular expressions to find and extract the values
    for key in keys_to_extract:
        pattern = re.compile(rf"{key}\s+(.+)")
        match = pattern.search(globaldata)
        if match:
            extracted_values[key] = match.group(1)
    return extracted_values
def getStates(globaldata):
    datalabs2 = ['LAT_I_09', 'LAT_G_07', 'LAT_P_16', 'LAT_B_02', 'LAT_W_23', 'LAT_O_15', 'LAT_Q_17', 'LAT_H_08',
                 'LAT_K_11', 'LAT_A_01', 'LAT_F_06', 'LAT_C_03', 'LAT_D_04', 'LAT_V_22', 'LAT_S_19',
                 'LAT_N_14', 'LAT_L_12', 'LAT_M_13', 'LAT_R_18', 'LAT_U_21', 'LAT_T_20', 'LAT_J_10']
    states = {}
    for lab_name in datalabs2:
        logging.info("start get state for : " + lab_name)
        if lab_name+' Completed' in globaldata:
            states[lab_name] = 'Completed'
        else:
            states[lab_name] = 'Running'
    return states
def getRunDate(globaldata):
    #get run date
    pattern = r'\[(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}\.\d{4})\]'
    dates = re.findall(pattern, globaldata)
    if dates:
        rundate = dates[0].split(".")[0]
        return rundate
    else:
        return None
def getDataGlobal(filename):
    try :
        globalfile = getGlobal(filename)
        ftp.cwd('..') #back to temp
        globaldata = getFilecontent(globalfile)
        data = {
            "trxFolder" : getTrxFolder(globaldata)
        }
        installations = getInstallations(globaldata)
        states = getStates(globaldata)
        rundate = getRunDate(globaldata)
        logging.info("Get Data from getDataGlobal done")
        os.remove(globalfile)
        logging.info("delete global file from os done succsesfully")
        if data == None:
            logging.error("Failed to get data from the globalfile in getDataGlobal func")
        return data, installations, states, rundate
    except Exception as Argument:
        logging.exception("Error occurred in getGlobal func")
        return None
def downloadTrx(trxFolder):
    ftp.cwd(trxFolder)
    file_list = ftp.mlsd()
    global local_directory
    local_directory = 'C:\Dashboard\TempSet02'
    #clean the directory
    if os.path.exists(local_directory):
        shutil.rmtree(local_directory, ignore_errors=False)
    os.makedirs(local_directory, exist_ok=True)
    # Iterate through the remote file list
    for filename, attrs in file_list:
        if filename.endswith('.trx'):
            local_file_path = os.path.join(local_directory, filename)
            with open(local_file_path, 'wb') as local_file:
                ftp.retrbinary('RETR ' + filename, local_file.write)
        if filename.endswith('err.txt') and int(attrs['size']) > 0:
            local_file_path = os.path.join(local_directory, filename)
            with open(local_file_path, 'wb') as local_file:
                ftp.retrbinary('RETR ' + filename, local_file.write)
def main():
    script_filename = os.path.splitext(os.path.basename(__file__))[0]
    logging.info(f"------------------- {script_filename} --------------------")
    global ftp
    ftp = FTP('XXXXXXX')
    ftp.login(user='Temp', passwd='Temp')
    ftp.cwd('/Temp/Report')

    filename = 'GenerateReport.Set02.ps1'
    data,installations,states,rundate = getDataGlobal(filename)
    df_installations = pd.DataFrame.from_dict([installations])
    df_states = pd.DataFrame.from_dict([states])
    downloadTrx(data["trxFolder"])
    # Close the FTP connection
    ftp.quit()
    return local_directory,df_installations,df_states,rundate

#TODO:
# read the genreate
# extract global
# extract from global the setid,trxfolder , installations
if __name__ == '__main__':
    main()
