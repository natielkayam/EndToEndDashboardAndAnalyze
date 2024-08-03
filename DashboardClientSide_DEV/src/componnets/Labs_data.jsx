import React, { useEffect, useState } from 'react';
import { useData } from '../DataContext';
import { DataGrid,GridToolbar } from '@mui/x-data-grid';

const Labs_data = () => {
  
  const { labName, selectedValue } = useData();
  const {data_summary, setDataSummary} = useData();
  const {data_unit, setDataUnit} = useData();
  const {isLoadingLabs, setIsLoadingLabs} = useData();
  const {state , SetState} = useData();
  const { error, seterror } = useData();
  const { date1 } = useData();
  const { date2 } = useData();
  const {rundate1 } = useData();
  const {rundate2 } = useData();
  const {checkedrows, setcheckedrows} = useData() 
  const {rowSelection, setrowSelection} = useData();

  useEffect(() => {
    let apiUrlSummary;
    let apiUrlUnit;
    let apiState;
    let apiError;
    console.log("enter use effect")
    if (selectedValue === 'set1') {
      apiUrlSummary = 'http://localhost:5000/api/files/summary1?lab_name=' + labName;
      apiUrlUnit = 'http://localhost:5000/api/files/unit1?lab_name=' + labName;
      apiState = 'http://localhost:5000/api/files/States_Set01?lab_name=' + labName;
      apiError = 'http://localhost:5000/api/files/error1?lab_name=' + labName;
    } else {
      apiUrlSummary = 'http://localhost:5000/api/files/summary2?lab_name=' + labName;
      apiUrlUnit = 'http://localhost:5000/api/files/unit2?lab_name=' + labName;
      apiState = 'http://localhost:5000/api/files/States_Set02?lab_name=' + labName;
      apiError = 'http://localhost:5000/api/files/error2?lab_name=' + labName;
    }
    fetch(apiUrlSummary)
      .then((response) => response.json())
      .then((data) => {
        setDataSummary(data);
      })
      .catch((error) => {
        console.error(error);
        fetchfunc(apiUrlSummary,setDataSummary);
      });

    fetch(apiUrlUnit)
      .then((response) => response.json())
      .then((data) => {
        setDataUnit(data);
      })
      .catch((error) => {
        console.error(error);
        fetchfunc(apiUrlUnit,setDataUnit);
      })

    fetch(apiState)
      .then((response) => response.json())
      .then((data) => {
        SetState(data);
      })
      .catch((error) => {
        console.error(error);
        fetchfunc(apiState,SetState);
      })

      fetch(apiError)
      .then((response) => response.json())
      .then((data) => {
        seterror(data);
      })
      .catch((error) => {
        console.error(error);
        fetchfunc(apiError,seterror);
      })
      
      .finally(() => {
        // Set loading state to false when data is fetched
        setIsLoadingLabs(false);
        setcheckedrows("")
        setrowSelection("")
      });
  }, [labName]);
  
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

  // Conditional rendering based on loading state
  if (isLoadingLabs) {
    return <div>Loading...</div>; // You can replace this with a loading spinner or message
  }
  
  const columns_summary = [
    { field: 'Lab_Name', headerName: 'Lab Name', flex: 1},
    { field: 'Test_Name', headerName: 'Test Name', flex: 1},
    { field: 'Type', headerName: 'Type', flex: 1},
    { field: 'Total', headerName: 'Total', flex: 1},
    { field: 'Passed', headerName: 'Passed', flex: 1},
    { field: 'Failed', headerName: 'Failed', flex: 1},
    { field: 'duration', headerName: 'Duration', flex: 1},
  ];
  const columns_units = [
    { field: 'Lab_name', headerName: 'Lab Name' ,flex: 1},
    { field: 'parent', headerName: 'Parent' ,flex: 1},
    { field: 'type', headerName: 'Type' ,flex: 1},
    { field: 'test_name', headerName: 'Name' ,flex: 1},
    { field: 'test_outcome', headerName: 'Outcome' ,flex: 1},
    { field: 'test_duration', headerName: 'Duration' ,flex: 1},
    { field: 'test_start_time', headerName: 'Start time' ,flex: 1},
    { field: 'test_end_time', headerName: 'End time' ,flex: 1},
    { field: 'Errormessage', headerName: 'Error message' ,flex: 1},
    { field: 'ErrorStackTrace', headerName: 'Stack trace' ,flex: 1}
  ];

  const getfilename = (pre) =>{
    let prefix
    if (pre === 's'){
      prefix = 'Summary'
    }
    else {
      prefix = 'Units'
    }

    if (selectedValue === 'set1'){
      return prefix+"-"+labName+"-ID-"+rundate1+"-Up-"+date1
    }
    else
    {
      return prefix+"-"+labName+"-ID-"+rundate2+"-Up-"+date2
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
    const selectedRowsData = ids.map((id) => data_unit.find((row) => row.id === id));
    var dic = {}
    selectedRowsData.forEach(element => {
      dic[element.id] = [element.parent,element.test_name, element.Errormessage ,element.ErrorStackTrace]
    });
    setcheckedrows(dic)
  };

  const checkedrowsdata = () =>{
    if (checkedrows !== undefined )
    {
    return (
      <div>
        {Object.entries(checkedrows).map(([key, value]) => (
          <div key={key}
          style ={{
            "border": "1px solid",
            "borderRadius": "5px",
            "margin": "5px",
            "padding": "3px"
          }}
          >
            <br/>
            <b><u>TRX :</u></b> {value[0]}
            <br/>
            ---------------------
            <br/>
            <b><u>Test Name :</u></b> {value[1]}
            <br/>
            ---------------------
            <br/>
            <b><u>Error Message :</u></b> {value[2]}
            <br/>
            ---------------------
            <br/>
            <b><u>Stack Trace :</u></b> {value[3]}
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
      <div ><h2> {labName} </h2></div>
      <div> State : {state} </div>
      <div className='sum_title'>
        <h3>Summary</h3>
      </div>
      <div style={{ height: 300, width: '100%', paddingLeft: '1px', paddingRight: '2px' }}>
       {data_summary && <DataGrid
          rows={data_summary}
          columns={columns_summary}
          pageSize={5}
          density={'compact'}
          checkboxSelection
          getRowId={(row) => (row.id)}
          slots={{ toolbar: GridToolbar }}
          slotProps={{ toolbar: { 
            csvOptions: { fileName: getfilename('s')}
        }}}
          sx = {{
            button: {color : '#fff'},
            '& .MuiCheckbox-root.Mui-checked, & .MuiCheckbox-root.MuiCheckbox-indeterminate': {
              '& .MuiSvgIcon-root': {
                color: '#fff',
              },
            },
          }}
        />}
      </div>
      <div className='uni_title'>
        <h3>Units</h3>
      </div>
      <div style={{ height: 500, paddingLeft: '1px', paddingRight: '2px' }}>
      {data_unit &&(
        <DataGrid
          rows={data_unit}
          columns={columns_units}
          pageSize={8}
          density={'compact'}
          checkboxSelection
          rowSelection = {rowSelection}
          onRowSelectionModelChange={(ids) => 
            {
            onRowsSelectionHandler(ids);
            setrowSelection(ids)
            }
          }
          getRowId={(row) => row.id}
          slots={{ toolbar: GridToolbar }}
          slotProps={{ toolbar: { 
            csvOptions: { fileName: getfilename('u') }
          }}}
          sx={{
            button: { color: '#fff' },
            '& .MuiCheckbox-root.Mui-checked, & .MuiCheckbox-root.MuiCheckbox-indeterminate': {
              '& .MuiSvgIcon-root': {
                color: '#fff',
              },
            },
          }}
        />
      )}
    </div>
      <div className='rowselection' >
        {checkedrowsdata()}
      </div>
      <div className='errors'>
          <h3> Errors </h3>
          <p style={{padding : '10px 10px 80px 10px'}}>
            {error}
            </p>
      </div>
    </div>
  );
};

export default Labs_data;