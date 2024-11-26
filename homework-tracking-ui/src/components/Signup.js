import React, { useState } from "react";
import { TextField, Button, Box, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

const Signup = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      console.log("Attempting to signup with:", { name, email, password });

      const response = await fetch("http://localhost:8001/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, email, password }),
      });

      console.log("Response status:", response.status);

      if (response.ok) {
        const data = await response.json();
        setMessage("Signup successful! You can now log in.");
        console.log("User created:", data);
        navigate("/");
      } else {
        // Try to get error details
        const errorData = await response.text();
        console.error("Signup failed:", errorData);

        setMessage(
          response.status === 400
            ? "Signup failed. Email already exists or invalid data."
            : "An error occurred. Please try again later."
        );
      }
    } catch (error) {
      console.error("Full error signing up:", error);
      setMessage("An error occurred. Please try again later.");
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        flexDirection: "column",
        backgroundColor: "#f5f5f5",
        padding: 3,
      }}
    >
      <Box
        sx={{
          width: "400px",
          backgroundColor: "white",
          padding: 3,
          borderRadius: 2,
          boxShadow: 3,
        }}
      >
        <Typography variant="h4" gutterBottom>
          Sign Up
        </Typography>
        <form onSubmit={handleSignup}>
          <TextField
            label="Name"
            variant="outlined"
            fullWidth
            margin="normal"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <TextField
            label="Email"
            variant="outlined"
            fullWidth
            margin="normal"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <TextField
            label="Password"
            type="password"
            variant="outlined"
            fullWidth
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            sx={{ marginTop: 2 }}
          >
            Sign Up
          </Button>
        </form>
        {message && (
          <Typography
            variant="body2"
            color={message.includes("successful") ? "green" : "red"}
            sx={{ marginTop: 2 }}
          >
            {message}
          </Typography>
        )}
        <Button
          variant="text"
          fullWidth
          sx={{ marginTop: 2 }}
          onClick={() => navigate("/")}
        >
          Already have an account? Login
        </Button>
      </Box>
    </Box>
  );
};

export default Signup;
