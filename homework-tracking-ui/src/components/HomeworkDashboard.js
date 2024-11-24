import React, { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Typography,
  IconButton,
  Grid,
  Alert,
} from "@mui/material";
import {
  CalendarToday,
  List,
  Add,
  CheckCircle,
  Edit,
  Delete,
} from "@mui/icons-material";

const HomeworkDashboard = () => {
  const [assignments, setAssignments] = useState([
    {
      id: 1,
      title: "Math Problem Set 3",
      subject: "Mathematics",
      dueDate: "2024-11-25",
      priority: "High",
      completed: false,
    },
    {
      id: 2,
      title: "Physics Lab Report",
      subject: "Physics",
      dueDate: "2024-11-24",
      priority: "Medium",
      completed: true,
    },
  ]);

  const [view, setView] = useState("list"); // 'list' or 'calendar'

  const getPriorityColor = (priority) => {
    switch (priority.toLowerCase()) {
      case "high":
        return "red";
      case "medium":
        return "orange";
      case "low":
        return "green";
      default:
        return "gray";
    }
  };

  const toggleComplete = (id) => {
    setAssignments((prev) =>
      prev.map((assignment) =>
        assignment.id === id
          ? { ...assignment, completed: !assignment.completed }
          : assignment
      )
    );
  };

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
          >
            Add Assignment
          </Button>
        </Box>
      </Box>

      {/* Stats Overview */}
      <Grid container spacing={2} marginBottom={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader
              title="Total Assignments"
              titleTypographyProps={{ variant: "subtitle1" }}
            />
            <CardContent>
              <Typography variant="h5">{assignments.length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader
              title="Completed"
              titleTypographyProps={{ variant: "subtitle1" }}
            />
            <CardContent>
              <Typography variant="h5">
                {assignments.filter((a) => a.completed).length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader
              title="Due Soon"
              titleTypographyProps={{ variant: "subtitle1" }}
            />
            <CardContent>
              <Typography variant="h5" color="orange">
                2
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardHeader
              title="Overdue"
              titleTypographyProps={{ variant: "subtitle1" }}
            />
            <CardContent>
              <Typography variant="h5" color="red">
                0
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Assignments List */}
      {assignments.map((assignment) => (
        <Card
          key={assignment.id}
          sx={{
            marginBottom: 2,
            backgroundColor: assignment.completed ? "#f9f9f9" : "#ffffff",
          }}
        >
          <CardContent>
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              <Box sx={{ display: "flex", alignItems: "center" }}>
                <IconButton
                  color={assignment.completed ? "success" : "default"}
                  onClick={() => toggleComplete(assignment.id)}
                >
                  <CheckCircle />
                </IconButton>
                <Box sx={{ marginLeft: 2 }}>
                  <Typography
                    variant="h6"
                    sx={{
                      textDecoration: assignment.completed
                        ? "line-through"
                        : "none",
                    }}
                  >
                    {assignment.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {assignment.subject} - Due: {assignment.dueDate}
                  </Typography>
                  <Typography
                    variant="body2"
                    fontWeight="bold"
                    color={getPriorityColor(assignment.priority)}
                  >
                    {assignment.priority} Priority
                  </Typography>
                </Box>
              </Box>
              <Box>
                <Button variant="outlined" size="small" sx={{ marginRight: 1 }}>
                  Edit
                </Button>
                <Button variant="outlined" color="error" size="small">
                  Delete
                </Button>
              </Box>
            </Box>
          </CardContent>
        </Card>
      ))}

      {/* Upcoming Deadlines Alert */}
      <Alert severity="info" sx={{ marginTop: 3 }}>
        You have 2 assignments due in the next 48 hours.{" "}
        <Button variant="text" size="small">
          View details
        </Button>
      </Alert>
    </Box>
  );
};

export default HomeworkDashboard;
