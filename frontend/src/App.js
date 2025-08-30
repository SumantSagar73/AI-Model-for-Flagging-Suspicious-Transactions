import React from "react";
import { Container, Typography, Tabs, Tab, Box, AppBar, Toolbar } from "@mui/material";
import UploadForm from "./components/UploadForm";
import TransactionForm from "./components/TransactionForm";
import ResultsTable from "./components/ResultsTable";
import Charts from "./components/Charts";

function App() {
  const [tab, setTab] = React.useState(0);
  const [results, setResults] = React.useState(null);

  const handleResults = (newResults) => {
    setResults(newResults);
    // Switch to Charts tab to show results
    setTab(2);
  };

  return (
    <div>
      <AppBar position="static" sx={{ mb: 3, bgcolor: '#1565c0' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            🚔 Police Financial Crime Investigation System
          </Typography>
          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', mr: 2 }}>
            Cyber Crime Division
          </Typography>
          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
            AI-Powered Fraud Detection
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="lg">
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
          <Tabs value={tab} onChange={(e, v) => setTab(v)} centered>
            <Tab label="�️ Case Upload" />
            <Tab label="🔍 Transaction Check" />
            <Tab label="📊 Investigation Analytics" />
            <Tab label="📋 Evidence Report" />
          </Tabs>
        </Box>
        
        <Box>
          {tab === 0 && <UploadForm onResults={handleResults} />}
          {tab === 1 && <TransactionForm />}
          {tab === 2 && <Charts results={results} />}
          {tab === 3 && <ResultsTable results={results} />}
        </Box>
      </Container>
    </div>
  );
}

export default App;
