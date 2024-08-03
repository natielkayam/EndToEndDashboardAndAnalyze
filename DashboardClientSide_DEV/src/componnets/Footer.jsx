import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import { Box,useTheme } from "@mui/material";
import { useData } from "../DataContext";
import React, { useEffect } from 'react';
import { tokens } from "../theme";


const Footer = () =>{
    const {  selectedValue } = useData();
    const {versions, setVersions }= useData();
    const {isLoadingVersions, setIsLoadingVersions} = useData();
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    useEffect(() => {
        let apiVersions;
        if (selectedValue === 'set1') {
            apiVersions = 'http://localhost:5000/api/files/Versions_Set01';
        } else if(selectedValue === 'set2'){
            apiVersions = 'http://localhost:5000/api/files/Versions_Set02';
        }
        fetch(apiVersions)
          .then((response) => response.json())
          .then((data) => {
            setVersions(data[0]);
            footerdata();
          })
          .catch((error) => {
            console.error(error);
            fetchfunc(apiVersions,setVersions);
          })
          .finally(() => {
            setIsLoadingVersions(false);
          });
        }
      , [selectedValue]);

      const fetchfunc = (apiurl,setaction, maxRetries = 10, currentRetries = 0) =>{
        fetch(apiurl)
        .then((response) => response.json())
        .then((data) => {
          setaction(data[0]);
          footerdata();
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
      }
      if (isLoadingVersions) {
        return <div>Loading...</div>; 
      }

      const footerdata = () =>{
        if (versions !== undefined )
        {
        return Object.entries(versions).map(([key, value]) => (
          key+" : "+value.split("/")[1]+" "))
        }
        else {
          return ""
        }
      }
      return (
        <Box
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === "light"
                ? theme.palette.grey[200]
                : colors.primary[400],
            p: 0.5,
            position: 'fixed',
            width: '100%',
            bottom: '0',
            paddingRight : '120px'
          }}
          component="footer"
        >
          <Container maxWidth="xl">
            <Typography variant="body2" color="text.secondary">
            {footerdata()}
            </Typography>
          </Container>
        </Box>
      );
                  }
export default Footer