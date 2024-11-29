import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Typography,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Alert,
} from "@mui/material";
import { CalendarToday, List, Add } from "@mui/icons-material";
import AddAssignment from "./AddAssignment";

const HomeworkDashboard = () => {
  const [assignments, setAssignments] = useState([]); // Initialize as an empty array
  const [view, setView] = useState("list"); // 'list' or 'calendar'
  const [isModalOpen, setModalOpen] = useState(false);

  const fetchAssignments = async () => {
    try {
      const response = await fetch("http://localhost:8001/homework/user/1"); // Adjust user ID dynamically
      if (response.ok) {
        const data = await response.json();
        setAssignments(data.assignments || []); // Use fallback empty array if `data.assignments` is undefined
      } else {
        console.error("Failed to fetch assignments:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching assignments:", error);
    }
  };

  const handleAddAssignment = async (newAssignment) => {
    try {
      const response = await fetch("http://localhost:8001/homework", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newAssignment),
      });

      if (response.ok) {
        fetchAssignments(); // Refresh assignments after adding
      } else {
        console.error("Failed to add assignment:", response.statusText);
      }
    } catch (error) {
      console.error("Error adding assignment:", error);
    }
  };

  useEffect(() => {
    fetchAssignments(); // Fetch assignments on component mount
  }, []);

  return (
    <Box sx={{ padding: 3, maxWidth: "1200px", margin: "auto" }}>
      {/* Header Section */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 3,
        }}
      >
        <Typography variant="h4" fontWeight="bold">
          My Homework Dashboard
        </Typography>
        <Box>
          <Button
            variant={view === "list" ? "contained" : "outlined"}
            startIcon={<List />}
            sx={{ marginRight: 1 }}
            onClick={() => setView("list")}
          >
            List View
          </Button>
          <Button
            variant={view === "calendar" ? "contained" : "outlined"}
            startIcon={<CalendarToday />}
            onClick={() => setView("calendar")}
          >
            Calendar View
          </Button>
          <Button
            variant="contained"
            color="primary"
            startIcon={<Add />}
            sx={{ marginLeft: 1 }}
            onClick={() => setModalOpen(true)}
          >
            Add Assignment
          </Button>
        </Box>
      </Box>

      {/* Stats Overview */}
      <Grid container spacing={2} marginBottom={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader title="Total Assignments" />
            <CardContent>
              <Typography variant="h5">{assignments.length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        {/* Add other stats like Completed, Due Soon, Overdue */}
      </Grid>

      {/* Assignments List */}
      {assignments.map((assignment) => (
        <Card key={assignment.id} sx={{ marginBottom: 2 }}>
          <CardContent>
            <Typography variant="h6">{assignment.title}</Typography>
            {/* Additional assignment details */}
          </CardContent>
        </Card>
      ))}

      {/* Add Assignment Modal */}
      <AddAssignment
        open={isModalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleAddAssignment}
      />
    </Box>
  );
};

export default HomeworkDashboard;
