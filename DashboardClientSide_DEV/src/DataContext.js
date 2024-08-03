// DataContext.js
import React, { createContext, useContext, useState } from 'react';


const DataContext = createContext();

export const DataProvider = ({ children }) => {
  const [labName, setLabName] = useState('ALL_SET01');
  const [selectedValue, setSelectedValue] = useState("set1");
  const [data_All_summary, setDataAllSummary] = useState([]);
  const [isLoading, setIsLoading] = useState(true); 
  const [data_summary, setDataSummary] = useState([]);
  const [data_unit, setDataUnit] = useState([]);
  const [isLoadingLabs, setIsLoadingLabs] = useState(true); 
  const [state , SetState] = useState(); 
  const [versions, setVersions ]= useState([]);
  const [isLoadingVersions, setIsLoadingVersions ]= useState();
  const [isDisabled, setIsDisabled] = useState(false);
  const [ error, seterror ] = useState();
  const [ date1, setdate1 ] = useState("");
  const [ date2, setdate2 ] = useState("");
  const [ rundate1, setrundate1 ] = useState();
  const [ rundate2, setrundate2 ] = useState();
  const [checkedrows, setcheckedrows] = useState("") 
  const [rowSelection, setrowSelection] = useState("");
  const [allcheckedrows, setallcheckedrows] = useState("") 
  const [allrowSelection, setallrowSelection] = useState("");



  return (
    <DataContext.Provider value={{ labName, setLabName, selectedValue, setSelectedValue
    ,data_All_summary, setDataAllSummary,isLoading, setIsLoading,data_summary, setDataSummary
    , data_unit, setDataUnit, isLoadingLabs, setIsLoadingLabs,state , SetState
    ,versions, setVersions, isLoadingVersions, setIsLoadingVersions, isDisabled, setIsDisabled
    ,error, seterror,date1, setdate1,date2, setdate2,rundate2, setrundate2,rundate1, setrundate1,checkedrows, setcheckedrows,
    rowSelection, setrowSelection, allcheckedrows, setallcheckedrows, allrowSelection, setallrowSelection}}>
      {children}
    </DataContext.Provider>
  );
};

export const useData = () => {
  return useContext(DataContext);
};