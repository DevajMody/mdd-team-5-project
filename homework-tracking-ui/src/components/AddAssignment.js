import React, { useState } from "react";
import {
  Modal,
  Box,
  TextField,
  Button,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material";

const AddAssignment = ({ open, onClose, onSubmit, sessionKey, userId }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [priority, setPriority] = useState("");
  const [subject, setSubject] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Prevent multiple submissions
    if (isSubmitting) return;

    const newAssignment = {
      title,
      description,
      due_date: dueDate,
      priority,
      subject,
    };

    if (!sessionKey) {
      console.error("No session key found. User might not be logged in.");
      alert("You need to log in to add an assignment.");
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch("http://localhost:8001/homework", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Session-Key": sessionKey,
        },
        body: JSON.stringify(newAssignment),
      });

      if (response.ok) {
        console.log("Assignment added successfully.");

        // Wait for the onSubmit to complete before closing
        await onSubmit(newAssignment);

        // Reset form
        setTitle("");
        setDescription("");
        setDueDate("");
        setPriority("");
        setSubject("");

        onClose(); // Close modal
      } else {
        const errorMsg = await response.text();
        console.error("Failed to add assignment:", errorMsg);
        alert(`Failed to add assignment: ${errorMsg}`);
      }
    } catch (error) {
      console.error("Error adding assignment:", error);
      alert("An error occurred while adding the assignment.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box
        sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: 400,
          bgcolor: "background.paper",
          boxShadow: 24,
          p: 4,
          borderRadius: 2,
        }}
      >
        <Typography variant="h6" gutterBottom>
          Add New Assignment
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Title"
            variant="outlined"
            fullWidth
            margin="normal"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            disabled={isSubmitting}
          />
          <TextField
            label="Description"
            variant="outlined"
            fullWidth
            margin="normal"
            multiline
            rows={3}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
            disabled={isSubmitting}
          />
          <TextField
            label="Due Date"
            variant="outlined"
            fullWidth
            margin="normal"
            type="date"
            InputLabelProps={{ shrink: true }}
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            required
            disabled={isSubmitting}
          />
          <FormControl fullWidth margin="normal" disabled={isSubmitting}>
            <InputLabel>Priority</InputLabel>
            <Select
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
              required
            >
              <MenuItem value="High">High</MenuItem>
              <MenuItem value="Normal">Medium</MenuItem>
              <MenuItem value="Low">Low</MenuItem>
            </Select>
          </FormControl>
          <FormControl fullWidth margin="normal" disabled={isSubmitting}>
            <InputLabel>Subject</InputLabel>
            <Select
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              required
            >
              <MenuItem value="Mathematics">Mathematics</MenuItem>
              <MenuItem value="Physics">Physics</MenuItem>
              <MenuItem value="Chemistry">Chemistry</MenuItem>
              <MenuItem value="English">English</MenuItem>
              {/* Add more subjects as needed */}
            </Select>
          </FormControl>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            sx={{ mt: 2 }}
            disabled={isSubmitting}
          >
            {isSubmitting ? "Submitting..." : "Submit"}
          </Button>
        </form>
      </Box>
    </Modal>
  );
};

export default AddAssignment;
