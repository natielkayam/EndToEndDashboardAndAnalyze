import { useState } from "react";
import { ProSidebar, Menu, MenuItem } from "react-pro-sidebar";
import { Box, IconButton, Typography, useTheme } from "@mui/material";
import { Link } from "react-router-dom";
import "react-pro-sidebar/dist/css/styles.css";
import { tokens } from "../theme";
import lab1json from "../lab1";
import lab2json from "../lab2";
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";
import ComputerIcon from '@mui/icons-material/Computer';
import Radio from '@mui/material/Radio'; 
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import List from '@mui/material/List';
import CloudQueueIcon from '@mui/icons-material/CloudQueue';
import { useData } from '../DataContext';


const Sidebar = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const {labName, setLabName} = useData()
  const { selectedValue, setSelectedValue } = useData();
  const {isDisabled} = useData();


  let labs1 = new Array(Object.keys(lab1json))
  labs1[0].unshift('ALL_SET01')
  let labs2 = new Array(Object.keys(lab2json))
  labs2[0].unshift('ALL_SET02')

  const handleRadioChange = (event) => {
      if (event.target.value === 'set1'){
      if (!labs1[0].includes(labName)){
        var labname1 = 'ALL_SET01';
        setLabName(labname1);
      }
      } 
      if (event.target.value === 'set2'){
      if (!labs2[0].includes(labName)){
        var labname2 = 'ALL_SET02';
        setLabName(labname2);
      }
    } 
  setSelectedValue(event.target.value); 
  };
  
  const renderLabItems = () => {
    const labData = selectedValue === "set1" ? lab1json : lab2json;
    const set = selectedValue === "set1" ? "ALL_SET01" : "ALL_SET02"
    let labs = new Array(Object.keys(labData))
    labs[0].unshift(set)

    return labs[0].map((key) => (
      <ListItem
        key={key}
        button
        selected={selectedValue === key}
        onClick={() => handleItemClick(key)}
        component={Link}
        to="/"
      >
        <ListItemText primary={key} />
      </ListItem>
    ));
  };

  const handleItemClick = (item) => {
    setLabName(item);
  };
  return (
    <Box
      sx={{
        "& .pro-sidebar-inner": {
          background: `${colors.primary[400]} !important`,
        },
        "& .pro-icon-wrapper": {
          backgroundColor: "transparent !important",
        },
        "& .pro-inner-item": {
          padding: "5px 35px 5px 20px !important",
        },
        "& .pro-inner-item:hover": {
          color: "#868dfb !important",
        },
        "& .pro-menu-item.active": {
          color: "#6870fa !important",
        },
      }}
    >
      <ProSidebar collapsed={isCollapsed} width = '210px'>
        <Menu iconShape="square">
          {/* LOGO AND MENU ICON */}
          <MenuItem
            onClick={() => setIsCollapsed(!isCollapsed)}
            icon={isCollapsed ? <MenuOutlinedIcon /> : undefined}
            style={{
              margin: "10px 0 20px 0",
              color: colors.grey[100],
            }}
          >
            {!isCollapsed && (
              <Box
                display="flex"
                justifyContent="space-between"
                alignItems="center"
                ml="10px"
              >
                <Typography variant="h3" color={colors.grey[100]}>
                  UI Results
                </Typography>
                <IconButton onClick={() => setIsCollapsed(!isCollapsed)}>
                  <MenuOutlinedIcon />
                </IconButton>
              </Box>
            )}
          </MenuItem>

          <Box paddingLeft={isCollapsed ? undefined : "10%"}>
            {/* List items */}
            <Typography 
            variant="h6" 
            fontWeight="bold" 
            color={colors.grey[200]}
            sx={{ display: 'flex', 
            alignItems: 'center', 
            m: "15px 0 5px 20px" }}>
            <CloudQueueIcon sx={{ marginRight: '6px' }} /> 
            SET ID
            </Typography>
            {/* Radio button group */}
            <RadioGroup
              aria-label="Select an option"
              name="option"
              value={selectedValue}
              onChange={handleRadioChange}
              //disa
              style={{
                margin: "10px 0 20px 20px",
                color: colors.grey[100],
              }}
            >
              <FormControlLabel value="set1" control={<Radio />} disabled = {isDisabled} label="1" />
              <FormControlLabel value="set2" control={<Radio />} disabled = {isDisabled} label="2" />
            </RadioGroup>
            <Typography
              variant="h6"
              fontWeight="bold"
              color={colors.grey[200]}
              sx={{ display: 'flex', 
              alignItems: 'center', 
              m: "15px 0 5px 20px" }}>
              <ComputerIcon sx={{ marginRight: '8px' }} />
            LAB
            </Typography>

            <List>{renderLabItems()}</List>
          </Box>
        </Menu>
      </ProSidebar>
    </Box>
  );
};

export default Sidebar;