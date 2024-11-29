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
import { CalendarToday, List, Add, Edit, Delete } from "@mui/icons-material";
import AddAssignment from "./AddAssignment";
import EditAssignment from "./EditAssignment";
import Logout from "./Logout";
import { useNavigate } from "react-router-dom";

const HomeworkDashboard = () => {
  const [assignments, setAssignments] = useState([]); // Assignments state
  const [user, setUser] = useState(null); // User state
  const [view, setView] = useState("list"); // 'list' or 'calendar'
  const [isAddModalOpen, setAddModalOpen] = useState(false);
  const [isEditModalOpen, setEditModalOpen] = useState(false);
  const [selectedAssignment, setSelectedAssignment] = useState(null); // Selected assignment for editing
  const navigate = useNavigate();

  const fetchUser = async () => {
    const sessionKey = localStorage.getItem("sessionKey");

    if (!sessionKey) {
      console.error("Session key is missing. Redirecting to login.");
      navigate("/login");
      return;
    }

    try {
      const userId = 1; // Replace with logic to dynamically fetch user_id
      const response = await fetch(`http://localhost:8001/user/${userId}`, {
        method: "GET",
        headers: {
          "Session-Key": sessionKey,
        },
      });

      if (response.ok) {
        const user = await response.json();
        console.log("User details fetched successfully:", user);
        setUser(user.user_data); // Update state with user data
      } else {
        console.error("Failed to fetch user details:", response.statusText);
        navigate("/login");
      }
    } catch (error) {
      console.error("Error fetching user details:", error);
      navigate("/login");
    }
  };

  const fetchAssignments = async (userId) => {
    try {
      const response = await fetch(
        `http://localhost:8001/homework/user/${userId}`,
        {
          headers: {
            "Session-Key": localStorage.getItem("sessionKey"),
          },
        }
      );
      if (response.ok) {
        const data = await response.json();
        setAssignments(data.homework || []); // Fallback to an empty array
      } else {
        console.error("Failed to fetch assignments:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching assignments:", error);
    }
  };

  const handleEditAssignment = (assignment) => {
    setSelectedAssignment(assignment);
    setEditModalOpen(true);
  };

  const handleUpdateAssignment = async (updatedAssignment) => {
    const sessionKey = localStorage.getItem("sessionKey");
    try {
      const response = await fetch(
        `http://localhost:8001/homework/${selectedAssignment.homework_id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Session-Key": sessionKey,
          },
          body: JSON.stringify(updatedAssignment),
        }
      );

      if (response.ok) {
        console.log("Assignment updated successfully.");
        fetchAssignments(user.user_id); // Refresh assignments after updating
        setEditModalOpen(false); // Close the edit modal
      } else {
        const errorMsg = await response.text();
        console.error("Failed to update assignment:", errorMsg);
        alert(`Failed to update assignment: ${errorMsg}`);
      }
    } catch (error) {
      console.error("Error updating assignment:", error);
      alert("An error occurred while updating the assignment.");
    }
  };

  const handleDeleteAssignment = async (assignmentId) => {
    const sessionKey = localStorage.getItem("sessionKey");
    try {
      const response = await fetch(
        `http://localhost:8001/homework/${assignmentId}`,
        {
          method: "DELETE",
          headers: {
            "Session-Key": sessionKey,
          },
        }
      );

      if (response.ok) {
        console.log("Assignment deleted successfully.");
        fetchAssignments(user.user_id); // Refresh assignments after deletion
      } else {
        const errorMsg = await response.text();
        console.error("Failed to delete assignment:", errorMsg);
        alert(`Failed to delete assignment: ${errorMsg}`);
      }
    } catch (error) {
      console.error("Error deleting assignment:", error);
      alert("An error occurred while deleting the assignment.");
    }
  };

  useEffect(() => {
    fetchUser(); // Fetch user details on component mount
  }, []);

  useEffect(() => {
    if (user) {
      fetchAssignments(user.user_id); // Fetch assignments after user details are loaded
    }
  }, [user]);

  if (!user) {
    return <Typography>Loading...</Typography>;
  }

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
            onClick={() => setAddModalOpen(true)}
          >
            Add Assignment
          </Button>
          <Logout sessionKey={localStorage.getItem("sessionKey")} />
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
      </Grid>

      {/* Assignments List */}
      {assignments.length > 0 ? (
        assignments.map((assignment) => (
          <Card key={assignment.homework_id} sx={{ marginBottom: 2 }}>
            <CardContent>
              <Typography variant="h6">{assignment.title}</Typography>
              <Typography variant="body2">{assignment.description}</Typography>
              <Typography variant="caption">
                Due: {assignment.due_date}
              </Typography>
              <Box sx={{ display: "flex", gap: 1, marginTop: 1 }}>
                <Button
                  startIcon={<Edit />}
                  onClick={() => handleEditAssignment(assignment)}
                >
                  Edit
                </Button>
                <Button
                  startIcon={<Delete />}
                  color="error"
                  onClick={() => handleDeleteAssignment(assignment.homework_id)}
                >
                  Delete
                </Button>
              </Box>
            </CardContent>
          </Card>
        ))
      ) : (
        <Alert severity="info">No assignments found.</Alert>
      )}

      {/* Add Assignment Modal */}
      <AddAssignment
        open={isAddModalOpen}
        onClose={() => setAddModalOpen(false)}
        onSubmit={() => {
          if (user) {
            fetchAssignments(user.user_id); // Refresh assignments list after adding
          }
        }}
        sessionKey={localStorage.getItem("sessionKey")} // Pass session key
        userId={user.user_id} // Pass user ID
      />

      {/* Edit Assignment Modal */}
      {selectedAssignment && (
        <EditAssignment
          open={isEditModalOpen}
          onClose={() => setEditModalOpen(false)}
          onSubmit={handleUpdateAssignment}
          sessionKey={localStorage.getItem("sessionKey")}
          homework={selectedAssignment}
        />
      )}
    </Box>
  );
};

export default HomeworkDashboard;
