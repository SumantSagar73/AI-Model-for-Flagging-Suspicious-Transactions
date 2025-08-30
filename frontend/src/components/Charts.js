import React from "react";
import { Typography, Paper, Grid, Box } from "@mui/material";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

function Charts({ results }) {
  if (!results || !results.results) {
    return (
      <Paper sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          Fraud Analytics Charts
        </Typography>
        <Typography color="text.secondary">
          Upload data or make predictions to see analytics charts here.
        </Typography>
      </Paper>
    );
  }

  const { results: transactions, summary } = results;

  // Data for Pie Chart
  const pieData = [
    { name: 'Legitimate', value: summary.legit, color: '#4caf50' },
    { name: 'Fraudulent', value: summary.fraudulent, color: '#f44336' }
  ];

  // Data for Risk Distribution Bar Chart
  const riskDistribution = transactions.reduce((acc, transaction) => {
    const riskLevel = transaction.probability > 0.7 ? 'High Risk' : 
                     transaction.probability > 0.3 ? 'Medium Risk' : 'Low Risk';
    acc[riskLevel] = (acc[riskLevel] || 0) + 1;
    return acc;
  }, {});

  const barData = Object.entries(riskDistribution).map(([risk, count]) => ({
    risk,
    count,
    color: risk === 'High Risk' ? '#f44336' : risk === 'Medium Risk' ? '#ff9800' : '#4caf50'
  }));

  // Data for Probability Distribution
  const probabilityBins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];
  const probabilityData = probabilityBins.slice(0, -1).map((bin, index) => {
    const nextBin = probabilityBins[index + 1];
    const count = transactions.filter(t => t.probability >= bin && t.probability < nextBin).length;
    return {
      range: `${(bin * 100).toFixed(0)}-${(nextBin * 100).toFixed(0)}%`,
      count
    };
  });

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Fraud Analytics Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        {/* Fraud vs Legitimate Pie Chart */}
        <Grid item xs={12} md={6}>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h6" gutterBottom>
              Fraud Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value, percent }) => `${name}: ${value} (${(percent * 100).toFixed(1)}%)`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Box>
        </Grid>

        {/* Risk Level Distribution */}
        <Grid item xs={12} md={6}>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h6" gutterBottom>
              Risk Level Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="risk" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#8884d8">
                  {barData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Box>
        </Grid>

        {/* Probability Distribution */}
        <Grid item xs={12}>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h6" gutterBottom>
              Fraud Probability Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={probabilityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="range" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#2196f3" name="Number of Transactions" />
              </BarChart>
            </ResponsiveContainer>
          </Box>
        </Grid>
      </Grid>
    </Paper>
  );
}

export default Charts;
