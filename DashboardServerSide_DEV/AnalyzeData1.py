import os
import xml.dom.minidom
import pandas as pd
from datetime import datetime
from datetime import timedelta
import glob
import logging
import FtpScript1

# split the trx to installtion and tests
def Split_trx(trxfiles):
    install_test_trx_names = []
    test_trx_names = []
    for trx in trxfiles:
        xml_doc = xml.dom.minidom.parse(path + "\\" + trx)
        test_definitions = xml_doc.getElementsByTagName("TestDefinitions")
        for test_definition in test_definitions:
            unit_tests = test_definition.getElementsByTagName("UnitTest")
            for unit_test in unit_tests:
                storage_value = unit_test.getAttribute("storage")
                if storage_value != r"c:\temp\ui.automation\ncr.uiautomation.installtests.dll":
                    test_trx_names.append(trx)
                    break
                else:
                    install_test_trx_names.append(trx)
                    break
    return install_test_trx_names, test_trx_names
# get result of instalation tests
def Installation_result(lab_name,trxfiles):
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
# get result of tests
def Get_tests_results(lab_name,trxfiles):
    data = []
    data_unit = []
    for trx in trxfiles:
        duration_trx = timedelta()
        xml_doc = xml.dom.minidom.parse(path + "\\" + trx)
        # collect unit test data
        results = xml_doc.getElementsByTagName("Results")
        for res in results:
            unit_test_result = res.getElementsByTagName("UnitTestResult")
            for k in unit_test_result:
                p = trx.split(",")
                parent = p[0]
                type = 'test'
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
                        if test_outcome == 'Timeout':
                            ErrorStackTrace = "Failed get StackTrace"
                        else :
                            StackTraceElements = m.getElementsByTagName("StackTrace")
                            if len(StackTraceElements) > 0:
                                StackTrace = StackTraceElements[0]
                                ErrorStackTrace = StackTrace.firstChild.nodeValue.strip()
                            else:
                                #StackTrace = m.getElementsByTagName("StackTrace")
                                ErrorStackTrace = ""
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
                    'Type': 'Test',
                    'Total': count,
                    'Passed': passed,
                    'Failed': failed,
                    'duration': str(duration_trx)
                })
    df_summary_tests, df_unit_tests = None, None
    if len(data_unit) != 0:
        df_unit_tests = pd.DataFrame(data_unit)
    if len(data) != 0:
        df_summary_tests = pd.DataFrame(data)
    return df_summary_tests, df_unit_tests
# main function that deals with all trx
def Get_Trx_Files(lab_name, path):
    # list to store files
    trxfiles = []
    # Iterate directory
    for file in os.listdir(path):
        if file.endswith('.trx') & file.startswith(lab_name):
            trxfiles.append(file)

    if len(trxfiles) != 0:
        install_files, test_files = Split_trx(trxfiles)
        l_summary_df = [Installation_result(lab_name,install_files)[0], Get_tests_results(lab_name,test_files)[0]]
        l_unit_df = [Installation_result(lab_name,install_files)[1], Get_tests_results(lab_name,test_files)[1]]
        summary_df = pd.concat(l_summary_df)
        summary_df.reset_index(drop=True, inplace=True)
        unit_df = pd.concat(l_unit_df)
        unit_df.reset_index(drop=True, inplace=True)
        return summary_df, unit_df
    return None, None
def Get_Error_Txt(lab_name, path):
    # list to store files
    errorFiles = []
    # Iterate directory
    for file in os.listdir(path):
        if file.endswith('err.txt') & file.startswith(lab_name):
            errorFiles.append(file)
    return errorFiles
def Get_Configuration():
    datalabs1 = ['LAB_UIR', 'LAB_ATQ', 'LAB_ATA', 'LAB_ATR', 'LAB_UIC', 'LAB_UII', 'LAB_UIS', 'LAB_UIO',
                'LAB_UIG', 'LAB_UIU', 'LAB_ATL', 'LAB_UIV', 'LAB_ATH', 'LAB_ATB', 'LAB_UIK', 'LAB_ATD', 'LAB_UIF',
               'LAB_UIJ', 'LAB_UIN', 'LAB_ATM', 'LAB_UIP', 'LAB_UIE', 'LAB_UID', 'LAB_ATC', 'LAB_UIL']
    return datalabs1
def Get_Path_installations_states_rundate():
    logging.info("run FtpScript1.py in order to get path from FTP")
    path,df_installations,df_states,rundate = FtpScript1.main()
    logging.info("got path : " + path)
    logging.info(f"------------------- {script_filename} --------------------")
    return path,df_installations,df_states,rundate
def StoreDF():
    try:
        global path
        path, df_installations,df_states,rundate = Get_Path_installations_states_rundate()
        set_versions(df_installations)
        logging.info("working on setid : 01")
        lab_config = Get_Configuration()
        # Create a folder for states if it doesn't exist
        States_folder = os.path.join(path, "States_Set01")
        os.makedirs(States_folder)
        logging.info("make folder for States_Set01 in path : " + path)
        df_states.to_csv(os.path.join(States_folder, f'States_Set01.csv'), index=False)
        logging.info("save df_states as CSV for States_Set01 in path : " + States_folder)
        # Create an empty dictionary to store DataFrames
        summary_dfs = {}
        units_dfs = {}
        for lab_name in lab_config:
            try:
                logging.info("start work on : "+lab_name)
                # Create DataFrame using Get_Trx_Files function
                summary_df, unit_df = Get_Trx_Files(lab_name, path)
                erros = Get_Error_Txt(lab_name, path)
                logging.info("got trx files for lab : "+lab_name)
                if summary_df is None or unit_df is None:
                    logging.error("DF for "+lab_name+" is NONE")
                    continue
                # Create a folder for the lab if it doesn't exist
                lab_folder = os.path.join(path, lab_name)
                os.makedirs(lab_folder)
                logging.info("make folder for "+lab_name+" in path : "+path)
                if len(erros) != 0:
                    for f in erros:
                        original = os.path.join(path, f)
                        file_path = os.path.join(lab_folder, f)
                        with open(original, 'r') as firstfile, open(file_path, 'a') as secondfile:
                            for line in firstfile:
                                secondfile.write(line)
                            logging.info("save error file for "+lab_name+" : "+f)

                summary_df.reset_index(inplace=True)
                summary_df.rename(columns={'index': 'id'}, inplace=True)
                summary_df.to_csv(os.path.join(lab_folder, f'summary_df_{lab_name}.csv'), index=False)
                summary_df.drop(columns= ['id'], inplace= True)
                logging.info("save summary_df as CSV for "+lab_name+" in path : "+lab_folder)
                unit_df.reset_index(inplace=True)
                unit_df.rename(columns={'index': 'id'}, inplace=True)
                unit_df.to_csv(os.path.join(lab_folder, f'unit_df_{lab_name}.csv'), index=False)
                unit_df.drop(columns= ['id'], inplace= True)
                logging.info("save unit_df as CSV for "+lab_name+" in path : "+lab_folder)
                # Assign the DataFrame to the dictionary with a dynamic key
                summary_dfs[f'summary_df_{lab_name}'] = summary_df
                units_dfs[f'unit_df_{lab_name}'] = unit_df
            except Exception as Argument:
                logging.exception(Argument)
        summary_dfs_all = {key: value for key, value in summary_dfs.items()}
        units_dfs_all = {key: value for key, value in units_dfs.items()}
        set_all(summary_dfs_all,df_states)
        #delete all trx files
        # Use glob to find all .trx files in the directory
        trx_files = glob.glob(os.path.join(path, '*.trx'))
        logging.info("list of trx to deleted : "+str(trx_files))
        txt_files = glob.glob(os.path.join(path, '*.txt'))
        logging.info("list of trx to deleted : "+str(txt_files))
        # Iterate over the list of .trx files and delete each one
        for file_path in trx_files:
            try:
                os.remove(file_path)
                logging.info(str(os.path.basename(file_path))+" deleted")
            except Exception as e:
                logging.exception(e)
        for file_path in txt_files:
            try:
                os.remove(file_path)
                logging.info(str(os.path.basename(file_path))+" deleted")
            except Exception as e:
                logging.exception(e)
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        file_path_date = os.path.join(path, 'dateUpdate01.txt')
        with open(file_path_date, "w") as f:
            f.write(str(date))
        file_path_rundate = os.path.join(path, 'rundate01.txt')
        with open(file_path_rundate, "w") as f:
            f.write(str(rundate))
        logging.info("Done AnalyzeData to path : "+path)
        return  summary_dfs_all,units_dfs_all
    except Exception as Argument:
        logging.exception(Argument, lab_name,)
        return None
def set_versions(df_installations):
    versions_name = 'Versions_Set01'
    # Create a folder for the lab if it doesn't exist
    lab_folder = os.path.join(path, versions_name)
    os.makedirs(lab_folder)
    logging.info("make folder for " + versions_name + " in path : " + path)
    df_installations.to_csv(os.path.join(lab_folder, f'df_installations_{versions_name}.csv'), index=False)
    logging.info("save df_installations as CSV for " + versions_name + " in path : " + lab_folder)
def Get_DLL(lab):
    labs_dll = {
        'LAB_UIR': ["R1","GovernmentProgram"],
        'LAB_ATQ': ["Tax"],
        'LAB_ATA': ["Office1"],
        'LAB_ATR': ["Office1","Organization","PatronID","Product","QSR","R1","Receipt","Return","Return1","Sanity","Selling","Selling1","Tax","TenderExchange","FLSCO","Pharmacy"],
        'LAB_UIC': ["Payment"],
        'LAB_UII': ["individualwrapper","datetimemanipulator","office"],
        'LAB_UIS': ["selling1"],
        'LAB_UIO': ["fuelepsilon1","fuelepsilon","fuel"],
        'LAB_UIG': ["selling"],
        'LAB_UIU': ["return1"],
        'LAB_ATL': ["StoredValue","BRM"],
        'LAB_UIV': ["twostores","draweraccountability"],
        'LAB_ATH': ["fueldraweraccountability","manualfuel","fuel3"],
        'LAB_ATB': ["fuel2","fuelpromotions"],
        'LAB_UIK': ["receipt","datapattern","return","patronid"],
        'LAB_ATD': ["TenderItemRestriction","Payment","AgeRestriction","BRM","CashOffice","CustomerScale","DataPattern","DateTimeManipulator","EndOfDay","EPS","FiPayment","Fuel1","GovernmentProgram","IDM","Localization","Menus","Office","Selling2"],
        'LAB_UIF': ["FiPayment","TenderItemRestriction","TenderExchange","FLSCO"],
        'LAB_UIJ': ["FuelBaseConfig"],
        'LAB_UIN': ["toggletransaction","cashieraccountability"],
        'LAB_ATM': ["fuelcashieraccountability","fuelmtx","fuelcouponue","fuelepsilon1"],
        'LAB_UIP': ["Selling2","CatalogPricesPE"],
        'LAB_UIE': ["EPS","Organization","CustomerScale","AgeRestriction","PromotionsUE","FiPaymentUE"],
        'LAB_UID': ["product","epsilon","pharmacy","idm","coindispenser"],
        'LAB_ATC': ["fuel1"],
        'LAB_UIL': ["endofday","cashoffice"],
    }
    s = ", ".join(str(x) for x in labs_dll[lab])
    return s
def set_all(df_summary,df_states):
    data_summary = []
    for df in df_summary.values() :
        LabName = ""
        num_install = 0
        num_install_failed = 0
        num_install_passed = 0
        num_tests = 0
        num_tests_failed = 0
        num_tests_passed = 0
        #tests_dll = ""
        duration = timedelta()
        for row,name in df.iterrows():
            LabName = df.at[row,'Lab_Name']
            state = df_states[LabName].iloc[0]
            duration_parts = df.at[row, 'duration'].split(':')
            if df.at[row,'Type'] == 'Install_Test':
                num_install += int(df.at[row,'Total'])
                num_install_failed += int(df.at[row,'Failed'])
                num_install_passed += int(df.at[row,'Passed'])
                duration += timedelta(hours=int(duration_parts[0]), minutes=int(duration_parts[1]),
                                     seconds=int(duration_parts[2]))
            elif df.at[row,'Type'] == 'Test':
                num_tests += int(df.at[row,'Total'])
                num_tests_failed += int(df.at[row,'Failed'])
                num_tests_passed += int(df.at[row,'Passed'])
                duration += timedelta(hours=int(duration_parts[0]), minutes=int(duration_parts[1]),
                                     seconds=int(duration_parts[2]))
                #tests_dll = Get_DLL(LabName)
        data_summary.append({
            'Lab_Name' : LabName,
            'num_install' : num_install,
            'num_install_failed' : num_install_failed,
            'num_install_passed' : num_install_passed,
            'num_tests' : num_tests,
            'num_tests_failed' : num_tests_failed,
            'num_tests_passed' : num_tests_passed,
            'State' : state,
            'Duration' : str(duration),
            'Tests_DLL' : Get_DLL(LabName)
            })
    df_summary_all = pd.DataFrame(data_summary)
    if df_summary_all is not None :
        # Calculate the sum of specific columns
        total_row = df_summary_all[['num_install', 'num_install_failed', 'num_install_passed', 'num_tests', 'num_tests_failed',
                        'num_tests_passed']].sum()
        # Convert the total_row Series to a DataFrame
        total_row = pd.DataFrame(total_row).T
        total_row['Lab_Name'] = 'SUM'
        df1 = pd.concat([df_summary_all, total_row], ignore_index=True)
        df1.reset_index(inplace=True)
        df1.rename(columns={'index': 'id'}, inplace=True)
    else:
        df1 = pd.DataFrame()
        df1['Lab_Name'] = ["ERROR getting trx from GitHub Machine"]
        df1.reset_index(inplace=True)
        df1.rename(columns={'index': 'id'}, inplace=True)
    set_name = 'ALL_SET01'
    # Create a folder for the lab if it doesn't exist
    lab_folder = os.path.join(path, set_name)
    os.makedirs(lab_folder)
    logging.info("make folder for " + set_name + " in path : " + path)
    # Save df_summary_all and df_unit_all as CSV files in the lab folder
    df1.to_csv(os.path.join(lab_folder, f'summary_df_{set_name}.csv'), index=False)
    logging.info("save summary_df as CSV for " + set_name + " in path : " + lab_folder)
def main():
    currentpath = os.getcwd() + "\AnalyzeData1.log"
    if os.path.exists(currentpath):
        os.remove(currentpath)
    logging.basicConfig(level=logging.ERROR,
                        filename='AnalyzeData1.log',
                        filemode='w',
                        format=f'[%(levelname)s] %(asctime)s | : Line No. : %(lineno)d - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        )
    global script_filename
    script_filename = 'AnalyzeData1.py'
    logging.info(f"------------------- {script_filename} --------------------")
    StoreDF()
    return "Done AnalyzeData 1 successfully"
#TODO:
# analyze the data
# create folder for each lab
# create csv from each DF for each lab
if __name__ == '__main__':
    main()

