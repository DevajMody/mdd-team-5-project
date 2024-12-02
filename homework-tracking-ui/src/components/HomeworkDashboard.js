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
import "../styles/homeworkdashboard.css";
import { Calendar as BigCalendar, dateFnsLocalizer } from "react-big-calendar";
import { format, parse, startOfWeek, getDay } from "date-fns";
import "react-big-calendar/lib/css/react-big-calendar.css";
import enUS from "date-fns/locale/en-US";
import {
  CalendarToday,
  List,
  Add,
  Edit,
  Delete,
  CheckCircle,
} from "@mui/icons-material";
import AddAssignment from "./AddAssignment";
import EditAssignment from "./EditAssignment";
import Logout from "./Logout";
import CalendarView from "./CalendarView";
import SortByPriority from "./SortByPriority";
import { useNavigate } from "react-router-dom";

const locales = { "en-US": enUS };
const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

const HomeworkDashboard = () => {
  const [assignments, setAssignments] = useState([]); // Assignments state
  const [filteredAssignments, setFilteredAssignments] = useState([]); // Filtered by priority
  // const [priority, setPriority] = useState("All"); // Priority filter state
  const [events, setEvents] = useState([]); // Calendar events
  const [user, setUser] = useState(null); // User state
  const [view, setView] = useState("list"); // 'list' or 'calendar'
  const [isAddModalOpen, setAddModalOpen] = useState(false);
  const [isEditModalOpen, setEditModalOpen] = useState(false);
  const [selectedAssignment, setSelectedAssignment] = useState(null); // Selected assignment for editing
  const [dueDates, setDueDates] = useState([]);
  const navigate = useNavigate();
  const [priority, setPriority] = useState("All");

  const fetchUser = async () => {
    const sessionKey = localStorage.getItem("sessionKey");

    if (!sessionKey) {
      console.error("Session key is missing. Redirecting to login.");
      navigate("/");
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
        navigate("/");
      }
    } catch (error) {
      console.error("Error fetching user details:", error);
      navigate("/");
    }
  };

  const fetchAssignments = async (userId) => {
    try {
      const url =
        priority === "All"
          ? `http://localhost:8001/homework/user/${userId}`
          : `http://localhost:8001/homework/priority/${priority}`;
      const response = await fetch(url, {
        headers: {
          "Session-Key": localStorage.getItem("sessionKey"),
        },
      });
      if (response.ok) {
        const data = await response.json();
        setAssignments(data.homework || []);
        setFilteredAssignments(data.homework || []);
        const calendarEvents = data.homework.map((hw) => ({
          title: hw.title,
          start: new Date(hw.due_date),
          end: new Date(hw.due_date),
          homework: hw,
        }));
        setEvents(calendarEvents);
      } else {
        console.error("Failed to fetch assignments:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching assignments:", error);
    }
  };

  const fetchDueDates = async (userId) => {
    try {
      const response = await fetch(
        `http://localhost:8001/homework/due_dates/${userId}`,
        {
          headers: {
            "Session-Key": localStorage.getItem("sessionKey"),
          },
        }
      );
      if (response.ok) {
        const { due_dates } = await response.json();
        setDueDates(due_dates || []);
        console.log("Due dates fetched:", due_dates); // Debug log
      } else {
        console.error("Failed to fetch due dates:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching due dates:", error);
    }
  };

  const handleViewChange = (viewType) => {
    setView(viewType);
    if (viewType === "calendar" && user) {
      fetchDueDates(user.user_id); // Ensure due dates are refreshed when switching to calendar
    }
  };

  const handleEditAssignment = (assignment) => {
    setSelectedAssignment(assignment);
    setEditModalOpen(true);
  };

  const handleMarkAsCompleted = async (assignmentId) => {
    const sessionKey = localStorage.getItem("sessionKey");
    try {
      const response = await fetch(
        `http://localhost:8001/homework/${assignmentId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Session-Key": sessionKey,
          },
          body: JSON.stringify({ is_completed: true }),
        }
      );

      if (response.ok) {
        console.log("Homework marked as completed.");
        fetchAssignments(user.user_id); // Refresh assignments after updating
      } else {
        const errorMsg = await response.text();
        console.error("Failed to mark homework as completed:", errorMsg);
        alert(`Failed to mark homework as completed: ${errorMsg}`);
      }
    } catch (error) {
      console.error("Error marking homework as completed:", error);
      alert("An error occurred while marking the homework as completed.");
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
      fetchAssignments(user.user_id, priority);
    }
  }, [user, priority]);

  useEffect(() => {
    if (user) {
      fetchDueDates(user.user_id); // Fetch due dates for the calendar
    }
  }, [user]);

  // Update filtered assignments when priority changes
  // useEffect(() => {
  //   if (priority === "All") {
  //     setFilteredAssignments(assignments);
  //   } else {
  //     setFilteredAssignments(
  //       assignments.filter((a) => a.priority === priority)
  //     );
  //   }
  // }, [priority, assignments]);

  if (!user) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Box className="dashboard-container">
      {/* Header Section */}
      <Box className="dashboard-header">
        <Box className="dashboard-header-left">
          <img
            src="https://www.rit.edu/brandportal/sites/rit.edu.brandportal/files/2022-10/RIT-00071A_RGB_whiteTM.jpg"
            alt="Homework Tracker Logo"
            className="dashboard-logo"
          />
          <Typography
            className="dashboard-title"
            variant="h4"
            fontWeight="bold"
          >
            My Homework Dashboard
          </Typography>
        </Box>
        <Box className="dashboard-actions">
          <Button
            className={`dashboard-button ${
              view === "list" ? "button-active" : "button-inactive"
            }`}
            variant={view === "list" ? "contained" : "outlined"}
            startIcon={<List />}
            onClick={() => setView("list")}
          >
            List View
          </Button>
          <Button
            className={`dashboard-button ${
              view === "calendar" ? "button-active" : "button-inactive"
            }`}
            variant={view === "calendar" ? "contained" : "outlined"}
            startIcon={<CalendarToday />}
            onClick={() => handleViewChange("calendar")}
          >
            Calendar View
          </Button>
          <Button
            className="add-assignment-button"
            variant="contained"
            color="primary"
            startIcon={<Add />}
            onClick={() => setAddModalOpen(true)}
          >
            Add Assignment
          </Button>
          <Logout sessionKey={localStorage.getItem("sessionKey")} />
        </Box>
      </Box>

      {/* Calendar View */}
      {view === "calendar" && (
        <CalendarView className="calendar-view" dueDates={dueDates} />
      )}

      {/* Sort By Priority */}
      {view === "list" && (
        <Box className="sort-priority-container">
          <SortByPriority priority={priority} setPriority={setPriority} />
        </Box>
      )}

      {/* List View */}
      {view === "list" && (
        <>
          {/* Stats Overview */}
          <Grid className="stats-overview" container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <Card className="stats-card">
                <CardHeader title="Total Assignments" />
                <CardContent>
                  <Typography className="stats-value" variant="h5">
                    {assignments.length}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Assignments List */}
          {assignments.length > 0 ? (
            assignments.map((assignment) => (
              <Card
                key={assignment.homework_id}
                className={`assignment-card ${
                  assignment.is_completed ? "assignment-completed" : ""
                }`}
              >
                <CardContent>
                  <Typography className="assignment-title" variant="h6">
                    {assignment.title}
                  </Typography>
                  <Typography
                    className="assignment-description"
                    variant="body2"
                  >
                    {assignment.description}
                  </Typography>
                  <Typography className="assignment-due-date" variant="caption">
                    Due: {assignment.due_date}
                  </Typography>
                  <Box className="assignment-actions">
                    {!assignment.is_completed && (
                      <Button
                        className="mark-completed-button"
                        startIcon={<CheckCircle />}
                        color="success"
                        onClick={() =>
                          handleMarkAsCompleted(assignment.homework_id)
                        }
                      >
                        Mark as Completed
                      </Button>
                    )}
                    <Button className="edit-button" startIcon={<Edit />}>
                      Edit
                    </Button>
                    <Button
                      className="delete-button"
                      startIcon={<Delete />}
                      color="error"
                      onClick={() =>
                        handleDeleteAssignment(assignment.homework_id)
                      }
                    >
                      Delete
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            ))
          ) : (
            <Alert className="no-assignments-alert" severity="info">
              No assignments found.
            </Alert>
          )}
        </>
      )}

      {/* Add Assignment Modal */}
      <AddAssignment
        open={isAddModalOpen}
        onClose={() => setAddModalOpen(false)}
        onSubmit={() => {
          if (user) {
            fetchAssignments(user.user_id, priority);
            fetchDueDates(user.user_id);
          }
        }}
        sessionKey={localStorage.getItem("sessionKey")}
        userId={user.user_id}
      />

      {/* Edit Assignment Modal */}
      {selectedAssignment && (
        <EditAssignment
          open={isEditModalOpen}
          onClose={() => setEditModalOpen(false)}
          onSubmit={fetchAssignments}
          sessionKey={localStorage.getItem("sessionKey")}
          homework={selectedAssignment}
        />
      )}
    </Box>
  );
};

export default HomeworkDashboard;
