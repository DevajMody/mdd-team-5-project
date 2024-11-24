import React, { useState } from "react";
import { TextField, Button, Tabs, Tab, Box } from "@mui/material";
import { useNavigate } from "react-router-dom"; // Import useNavigate for navigation
import "../styles/Login.css";

const UserLogin = () => {
  const [tabValue, setTabValue] = useState(0); // 0: Login, 1: Register
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState(""); // For signup form

  const navigate = useNavigate(); // Initialize useNavigate

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleLogin = (e) => {
    e.preventDefault();
    console.log("User login:", { email, password });
    // After successful login, redirect to dashboard
    navigate("/dashboard");
  };

  const handleSignup = (e) => {
    e.preventDefault();
    console.log("User signup:", { name, email, password });
  };

  const redirectToAdmin = () => {
    navigate("/admin-login"); // Redirect to admin login page
  };

  return (
    <Box className="login-page">
      <Box className="login-left">
        <img src="/logo512.png" alt="RIT Logo" className="rit-logo" />
      </Box>
      <Box className="login-right">
        <h2>Homework Tracker</h2>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          centered
          indicatorColor="primary"
          textColor="primary"
          className="tabs"
        >
          <Tab label="Login" />
          <Tab label="Register" />
        </Tabs>

        {tabValue === 0 ? (
          // Login Form
          <form onSubmit={handleLogin} className="login-form">
            <TextField
              label="Email"
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
        ) : (
          // Signup Form
          <form onSubmit={handleSignup} className="login-form">
            <TextField
              label="Name"
              variant="outlined"
              fullWidth
              margin="normal"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <TextField
              label="Email"
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
              Register
            </Button>
          </form>
        )}
        <Button
          variant="text"
          color="primary"
          fullWidth
          sx={{ marginTop: "10px" }}
          onClick={redirectToAdmin}
        >
          Admin Login
        </Button>
      </Box>
    </Box>
  );
};

export default UserLogin;
