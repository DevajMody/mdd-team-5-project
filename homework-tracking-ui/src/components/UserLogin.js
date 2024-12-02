import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { TextField, Button, Box, Typography, Alert } from "@mui/material";
import "../styles/Login.css";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

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
        const sessionKey = data.user.session_key;

        if (sessionKey) {
          localStorage.setItem("sessionKey", sessionKey); // Save session key
          console.log("Session key stored:", sessionKey); // Debug log
          navigate("/dashboard"); // Redirect to dashboard
        } else {
          setError("Login failed: Missing session key.");
        }
      } else {
        setError("Invalid email or password.");
      }
    } catch (error) {
      console.error("Error during login:", error);
      setError("An unexpected error occurred.");
    }
  };

  return (
    <Box className="login-page">
      <Box className="login-container">
        <div className="login-header">
          <img
            src="https://www.rit.edu/brandportal/sites/rit.edu.brandportal/files/2022-10/RIT-00071A_RGB_whiteTM.jpg"
            alt="Homework Tracker Logo"
          />
          <Typography variant="h4" component="h1" className="login-title">
            Homework Tracker
          </Typography>
        </div>
        {error && (
          <Alert severity="error" sx={{ marginBottom: 2 }}>
            {error}
          </Alert>
        )}
        <form className="login-form" onSubmit={handleLogin}>
          <TextField
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            fullWidth
            sx={{ marginBottom: 2 }}
          />
          <TextField
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            fullWidth
            sx={{ marginBottom: 2 }}
          />
          <Button
            type="submit"
            variant="contained"
            fullWidth
            sx={{ marginBottom: 2 }}
          >
            Login
          </Button>
          <Button
            variant="text"
            fullWidth
            onClick={() => navigate("/signup")} // Navigate to Signup page
          >
            Don't have an account? Sign Up
          </Button>
        </form>
      </Box>
    </Box>
  );
};

export default Login;
