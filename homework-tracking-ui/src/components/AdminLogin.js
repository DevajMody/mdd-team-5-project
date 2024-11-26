import React, { useState } from "react";
import { TextField, Button, Box } from "@mui/material";

const AdminLogin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:8001/admin-signin", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessage("Admin login successful!");
        console.log("Logged in admin:", data.admin);
        // Save admin data and navigate to admin dashboard
        localStorage.setItem("admin", JSON.stringify(data.admin));
      } else if (response.status === 401) {
        setMessage("Invalid admin credentials. Please try again.");
      } else {
        setMessage("An error occurred. Please try again later.");
      }
    } catch (error) {
      console.error("Error during admin login:", error);
      setMessage("An error occurred. Please try again later.");
    }
  };

  return (
    <Box className="login-page">
      <Box className="login-left">
        <img src="/logo512.png" alt="RIT Logo" className="rit-logo" />
      </Box>
      <Box className="login-right">
        <h2>Admin Login</h2>
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
        {message && <p>{message}</p>}
      </Box>
    </Box>
  );
};

export default AdminLogin;
