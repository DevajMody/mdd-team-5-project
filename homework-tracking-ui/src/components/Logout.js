import React from "react";
import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

const Logout = ({ sessionKey }) => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const response = await fetch("http://localhost:8001/logout", {
        method: "POST",
        headers: {
          "Session-Key": sessionKey,
        },
      });

      if (response.ok) {
        console.log("Logged out successfully");
        localStorage.removeItem("sessionKey"); // Clear session key from local storage
        navigate("/"); // Redirect to login page
      } else {
        const errorMsg = await response.json();
        console.error("Failed to log out:", errorMsg.message);
        alert(`Failed to log out: ${errorMsg.message}`);
      }
    } catch (error) {
      console.error("Error during logout:", error);
      alert("An error occurred during logout. Please try again.");
    }
  };

  return (
    <Button
      variant="outlined"
      color="error"
      onClick={handleLogout}
      sx={{ marginLeft: 2 }}
    >
      Logout
    </Button>
  );
};

export default Logout;
