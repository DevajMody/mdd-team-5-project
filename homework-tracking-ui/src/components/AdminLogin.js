import React, { useState } from "react";
import { TextField, Button, Box } from "@mui/material";
import "../styles/Login.css";

const AdminLogin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    console.log("Admin login:", { email, password });
  };

  return (
    <Box className="login-page">
      <Box className="login-left">
        <img src="/logo512.png" alt="RIT Logo" className="rit-logo" />
      </Box>
      <Box className="login-right">
        <h2>CampusEvents - Admin</h2>
        <form onSubmit={handleLogin} className="login-form">
          <TextField
            label="Admin Username"
            variant="outlined"
            fullWidth
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <TextField
            label="Password"
            type="password"
            variant="outlined"
            fullWidth
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            sx={{ marginTop: "20px" }}
          >
            Login
          </Button>
        </form>
      </Box>
    </Box>
  );
};

export default AdminLogin;
