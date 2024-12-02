// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { TextField, Button, Box, Typography } from "@mui/material";
// import "../styles/Login.css";

// const Login = () => {
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [error, setError] = useState("");
//   const navigate = useNavigate();

//   const handleLogin = async (e) => {
//     e.preventDefault();
//     setError(""); // Clear previous errors

//     try {
//       const response = await fetch("http://localhost:8001/signin", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ email, password }),
//       });

//       if (response.ok) {
//         const data = await response.json();
//         const sessionKey = data.user.session_key;

//         // Store session key in localStorage
//         localStorage.setItem("sessionKey", sessionKey);

//         // Redirect to dashboard
//         navigate("/dashboard");
//       } else {
//         const errorData = await response.json();
//         setError(errorData.message || "Invalid login credentials");
//       }
//     } catch (err) {
//       console.error("Error logging in:", err);
//       setError("An error occurred. Please try again.");
//     }
//   };

//   return (
//     <Box
//       sx={{
//         maxWidth: 400,
//         margin: "auto",
//         mt: 5,
//         p: 3,
//         boxShadow: 3,
//         borderRadius: 2,
//       }}
//     >
//       <Typography variant="h5" mb={2}>
//         Login
//       </Typography>
//       {error && (
//         <Typography color="error" variant="body2" mb={2}>
//           {error}
//         </Typography>
//       )}
//       <form onSubmit={handleLogin}>
//         <TextField
//           label="Email"
//           variant="outlined"
//           fullWidth
//           margin="normal"
//           value={email}
//           onChange={(e) => setEmail(e.target.value)}
//           required
//         />
//         <TextField
//           label="Password"
//           variant="outlined"
//           fullWidth
//           margin="normal"
//           type="password"
//           value={password}
//           onChange={(e) => setPassword(e.target.value)}
//           required
//         />
//         <Button
//           type="submit"
//           variant="contained"
//           color="primary"
//           fullWidth
//           sx={{ mt: 2 }}
//         >
//           Login
//         </Button>
//       </form>
//     </Box>
//   );
// };

// export default Login;
