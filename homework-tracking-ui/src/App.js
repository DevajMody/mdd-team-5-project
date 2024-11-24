import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import UserLogin from "./components/UserLogin";
import AdminLogin from "./components/AdminLogin";
import HomeworkDashboard from "./components/HomeworkDashboard";

function App() {
  return (
    <Router>
      <Routes>
        {/* Default Route */}
        <Route path="/" element={<UserLogin />} />

        {/* Admin Login Route */}
        <Route path="/admin-login" element={<AdminLogin />} />

        {/* Homework Dashboard Route */}
        <Route path="/dashboard" element={<HomeworkDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
