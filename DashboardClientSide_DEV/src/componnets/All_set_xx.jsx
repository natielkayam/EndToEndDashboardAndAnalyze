
import React, { useEffect } from 'react';
import { useData } from '../DataContext';
import { DataGrid,GridToolbar } from '@mui/x-data-grid';


const All_set_xx = () => {

    const {selectedValue, labName } = useData();
    const {data_All_summary, setDataAllSummary} = useData();
    const {isLoading, setIsLoading} = useData(); 
    const { date1 } = useData();
    const { date2 } = useData();
    const {rundate1 } = useData();
    const {rundate2 } = useData();
    const {allcheckedrows, setallcheckedrows} = useData() 
    const {allrowSelection, setallrowSelection} = useData();

    useEffect(() => {
        let apiUrl;    
        if (selectedValue === 'set1') {
            apiUrl = 'http://localhost:5000/api/files/summary_All_Set01'
        } else {
            apiUrl = 'http://localhost:5000/api/files/summary_All_Set02'
        }
        fetch(apiUrl)
          .then((response) => response.json())
          .then((data) => {
            data = AddRate(data)
            setDataAllSummary(data);
          })
          .catch((error) => {
            console.error(error);
            fetchfunc(apiUrl,setDataAllSummary);
          })
          .finally(() => {
            // Set loading state to false when data is fetched
            setIsLoading(false);
            setallcheckedrows("")
            setallrowSelection("")
          });
      }, [selectedValue]);
      
      const fetchfunc = (apiurl, setaction, maxRetries = 10, currentRetries = 0) => {
          fetch(apiurl)
          .then((response) => response.json())
          .then((data) => {
            setaction(data);
          })
          .catch((error) => {
            console.error(error);
            if (currentRetries < maxRetries) {
              console.log("retry : "+currentRetries,apiurl)
              // Retry the fetch after a delay (e.g., 1 second)
              setTimeout(() => {
                fetchfunc(apiurl, setaction, maxRetries, currentRetries + 1);
              }, 500); // 1000 milliseconds = 1 second
            } else {
              console.error(`Max retries (${maxRetries}) reached. Cannot fetch data.`);
            }
          });
      };

      const AddRate = (data) =>{
        data.forEach(element => {
          if (element.num_tests != 0) {
            element.Rate = ((element.num_tests_passed / element.num_tests) * 100).toFixed(1) + ' %'
          }
          else {element.Rate = 0+ ' %'}
        });
        return data;
      }

      if (isLoading) {
        return <div>Loading...</div>; 
      }
      
      const columns_All_summary = [
        { field: 'Lab_Name', headerName: 'Lab Name', flex: 1 },
        { field: 'num_install', headerName: 'num_install', flex: 1 },
        { field: 'num_install_failed', headerName: 'num_install_failed', flex: 1 },
        { field: 'num_install_passed', headerName: 'num_install_passed', flex: 1 },
        { field: 'num_tests', headerName: 'num_tests', flex: 1 },
        { field: 'num_tests_failed', headerName: 'num_tests_failed', flex: 1 },
        { field: 'num_tests_passed', headerName: 'num_tests_passed', flex: 1 },
        { field: 'State', headerName: 'State', flex: 1 },
        { field: 'Rate', headerName: 'Rate', flex: 1 },
        { field: 'Duration', headerName: 'Duration', flex: 1 },
        { field: 'Tests_DLL', headerName: 'Tests_DLL', flex: 1 },
      ];
      
      const getfilename = (pre) =>{
        if (selectedValue === 'set1'){
          return labName+"-ID-"+rundate1+"-Up-"+date1
        }
        else
        {
          return labName+"-ID-"+rundate2+"-Up-"+date2
        }  
      }
      const getrundata =()=>{ 
        let update = ""
        let date = ""
        let hours = ""
        if (selectedValue === 'set1' && rundate1 !== undefined && rundate1 !== ""){
          update = date1
          date = rundate1.split('T')[0].replace(/-/g,'/')
          let parts = date.split('/');
          date = parts[2]+"/"+parts[1]+"/"+parts[0];
          hours = rundate1.split('T')[1].replace(/-/g,':')
        }
        else if (selectedValue === 'set2' && rundate2 !== undefined && rundate2 !== ""){
          update = date2
          date = rundate2.split('T')[0].replace(/-/g,'/')
          let parts = date.split('/');
          date = parts[2]+"/"+parts[1]+"/"+parts[0];
          hours = rundate2.split('T')[1].replace(/-/g,':')
        }
        let str = date+" "+hours;
        return (
          <div className='run_data'>
          {selectedValue}
          <br/>
          Run ID : {str}
          <br/>
          Update at : {update}
          </div>
        )
        }

      const onRowsSelectionHandler = (ids) => {
        //console.log("enter row selection")
        const selectedRowsData = ids.map((id) => data_All_summary.find((row) => row.id === id));
        var dic = {}
        selectedRowsData.forEach(element => {
          dic[element.id] = [element.Lab_Name,element.State,element.num_tests, element.num_tests_failed, element.Tests_DLL]
        });
        setallcheckedrows(dic)
      };
    
      const checkedrowsdata = () =>{
        if (allcheckedrows !== undefined )
        {
        return (
          <div>
            {Object.entries(allcheckedrows).map(([key, value]) => (
              <div key={key}
              style ={{
                "border": "1px solid",
                "borderRadius": "5px",
                "margin": "5px",
                "padding": "3px"
              }}
              >
                <br/>
                <b><u>Lab Name :</u></b> &nbsp;{value[0]}   &nbsp;<b><u>State :</u></b> &nbsp;{value[1]}
                <br/>
                ---------------------
                <br/>
                <b><u>Num Tests :</u></b> &nbsp;{value[2]}    &nbsp;<b><u>Tests Failed :</u></b> &nbsp;{value[3]}
                <br/>
                ---------------------
                <br/>
                <b><u>Tests DLL :</u></b> &nbsp;{value[4]}
                <br/>
                <br/>
              </div>
            ))}
          </div>
        );
        }
        else {
          return ""
        }
      }
      return (
        <div id='container' style={{ textAlign: 'center' }}>
          {getrundata()}
          <div className='sum_title'>
            <h3>Summary</h3>
          </div>
          <div style={{ height: 600, width: '100%', paddingLeft: '1px', paddingRight: '2px'}}>
            <DataGrid
              rows={data_All_summary}
              columns={columns_All_summary}
              pageSize={8}
              checkboxSelection
              rowSelection = {allrowSelection}
              onRowSelectionModelChange={(ids) => 
                {
                onRowsSelectionHandler(ids);
                setallrowSelection(ids)
                }
              }
              getRowId={(row) => (row.id)}
              density={'compact'}
              slots={{ toolbar: GridToolbar }}
              slotProps={{ toolbar: { 
                  csvOptions: { fileName: getfilename()}
              }}}
              sx = {{
                button: {color : '#fff'},
                '& .MuiCheckbox-root.Mui-checked, & .MuiCheckbox-root.MuiCheckbox-indeterminate': {
                  '& .MuiSvgIcon-root': {
                    color: '#fff',
                  },
                },
              }}
            />
          </div>
          <div className='rowselection' >
        {checkedrowsdata()}
      </div>
        </div>
      );
    };

export default All_set_xx;
