import os
import xml.dom.minidom
import pandas as pd
from datetime import datetime
from datetime import timedelta
import glob

def Split_trx(trxfiles,path):
    install_test_trx_names = []
    for trx in trxfiles:
        xml_doc = xml.dom.minidom.parse(path + "\\" + trx)
        test_definitions = xml_doc.getElementsByTagName("TestDefinitions")
        for test_definition in test_definitions:
            unit_tests = test_definition.getElementsByTagName("UnitTest")
            for unit_test in unit_tests:
                storage_value = unit_test.getAttribute("storage")
                if storage_value == r"c:\temp\ui.automation\ncr.uiautomation.installtests.dll":
                    install_test_trx_names.append(trx)
                    break
    return install_test_trx_names
def Installation_result(lab_name,trxfiles,path):
    data = []
    data_unit = []
    for trx in trxfiles:
        duration_trx = timedelta()
        xml_doc = xml.dom.minidom.parse(path + "\\" + trx)
        # collect unit test data
        results = xml_doc.getElementsByTagName("Results")
        for res in results:
            TestResult = res.getElementsByTagName("TestResultAggregation")
            for i in TestResult:
                InnerResults = i.getElementsByTagName("InnerResults")
                for t in InnerResults:
                    UnitTestResult = t.getElementsByTagName("UnitTestResult")
                    for k in UnitTestResult:
                        p = trx.split(",")
                        parent = p[0]
                        type = 'install_test'
                        test_name = k.getAttribute("testName")
                        test_outcome = k.getAttribute("outcome")
                        test_duration = k.getAttribute("duration")
                        test_start_time = k.getAttribute("startTime")
                        test_end_time = k.getAttribute("endTime")
                        Errormessage = None
                        ErrorStackTrace = None
                        if (test_duration != ''):
                            duration_trx += timedelta(hours=int(test_duration[:2]), minutes=int(test_duration[3:5]),
                                                      seconds=float(test_duration[6:8]))
                        output = k.getElementsByTagName("Output")
                        for e in output:
                            errorinfo = e.getElementsByTagName("ErrorInfo")
                            for m in errorinfo:
                                message = m.getElementsByTagName("Message")[0]
                                Errormessage = message.firstChild.nodeValue.strip()
                                StackTrace = m.getElementsByTagName("StackTrace")[0]
                                ErrorStackTrace = StackTrace.firstChild.nodeValue.strip()
                        data_unit.append({
                            'Lab_name': lab_name,
                            'parent': parent,
                            'type': type,
                            'test_name': test_name,
                            'test_outcome': test_outcome,
                            'test_duration': test_duration,
                            'test_start_time': test_start_time,
                            'test_end_time': test_end_time,
                            'Errormessage': Errormessage,
                            'ErrorStackTrace': ErrorStackTrace
                        })

        res = xml_doc.getElementsByTagName("ResultSummary")
        for i in res:
            c = i.getElementsByTagName("Counters")
            for i in c:
                count = i.getAttribute("total")
                passed = i.getAttribute("passed")
                failed = i.getAttribute("failed")
                data.append({
                    'Lab_Name': lab_name,
                    'Test_Name': trx,
                    'Type': 'Install_Test',
                    'Total': count,
                    'Passed': passed,
                    'Failed': failed,
                    'duration': str(duration_trx)
                })
                break

    df_unit_tests = pd.DataFrame(data_unit)
    df_summary_install = pd.DataFrame(data)
    return df_summary_install, df_unit_tests
def Get_Trx_Files(lab_name, path):
    # list to store files
    trxfiles = []
    # Iterate directory
    for file in os.listdir(path):
        if file.endswith('.trx') & file.startswith(lab_name):
            trxfiles.append(file)

    if len(trxfiles) != 0:
        install_files = Split_trx(trxfiles,path)
        l_summary_df = Installation_result(lab_name,install_files,path)[1]
        summary_df = pd.DataFrame(l_summary_df)
        summary_df.reset_index(drop=True, inplace=True)
        return summary_df
    return None, None
def Get_Error_Txt(lab_name, path):
    # list to store files
    errorFiles = []
    # Iterate directory
    for file in os.listdir(path):
        if file.endswith('err.txt') & file.startswith(lab_name):
            errorFiles.append(file)

    errors_list = []
    if len(errorFiles) != 0:
        for f in errorFiles:
            f_path = os.path.join(path, f)
            with open(f_path, 'r') as firstfile:
                for line in firstfile:
                    errors_list.append(line)

    errors_data = "".join(errors_list)
    return errors_data
def Get_Data(summary_df,globalOutputTrxFolder,lab_name):

    if(summary_df != (None,None)):
        failed_trx_df = summary_df[summary_df['test_outcome'] == 'Failed']
        install_trx = summary_df['parent'].unique()
        failed_trx = failed_trx_df['parent'].unique()
        failed_tests = failed_trx_df['test_name'].values
        errors = failed_trx_df['Errormessage'].values
        stacktrace = failed_trx_df['ErrorStackTrace'].values
        script_error = Get_Error_Txt(lab_name, globalOutputTrxFolder)
    else:
        script_error = Get_Error_Txt(lab_name, globalOutputTrxFolder)
        data = {
            'ES' : script_error
        }
        return data
    # Convert the arrays to lists
    install_trx = list(install_trx)
    failed_trx = list(failed_trx)
    failed_tests = list(failed_tests)
    errors = list(errors)
    stacktrace = list(stacktrace)

    data = {
        'install_trx': install_trx[0],
        'failed_trx': failed_trx[0],
        'failed_tests': failed_tests[0],
        'errors': errors[0],
        'stacktrace': stacktrace[0],
        'script_error': script_error
    }
    return data
def Delete_files(log, folder):
    try:
        # Delete the log file
        if os.path.exists(log):
            os.remove(log)
            print(f"Log file {log} deleted.")

        # Delete the folder and its contents
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    os.rmdir(dir_path)
            os.rmdir(folder)
            print(f"Folder {folder} and its contents deleted.")
        else:
            print(f"Folder {folder} does not exist.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
def main(globalDeploymentLogFile,globalOutputTrxFolder,lab_name):
    # globalDeploymentLogFile = 'C:\TempPersonal\global.deployment.2023-10-24T10-29-57.6487.log'
    # globalOutputTrxFolder = 'C:\TempPersonal\2023-10-24T10-30-59'
    # lab_name = 'LAB_ATF'

    summary_df = Get_Trx_Files(lab_name, globalOutputTrxFolder)
    data = Get_Data(summary_df,globalOutputTrxFolder,lab_name)
    Delete_files(globalDeploymentLogFile, globalOutputTrxFolder)
    if 'errors' in data:
        if data['errors'] == '' and data['script_error'] == '':
            Delete_files(globalDeploymentLogFile, globalOutputTrxFolder)
            #if something went wrong save the logs

    return data

if __name__ == '__main__':
    data = main()
