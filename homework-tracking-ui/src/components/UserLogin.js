import React, { useState } from "react";
import { TextField, Button, Tabs, Tab, Box } from "@mui/material";
import { useNavigate } from "react-router-dom";

const UserLogin = () => {
  const [tabValue, setTabValue] = useState(0);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
    setMessage(""); // Clear messages when switching tabs
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8001/signin", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessage("Login successful!");
        localStorage.setItem("user", JSON.stringify(data.user));
        navigate("/dashboard");
      } else if (response.status === 401) {
        setMessage("Invalid credentials. Please try again.");
      } else {
        setMessage("An error occurred. Please try again later.");
      }
    } catch (error) {
      console.error("Error logging in:", error);
      setMessage("An error occurred. Please try again later.");
    }
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8001/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessage("Signup successful! Please log in.");
        setTabValue(0); // Switch to Login tab after signup
      } else {
        setMessage("An error occurred during signup. Please try again.");
      }
    } catch (error) {
      console.error("Error signing up:", error);
      setMessage("An error occurred. Please try again later.");
    }
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
        >
          <Tab label="Login" />
          <Tab label="Register" />
        </Tabs>
        {tabValue === 0 ? (
          <form onSubmit={handleLogin}>
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
            <Button type="submit" variant="contained" fullWidth>
              Login
            </Button>
          </form>
        ) : (
          <form onSubmit={handleSignup}>
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
            <Button type="submit" variant="contained" fullWidth>
              Register
            </Button>
          </form>
        )}
        {message && <p>{message}</p>}
      </Box>
    </Box>
  );
};

export default UserLogin;
