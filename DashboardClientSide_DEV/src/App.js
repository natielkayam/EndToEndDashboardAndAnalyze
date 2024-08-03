
import { ColorModeContext, useMode } from "./theme";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Topbar from "./componnets/Topbar";
import Sidebar from "./componnets/Sidebar";
import Lab from "./componnets/Lab";
import { DataProvider } from "./DataContext";
import Footer from "./componnets/Footer";
function App() {
  const [theme, colorMode] = useMode();
  const [isSidebar] = useState(true);
  
  return (
    <DataProvider>
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="app">
      <Sidebar isSidebar={isSidebar} />
        <main className="content">
          <Topbar />
          <Routes>
              <Route path="/" element={<Lab/>} />
          </Routes>
          <Footer/>
        </main>
      </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
    </DataProvider>
  );
}

export default App;
