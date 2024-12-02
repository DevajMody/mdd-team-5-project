import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import UserLogin from "./components/UserLogin";
import AdminLogin from "./components/AdminLogin";
import HomeworkDashboard from "./components/HomeworkDashboard";
import Signup from "./components/Signup"; // Uncommented Signup import
import "./styles/App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UserLogin />} />
        <Route path="/admin-login" element={<AdminLogin />} />
        <Route path="/dashboard" element={<HomeworkDashboard />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </Router>
  );
}

export default App;
