from datetime import datetime
import shutil
import pandas as pd
from flask import Flask, request, jsonify, send_file
import os
from flask_cors import CORS, cross_origin
import logging


app = Flask(__name__)
CORS(app,supports_credentials=True)

global pathset1
global pathset2
global state_set1
global state_set2
# global personal_dic
pathset1 = r'C:\Dashboard\TempSet01'
pathset2 = r'C:\Dashboard\TempSet02'
state_set1 = False
state_set2 = False
# personal_dic = {}
currentpath = os.getcwd() + r"\server_log.log"
if os.path.exists(currentpath):
    os.remove(currentpath)
logging.basicConfig(level=logging.ERROR,
                    filename='server_log.log',
                    filemode='w',
                    format=f'[%(levelname)s] %(asctime)s | : Line No. : %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', )

global script_filename
script_filename = 'back_Server.py'
logging.info(f"------------------- {script_filename} --------------------")



def change_pathset1(input_path1):
    try:
        global pathset1
        pathset1 = input_path1
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500
def change_stateSet1(newstate1):
    try:
        global state_set1
        state_set1 = newstate1
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500
def change_pathset2(input_path2):
    try:
        global pathset2
        pathset2 = input_path2
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500
def change_stateSet2(newstate2):
    try:
        global state_set2
        state_set2 = newstate2
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

def procces_data1():
    try:
        import AnalyzeData1
        res = AnalyzeData1.main()
        return res
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500
def procces_data2():
    try:
        import AnalyzeData2
        res = AnalyzeData2.main()
        return res
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@app.route('/api/get_data1', methods=['POST'])
def run_scripts_get_data1():
    try:
        if not state_set1:
            parts_set1 = pathset1.split('\\')
            copy_set1 = os.path.join(parts_set1[0]+'\\'+parts_set1[1]+'\\CopyTempSet01')
            if os.path.exists(copy_set1):
                shutil.rmtree(copy_set1, ignore_errors=False)
            shutil.copytree(pathset1, copy_set1)
            change_pathset1(copy_set1)
            change_stateSet1(True)
            res = procces_data1()
            pset1 = r'C:\Dashboard\TempSet01'
            change_pathset1(pset1)
            change_stateSet1(False)
            return jsonify(res), 200
        else:
            res = 'Update in progress by another client, got most update copy\nRefresh later'
            return jsonify(res), 200
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/get_data2', methods=['POST'])
def run_scripts_get_data2():
    try:
        if not state_set2:
            parts_set2 = pathset2.split('\\')
            copy_set2 = os.path.join(parts_set2[0]+'\\'+parts_set2[1]+'\\CopyTempSet02')
            if os.path.exists(copy_set2):
                shutil.rmtree(copy_set2, ignore_errors=False)
            shutil.copytree(pathset2, copy_set2)
            change_pathset2(copy_set2)
            change_stateSet2(True)
            res = procces_data2()
            pset2 = r'C:\Dashboard\TempSet02'
            change_pathset2(pset2)
            change_stateSet2(False)
            return jsonify(res), 200
        else:
            res = 'Update in progress by another client, got most update copy\nRefresh later'
            return jsonify(res), 200
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/States_Set01', methods=['GET'])
def get_States_Set01_csv():
    try:
        folder_name = "States_Set01"
        folder_path = os.path.join(pathset1, folder_name)
        lab_name = request.args.get('lab_name')
        logging.info("log : "+folder_name)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            csv_files = [file for file in os.listdir(folder_path) if file.startswith("States_Set01") and file.endswith('.csv')]
            if csv_files:
                first_csv_file_path = os.path.join(folder_path, csv_files[0])
                df = pd.read_csv(first_csv_file_path)
                value = df[lab_name].iloc[0]
                return jsonify(value)
            else:
                return jsonify({"error": "No CSV files found in the folder"}), 404
        else:
            return jsonify({"error": "No CSV files found in the folder"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

cross_origin(supports_credentials=True)
@app.route('/api/files/States_Set02', methods=['GET'])
def get_States_Set02_csv():
    try:
        folder_name = "States_Set02"
        folder_path = os.path.join(pathset2, folder_name)
        lab_name = request.args.get('lab_name')
        logging.info("log : "+folder_name)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            csv_files = [file for file in os.listdir(folder_path) if file.startswith("States_Set02") and file.endswith('.csv')]
            if csv_files:
                first_csv_file_path = os.path.join(folder_path, csv_files[0])
                df = pd.read_csv(first_csv_file_path)
                value = df[lab_name].iloc[0]
                return jsonify(value)
            else:
                return jsonify({"error": "No CSV files found in the folder"}), 404
        else:
            return jsonify({"error": "No CSV files found in the folder"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/Versions_Set01', methods=['GET'])
def get_Versions_Set01_csv():
    try:
        folder_name = "Versions_Set01"
        folder_path = os.path.join(pathset1, folder_name)  # Adjust the path as needed
        logging.info("log : "+folder_name)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            csv_files = [file for file in os.listdir(folder_path) if file.startswith("df_installations_"+folder_name) and file.endswith('.csv')]
            if csv_files:
                first_csv_file_path = os.path.join(folder_path, csv_files[0])
                df = pd.read_csv(first_csv_file_path)
                df1 = df.to_json(orient='records')
                return df1
            else:
                return jsonify({"error": "No CSV files found in the folder"}), 404
        else:
            return jsonify({"error": "No CSV files found in the folder"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/Versions_Set02', methods=['GET'])
def get_Versions_Set02_csv():
    try:
        folder_name = "Versions_Set02"
        folder_path = os.path.join(pathset2, folder_name)  # Adjust the path as needed
        logging.info("log : "+folder_name)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            csv_files = [file for file in os.listdir(folder_path) if file.startswith("df_installations_"+folder_name) and file.endswith('.csv')]
            if csv_files:
                first_csv_file_path = os.path.join(folder_path, csv_files[0])
                df = pd.read_csv(first_csv_file_path)
                df1 = df.to_json(orient='records')
                return df1
            else:
                return jsonify({"error": "No CSV files found in the folder"}), 404
        else:
            return jsonify({"error": "No CSV files found in the folder"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/summary_All_Set01', methods=['GET'])
def get_summary_All_Set01_csv():
    try:
        folder_name = "ALL_SET01"
        folder_path = os.path.join(pathset1, folder_name)  # Adjust the path as needed
        logging.info("log : "+folder_name)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            csv_files = [file for file in os.listdir(folder_path) if file.startswith("summary_df_"+folder_name) and file.endswith('.csv')]
            if csv_files:
                first_csv_file_path = os.path.join(folder_path, csv_files[0])
                df = pd.read_csv(first_csv_file_path)
                df1 = df.to_json(orient='records')
                return df1
            else:
                return jsonify({"error": "No CSV files found in the folder"}), 404
        else:
            return jsonify({"error": "No CSV files found in the folder"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/summary_All_Set02', methods=['GET'])
def get_summary_All_Set02_csv():
    try:
        folder_name = "ALL_SET02"
        folder_path = os.path.join(pathset2, folder_name)  # Adjust the path as needed
        logging.info("log : "+folder_name)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            csv_files = [file for file in os.listdir(folder_path) if file.startswith("summary_df_"+folder_name) and file.endswith('.csv')]
            if csv_files:
                first_csv_file_path = os.path.join(folder_path, csv_files[0])
                df = pd.read_csv(first_csv_file_path)
                df1 = df.to_json(orient='records')
                return df1
            else:
                return jsonify({"error": "No CSV files found in the folder"}), 404
        else:
            return jsonify({"error": "No CSV files found in the folder"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/summary1', methods=['GET'])
def get_summary1_csv():
    try:
        folder_name = request.args.get('lab_name')
        folder_path = os.path.join(pathset1, folder_name)  # Adjust the path as needed
        logging.info("log : "+folder_name)

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Assuming you want to return the content of the first CSV file found
            csv_files = [file for file in os.listdir(folder_path) if file.startswith("summary_df_"+folder_name) and file.endswith('.csv')]
            if csv_files:
                first_csv_file_path = os.path.join(folder_path, csv_files[0])
                df = pd.read_csv(first_csv_file_path)
                df1 = df.to_json(orient='records')
                return df1
            else:
                return jsonify({"error": "No CSV files found in the folder"}), 404
        else:
            return jsonify({"error": "No CSV files found in the folder"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/summary2', methods=['GET'])
def get_summary2_csv():
    try:
        folder_name = request.args.get('lab_name')
        folder_path = os.path.join(pathset2, folder_name)  # Adjust the path as needed
        logging.info("log : "+folder_name)

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Assuming you want to return the content of the first CSV file found
            csv_files = [file for file in os.listdir(folder_path) if file.startswith("summary_df_"+folder_name) and file.endswith('.csv')]
            if csv_files:
                first_csv_file_path = os.path.join(folder_path, csv_files[0])
                df = pd.read_csv(first_csv_file_path)
                df1 = df.to_json(orient='records')
                return df1
            else:
                return jsonify({"error": "No CSV files found in the folder"}), 404
        else:
            return jsonify({"error": "No CSV files found in the folder"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/unit1', methods=['GET'])
def get_unit1_csv():
    try:
        folder_name = request.args.get('lab_name')
        folder_path = os.path.join(pathset1, folder_name)  # Adjust the path as needed

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Assuming you want to return the content of the first CSV file found
            csv_files = [file for file in os.listdir(folder_path) if file.startswith("unit_df_"+folder_name) and file.endswith('.csv')]
            if csv_files:
                first_csv_file_path = os.path.join(folder_path, csv_files[0])
                df = pd.read_csv(first_csv_file_path)
                df1 = df.to_json(orient='records')
                return df1
            else:
                return jsonify({"error": "No CSV files found in the folder"}), 404
        else:
            return jsonify({"error": "No CSV files found in the folder"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/unit2', methods=['GET'])
def get_unit2_csv():
    try:
        folder_name = request.args.get('lab_name')
        folder_path = os.path.join(pathset2, folder_name)  # Adjust the path as needed

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Assuming you want to return the content of the first CSV file found
            csv_files = [file for file in os.listdir(folder_path) if file.startswith("unit_df_"+folder_name) and file.endswith('.csv')]
            if csv_files:
                first_csv_file_path = os.path.join(folder_path, csv_files[0])
                df = pd.read_csv(first_csv_file_path)
                df1 = df.to_json(orient='records')
                return df1
            else:
                return jsonify({"error": "No CSV files found in the folder"}), 404
        else:
            return jsonify({"error": "No CSV files found in the folder"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/error2', methods=['GET'])
def get_error2():
    try:
        folder_name = request.args.get('lab_name')
        folder_path = os.path.join(pathset2, folder_name)
        str = ""

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            error_files = [file for file in os.listdir(folder_path) if file.startswith(folder_name) and file.endswith('.err.txt')]
            if error_files:
                file_path = folder_path+"\\"+error_files[0]
                with open(file_path, 'r') as f:
                    for line in f:
                        str += line
            return jsonify(str),200
        else:
            return jsonify({"error": "No Found Lab"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/error1', methods=['GET'])
def get_error1():
    try:
        folder_name = request.args.get('lab_name')
        folder_path = os.path.join(pathset1, folder_name)
        str = ""

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            error_files = [file for file in os.listdir(folder_path) if file.startswith(folder_name) and file.endswith('.err.txt')]
            if error_files:
                file_path = folder_path+"\\"+error_files[0]
                with open(file_path, 'r') as f:
                    for line in f:
                        str += line
            return jsonify(str),200
        else:
            return jsonify("error No Found Lab"), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/dateUpdate01', methods=['GET'])
def get_date1():
    try:
        str = ""
        if os.path.exists(pathset1) and os.path.isdir(pathset1):
            date = [file for file in os.listdir(pathset1) if file.startswith('dateUpdate01') and file.endswith('.txt')]
            if date:
                file_path = pathset1+"\\"+date[0]
                with open(file_path, 'r') as f:
                    for line in f:
                        str += line
            return jsonify(str),200
        else:
            return jsonify({"error": "No Found date file in set01"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/dateUpdate02', methods=['GET'])
def get_date2():
    try:
        str = ""
        if os.path.exists(pathset2) and os.path.isdir(pathset2):
            date = [file for file in os.listdir(pathset2) if file.startswith('dateUpdate02') and file.endswith('.txt')]
            if date:
                file_path = pathset2+"\\"+date[0]
                with open(file_path, 'r') as f:
                    for line in f:
                        str += line
            return jsonify(str),200
        else:
            return jsonify({"error": "No Found date file in set01"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/rundate01', methods=['GET'])
def get_rundate1():
    try:
        str = ""
        if os.path.exists(pathset1) and os.path.isdir(pathset1):
            date = [file for file in os.listdir(pathset1) if file.startswith('rundate01') and file.endswith('.txt')]
            if date:
                file_path = pathset1+"\\"+date[0]
                with open(file_path, 'r') as f:
                    for line in f:
                        str += line
            return jsonify(str),200
        else:
            return jsonify({"error": "No Found date file in set01"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

@cross_origin(supports_credentials=True)

@app.route('/api/files/rundate02', methods=['GET'])
def get_rundate2():
    try:
        global pathset2
        str = ""
        if os.path.exists(pathset2) and os.path.isdir(pathset2):
            date = [file for file in os.listdir(pathset2) if file.startswith('rundate02') and file.endswith('.txt')]
            if date:
                file_path = pathset2+"\\"+date[0]
                with open(file_path, 'r') as f:
                    for line in f:
                        str += line
            return jsonify(str),200
        else:
            return jsonify({"error": "No Found date file in set02"}), 404
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    app.run()
