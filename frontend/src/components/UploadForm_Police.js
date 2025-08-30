import React, { useState } from "react";
import { 
  Button, 
  Typography, 
  Box, 
  Alert, 
  CircularProgress, 
  Card, 
  CardContent,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from "@mui/material";
import { CloudUpload, Description, Security, Assessment } from "@mui/icons-material";
import axios from "axios";

function UploadForm({ onResults }) {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setMessage("");
    
    const formData = new FormData();
    formData.append("file", file);
    
    try {
      const res = await axios.post("http://localhost:8001/upload", formData);
      console.log("Upload result:", res.data);
      
      if (res.data.results) {
        onResults(res.data); // Pass results to parent component
        setMessage(`🕵️ Case Analysis Complete! Processed ${res.data.summary.total} transactions. Identified ${res.data.summary.fraudulent} high-risk transactions requiring investigation.`);
      } else if (res.data.error) {
        setMessage(`❌ Error: ${res.data.error}`);
      }
    } catch (error) {
      console.error("Upload error:", error);
      setMessage(`❌ Upload failed: ${error.message}`);
    }
    
    setLoading(false);
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom sx={{ color: '#1565c0' }}>
        🕵️ Bulk Case File Analysis
      </Typography>
      
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            📁 Upload Transaction Records for Investigation
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 3 }}>
            Upload CSV files containing transaction data from complaints, FIRs, or bank records for automated fraud risk assessment.
          </Typography>
          
          <Box sx={{ 
            border: '2px dashed #1565c0', 
            borderRadius: 2, 
            p: 3, 
            textAlign: 'center',
            bgcolor: 'rgba(21, 101, 192, 0.05)',
            mb: 2
          }}>
            <CloudUpload sx={{ fontSize: 48, color: '#1565c0', mb: 2 }} />
            <Typography variant="body1" sx={{ mb: 2 }}>
              Drag and drop your case files here or click to browse
            </Typography>
            <input 
              type="file" 
              accept=".csv" 
              onChange={handleUpload}
              disabled={loading}
              style={{ 
                display: 'none' 
              }}
              id="case-file-upload"
            />
            <label htmlFor="case-file-upload">
              <Button
                variant="contained"
                component="span"
                disabled={loading}
                startIcon={loading ? <CircularProgress size={20} /> : <CloudUpload />}
                sx={{ 
                  bgcolor: '#1565c0',
                  '&:hover': { bgcolor: '#0d47a1' }
                }}
              >
                {loading ? 'Analyzing Cases...' : 'Select Case File (.csv)'}
              </Button>
            </label>
          </Box>
          
          {message && (
            <Alert 
              severity={message.includes('Complete') ? 'success' : 'error'} 
              sx={{ mt: 2 }}
              icon={message.includes('Complete') ? <Assessment /> : undefined}
            >
              {message}
            </Alert>
          )}
        </CardContent>
      </Card>
      
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            📋 Required CSV Format for Police Cases
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
            Ensure your CSV file contains the following columns for accurate fraud analysis:
          </Typography>
          
          <List dense>
            <ListItem>
              <ListItemIcon>
                <Description color="primary" />
              </ListItemIcon>
              <ListItemText 
                primary="Amount" 
                secondary="Transaction amount in INR (Required)"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <Description color="primary" />
              </ListItemIcon>
              <ListItemText 
                primary="Payment_Method" 
                secondary="UPI, NEFT, RTGS, IMPS, Card, Net Banking (Required)"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <Description color="primary" />
              </ListItemIcon>
              <ListItemText 
                primary="Merchant_Category" 
                secondary="Retail, Food, Transport, Healthcare, etc. (Required)"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <Description color="primary" />
              </ListItemIcon>
              <ListItemText 
                primary="Location" 
                secondary="City/State where transaction occurred (Required)"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <Description color="primary" />
              </ListItemIcon>
              <ListItemText 
                primary="Time" 
                secondary="Transaction timestamp (Optional)"
              />
            </ListItem>
          </List>
          
          <Divider sx={{ my: 2 }} />
          
          <Box sx={{ bgcolor: 'rgba(25, 118, 210, 0.05)', p: 2, borderRadius: 1 }}>
            <Typography variant="body2" sx={{ display: 'flex', alignItems: 'center' }}>
              <Security sx={{ mr: 1, color: '#1565c0' }} />
              <strong>Data Security:</strong> All uploaded data is processed securely and not stored permanently on the server.
            </Typography>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}

export default UploadForm;
