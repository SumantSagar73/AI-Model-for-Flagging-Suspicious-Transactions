import React, { useState } from "react";
import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  Typography,
  Chip,
  Box,
  Button,
  IconButton,
  TableContainer,
} from "@mui/material";

function ResultsTable({ results }) {
  const [currentPage, setCurrentPage] = useState(0);
  const entriesPerPage = 20;

  if (!results || !results.results) {
    return (
      <Paper sx={{ p: 2, mt: 2 }}>
        <Typography variant="h6" gutterBottom>
          Prediction Results
        </Typography>
        <Typography color="text.secondary">
          No results yet. Upload a CSV file or make a single prediction to see
          results here.
        </Typography>
      </Paper>
    );
  }

  const { results: transactions, summary } = results;
  const totalPages = Math.ceil(transactions.length / entriesPerPage);
  const startIndex = currentPage * entriesPerPage;
  const endIndex = Math.min(startIndex + entriesPerPage, transactions.length);
  const currentTransactions = transactions.slice(startIndex, endIndex);

  const handleFirstPage = () => setCurrentPage(0);
  const handlePreviousPage = () => setCurrentPage(Math.max(0, currentPage - 1));
  const handleNextPage = () =>
    setCurrentPage(Math.min(totalPages - 1, currentPage + 1));
  const handleLastPage = () => setCurrentPage(totalPages - 1);

  return (
    <Paper sx={{ p: 2, mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        🚔 Police Investigation Results
      </Typography>

      {/* Summary */}
      <Box sx={{ mb: 2, display: "flex", flexWrap: "wrap", gap: 1 }}>
        <Chip
          label={`Total Cases: ${summary.total}`}
          sx={{ fontWeight: "bold", bgcolor: "#1565c0", color: "white" }}
        />
        <Chip label={`✅ Low Risk: ${summary.legit}`} color="success" />
        <Chip label={`🚨 High Risk: ${summary.fraudulent}`} color="error" />
        <Chip
          label={`Risk Rate: ${(
            (summary.fraudulent / summary.total) *
            100
          ).toFixed(2)}%`}
          color="warning"
        />
      </Box>

      {/* Pagination Info */}
      <Box
        sx={{
          mb: 2,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Typography variant="body2" color="text.secondary">
          Showing cases {startIndex + 1}-{endIndex} of {transactions.length}{" "}
          total cases
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Page {currentPage + 1} of {totalPages}
        </Typography>
      </Box>

      {/* Results Table */}
      <TableContainer sx={{ maxHeight: 600 }}>
        <Table size="small" stickyHeader>
          <TableHead>
            <TableRow>
              <TableCell>
                <strong>Case ID</strong>
              </TableCell>
              <TableCell>
                <strong>Risk Assessment</strong>
              </TableCell>
              <TableCell>
                <strong>Fraud Probability</strong>
              </TableCell>
              <TableCell>
                <strong>Priority Level</strong>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {currentTransactions.map((transaction) => {
              const riskLevel =
                transaction.probability > 0.7
                  ? "HIGH PRIORITY"
                  : transaction.probability > 0.3
                  ? "MEDIUM PRIORITY"
                  : "LOW PRIORITY";
              const riskColor =
                transaction.probability > 0.7
                  ? "error"
                  : transaction.probability > 0.3
                  ? "warning"
                  : "success";

              return (
                <TableRow
                  key={transaction.transaction_id}
                  sx={{
                    backgroundColor: transaction.is_fraud
                      ? "rgba(244, 67, 54, 0.08)"
                      : "rgba(76, 175, 80, 0.08)",
                  }}
                >
                  <TableCell>
                    CASE-{String(transaction.transaction_id).padStart(5, "0")}
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: "flex", alignItems: "center" }}>
                      {transaction.is_fraud ? (
                        <Chip
                          label="🚨 INVESTIGATE"
                          color="error"
                          size="small"
                        />
                      ) : (
                        <Chip label="✅ ROUTINE" color="success" size="small" />
                      )}
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Typography
                      variant="body2"
                      color={
                        transaction.probability > 0.5 ? "error" : "success"
                      }
                      fontWeight="bold"
                    >
                      {(transaction.probability * 100).toFixed(2)}%
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip label={riskLevel} color={riskColor} size="small" />
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <Box
          sx={{
            mt: 2,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 1,
          }}
        >
          <Button
            onClick={handleFirstPage}
            disabled={currentPage === 0}
            variant="outlined"
            size="small"
          >
            ⏮️ First
          </Button>

          <Button
            onClick={handlePreviousPage}
            disabled={currentPage === 0}
            variant="outlined"
            size="small"
          >
            ◀️ Previous
          </Button>

          <Typography variant="body2" sx={{ mx: 2 }}>
            Page {currentPage + 1} of {totalPages}
          </Typography>

          <Button
            onClick={handleNextPage}
            disabled={currentPage >= totalPages - 1}
            variant="outlined"
            size="small"
          >
            Next ▶️
          </Button>

          <Button
            onClick={handleLastPage}
            disabled={currentPage >= totalPages - 1}
            variant="outlined"
            size="small"
          >
            Last ⏭️
          </Button>
        </Box>
      )}

      {/* Additional Info */}
      <Box
        sx={{
          mt: 2,
          p: 1,
          backgroundColor: "rgba(0,0,0,0.02)",
          borderRadius: 1,
        }}
      >
        <Typography variant="caption" color="text.secondary">
          � Police Investigation Dashboard: Use pagination controls to navigate
          through all {transactions.length} cases. Red-tinted rows indicate
          high-risk cases requiring immediate investigation, green-tinted rows
          are routine cases.
        </Typography>
      </Box>
    </Paper>
  );
}

export default ResultsTable;
