import React, { useContext, useState } from 'react';
import { Box, IconButton, useTheme } from "@mui/material";
import { ColorModeContext } from "../theme";
import InputBase from "@mui/material/InputBase";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";
import Button from '@mui/material/Button';
import GetAppIcon from '@mui/icons-material/GetApp';
import CircularProgress from "@mui/material/CircularProgress"; 
import logo3 from '../images/NCR-Logo.png';
import HomeIcon from '@mui/icons-material/Home';
import { useData } from '../DataContext';
import { useEffect } from 'react';
import { tokens } from "../theme";
import { Link } from "react-router-dom";


const Topbar = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const colorMode = useContext(ColorModeContext);
  const [isLoadingSet1, setIsLoadingSet1] = useState(false); 
  const [isLoadingSet2, setIsLoadingSet2] = useState(false); 
  const {setLabName} = useData();
  const {setSelectedValue} = useData();
  const {setIsDisabled} = useData();
  const {date1, setdate1 } = useData();
  const {date2, setdate2 } = useData();
  const {setrundate1 } = useData();
  const {setrundate2 } = useData();

  let apidateupdate1 = 'http://localhost:5000/api/files/dateUpdate01' ;
  let apidateupdate2 = 'http://localhost:5000/api/files/dateUpdate02' ;
  let apirundate1 = 'http://localhost:5000/api/files/rundate01' ;
  let apirundate2 = 'http://localhost:5000/api/files/rundate02' ;

  useEffect(() => {
    getdate1request();
    getdate2request();
    // This will only run on initial render    
  },[] );

  const getdate1request =()=>{

    fetch(apidateupdate1, {
      method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
      setdate1(data)
    })
    .catch(error => {
      console.error(error);
      fetchfunc(apidateupdate1,setdate1);
    });

    fetch(apirundate1, {
      method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
      setrundate1(data);
    })
    .catch(error => {
      console.error(error);
      fetchfunc(apirundate1,setrundate1);
    });
    }
  const getdate2request =()=>{
    fetch(apidateupdate2, {
      method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
      setdate2(data)
    })
    .catch(error => {
      console.error(error);
      fetchfunc(apidateupdate2,setdate2);
    });
    fetch(apirundate2, {
      method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
      setrundate2(data);
    })
    .catch(error => {
      console.error(error);
      fetchfunc(apirundate2,setrundate2);
    });
    }

    const fetchfunc = (apiurl, setaction, maxRetries = 10, currentRetries = 0) => {
      fetch(apiurl)
      .then((response) => response.json())
      .then((data) => {
        if (setaction !== null){
          setaction(data);
        }
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
  const updateInProgress1 =(data)=>{
    if (data ==='Update in progress by another client, got most update copy\nRefresh later'){
      alert(data)
    }
  }
  const updateInProgress2 =(data)=>{
    if (data ==='Update in progress by another client, got most update copy\nRefresh later'){
      alert(data)
    }
  }

  const handleSet1Click = () => {

    setSelectedValue("set2")
    setLabName("ALL_SET02")
    setIsLoadingSet1(true);
    setdate1("Loading SET01 ...") 
    setIsLoadingSet2(true); 
    setIsDisabled(true);

    fetch('http://localhost:5000/api/get_data1', {
      method: 'POST'
    })
      .then(response => response.json())
      .then(data => {
        updateInProgress1(data)
      })
      .catch(error => {
        console.error(error);
        fetchfunc('http://localhost:5000/api/get_data1',updateInProgress1)
      })  
      .finally(() => {
        setIsLoadingSet1(false);
        setIsLoadingSet2(false);
        setIsDisabled(false);
        getdate1request()
              });
  };

  const handleSet2Click = () => {
    setSelectedValue("set1")
    setLabName("ALL_SET01")
    setIsLoadingSet2(true); 
    setdate2("Loading SET02 ...") 
    setIsLoadingSet1(true); 
    setIsDisabled(true);
    fetch('http://localhost:5000/api/get_data2', {
      method: 'POST'
    })
      .then(response => response.json())
      .then(data => {
        updateInProgress2(data)
      })
      .catch(error => {
        console.error(error);
        fetchfunc('http://localhost:5000/api/get_data2',updateInProgress2)
      })
      .finally(() => {
        setIsLoadingSet2(false);
        setIsLoadingSet1(false);
        setIsDisabled(false);
        getdate2request()
            });
  };

  const getbackground = () =>{
    var list = []
    if (theme.palette.mode === "light"){
      list[0] = colors.grey[800]
      list[1] = colors.grey[600]
      return list
    }
    else {
      list[0] = colors.grey[0]
      list[1] = colors.primary[400]
      return list
    }
  }
  return (
    <Box display="flex" justifyContent="space-between" p={2}>
      {/* button set 1 */}
      <Button
        sx={{
          backgroundColor: getbackground()[0], 
          ':hover': {
            backgroundColor: getbackground()[1], 
          },
        }}
        color = 'primary'
        component="label"
        variant="contained"
        startIcon={<GetAppIcon />}
        onClick={handleSet1Click}
        disabled={isLoadingSet1} // Disable the button when loading
      >
        Get SET 1
      </Button>
      {isLoadingSet1 ? (
        // Render loading indicator when loading Set 1
        <CircularProgress size={24} color="primary" />
      ) : (
        // Render lastup1 when not loading Set 1
        <p style={{margin : '14px'}}>{date1}</p>
      )}
      {/* button set 2 */}
      <Button
        sx={{
          backgroundColor: getbackground()[0], 
          ':hover': {
            backgroundColor: getbackground()[1], 
          },
        }}
        component="label"
        variant="contained"
        startIcon={<GetAppIcon />}
        onClick={handleSet2Click}
        disabled={isLoadingSet2} // Disable the button when loading
      >
        Get SET 2
      </Button>
      {isLoadingSet2 ? (
        // Render loading indicator when loading Set 2
        <CircularProgress size={24} color="primary" />
      ) : (
        // Render lastup2 when not loading Set 2
        <p style={{margin : '14px'}}> {date2} </p>
      )}

      <InputBase sx={{ mr: 2, flex: 1 }} />
      <Box display="flex">
        <img
          src={logo3}
          alt="logo3"
          style={{ width: "100px", height: "32px", paddingTop: "5px", margin: '5px'}}
        />
        <IconButton onClick={colorMode.toggleColorMode}>
          {theme.palette.mode === "dark" ? (
            <DarkModeOutlinedIcon />
          ) : (
            <LightModeOutlinedIcon />
          )}
        </IconButton>
      </Box>
    </Box>
  );
};

export default Topbar;