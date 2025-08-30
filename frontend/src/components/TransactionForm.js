import React, { useState } from "react";
import { 
  Button, 
  TextField, 
  Typography, 
  Box, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem,
  Card,
  CardContent,
  Grid
} from "@mui/material";
import axios from "axios";

function TransactionForm() {
  const [form, setForm] = useState({ 
    Amount: "", 
    Payment_Method: "UPI",
    Merchant_Category: "Retail",
    Location: "Mumbai",
    Time: new Date().toISOString()
  });
  const [result, setResult] = useState(null);
  
  const paymentMethods = ["UPI", "NEFT", "RTGS", "IMPS", "Card", "Net Banking"];
  const merchantCategories = [
    "Retail", "Food", "Transport", "Healthcare", "Entertainment", 
    "Education", "Utilities", "Fuel", "Others"
  ];
  const locations = [
    "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad",
    "Pune", "Ahmedabad", "Surat", "Jaipur", "Lucknow", "Kanpur"
  ];
  
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
  
  const handleSubmit = async () => {
    try {
      const data = {
        ...form,
        Amount: parseFloat(form.Amount) || 0
      };
      
      const res = await axios.post("http://localhost:8001/predict", data);
      setResult(res.data);
      console.log("Prediction result:", res.data);
    } catch (error) {
      console.error("Prediction error:", error);
      alert("Prediction failed! Check console for details.");
    }
  };
  
  return (
    <Box>
      <Typography variant="h6" sx={{ mb: 3 }}>
        🕵️ Police Transaction Investigation Tool
      </Typography>
      
      <Card sx={{ maxWidth: 700, mb: 3 }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2, color: '#1565c0' }}>
            📝 Case Details Entry
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 3 }}>
            Enter transaction details from complaint/FIR for fraud analysis
          </Typography>
          
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField 
                fullWidth
                label="Transaction Amount (₹)" 
                name="Amount" 
                type="number"
                value={form.Amount} 
                onChange={handleChange}
                placeholder="Enter amount in INR"
                helperText="Amount involved in the suspected transaction"
              />
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Payment Method</InputLabel>
                <Select
                  name="Payment_Method"
                  value={form.Payment_Method}
                  onChange={handleChange}
                  label="Payment Method"
                >
                  {paymentMethods.map(method => (
                    <MenuItem key={method} value={method}>{method}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Merchant/Business Type</InputLabel>
                <Select
                  name="Merchant_Category"
                  value={form.Merchant_Category}
                  onChange={handleChange}
                  label="Merchant Category"
                >
                  {merchantCategories.map(category => (
                    <MenuItem key={category} value={category}>{category}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Location/Jurisdiction</InputLabel>
                <Select
                  name="Location"
                  value={form.Location}
                  onChange={handleChange}
                  label="Location"
                >
                  {locations.map(location => (
                    <MenuItem key={location} value={location}>{location}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            
            <Grid item xs={12}>
              <TextField 
                fullWidth
                label="Transaction Date & Time" 
                name="Time" 
                type="datetime-local"
                value={form.Time.slice(0, 16)} 
                onChange={handleChange}
                InputLabelProps={{
                  shrink: true,
                }}
                helperText="Date and time when the suspicious transaction occurred"
              />
            </Grid>
            
            <Grid item xs={12}>
              <Button 
                variant="contained" 
                color="primary" 
                onClick={handleSubmit}
                size="large"
                fullWidth
                sx={{ 
                  mt: 2,
                  bgcolor: '#1565c0',
                  '&:hover': { bgcolor: '#0d47a1' }
                }}
              >
                🔍 Analyze for Fraud Risk
              </Button>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
      
      {result && (
        <Card sx={{ maxWidth: 700 }}>
          <CardContent>
            <Typography variant="h6" sx={{ mb: 2 }}>
              {result.is_fraud ? "🚨 HIGH FRAUD RISK - INVESTIGATION RECOMMENDED" : "✅ LOW FRAUD RISK - APPEARS LEGITIMATE"}
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Typography variant="body2" color="textSecondary">
                  Fraud Risk Score
                </Typography>
                <Typography variant="h6" color={result.probability > 0.5 ? "error" : "success"}>
                  {(result.probability * 100).toFixed(2)}%
                </Typography>
              </Grid>
              
              <Grid item xs={6}>
                <Typography variant="body2" color="textSecondary">
                  Risk Classification
                </Typography>
                <Typography variant="h6">
                  {result.probability > 0.7 ? "🔴 HIGH RISK" : 
                   result.probability > 0.3 ? "🟡 MEDIUM RISK" : "🟢 LOW RISK"}
                </Typography>
              </Grid>
              
              {result.details?.payment_method && (
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">
                    Payment Method
                  </Typography>
                  <Typography variant="body1">
                    {result.details.payment_method}
                  </Typography>
                </Grid>
              )}
              
              {result.details?.amount && (
                <Grid item xs={6}>
                  <Typography variant="body2" color="textSecondary">
                    Amount Involved
                  </Typography>
                  <Typography variant="body1">
                    ₹{result.details.amount.toLocaleString('en-IN')}
                  </Typography>
                </Grid>
              )}
              
              <Grid item xs={12}>
                <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
                  Investigation Recommendations:
                </Typography>
                {result.probability > 0.7 ? (
                  <Typography variant="body2" sx={{ color: '#d32f2f' }}>
                    • High priority case - Immediate investigation required<br/>
                    • Contact bank for transaction details<br/>
                    • Check for similar pattern transactions<br/>
                    • Verify complainant identity and details
                  </Typography>
                ) : result.probability > 0.3 ? (
                  <Typography variant="body2" sx={{ color: '#f57c00' }}>
                    • Medium priority - Further verification needed<br/>
                    • Review transaction history<br/>
                    • Check merchant legitimacy<br/>
                    • Monitor for additional complaints
                  </Typography>
                ) : (
                  <Typography variant="body2" sx={{ color: '#388e3c' }}>
                    • Low priority - Standard documentation<br/>
                    • File routine report<br/>
                    • May be legitimate transaction<br/>
                    • Keep on record for pattern analysis
                  </Typography>
                )}
              </Grid>
              
              <Grid item xs={12}>
                <Typography variant="caption" color="textSecondary">
                  Analysis generated by: {result.details?.model || "Police AI System"} • 
                  Time: {new Date().toLocaleString('en-IN')}
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      )}
    </Box>
  );
}

export default TransactionForm;
