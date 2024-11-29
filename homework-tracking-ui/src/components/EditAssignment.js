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

const EditAssignment = ({ open, onClose, onSubmit, sessionKey, homework }) => {
  const [title, setTitle] = useState(homework.title || "");
  const [description, setDescription] = useState(homework.description || "");
  const [dueDate, setDueDate] = useState(homework.due_date || "");
  const [subject, setSubject] = useState(homework.subject || "");
  const [priority, setPriority] = useState(homework.priority || "");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (isSubmitting) return;

    const updatedAssignment = {
      title,
      description,
      due_date: dueDate,
      subject,
      priority,
    };

    setIsSubmitting(true);

    try {
      const response = await fetch(
        `http://localhost:8001/homework/${homework.homework_id}`,
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
        await onSubmit(updatedAssignment);
        onClose();
      } else {
        const errorMsg = await response.text();
        console.error("Failed to update assignment:", errorMsg);
        alert(`Failed to update assignment: ${errorMsg}`);
      }
    } catch (error) {
      console.error("Error updating assignment:", error);
      alert("An error occurred while updating the assignment.");
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
          Edit Assignment
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
          <FormControl fullWidth margin="normal">
            <InputLabel>Subject</InputLabel>
            <Select
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              required
              disabled={isSubmitting}
            >
              <MenuItem value="Mathematics">Mathematics</MenuItem>
              <MenuItem value="Physics">Physics</MenuItem>
              <MenuItem value="Chemistry">Chemistry</MenuItem>
              <MenuItem value="English">English</MenuItem>
            </Select>
          </FormControl>
          <FormControl fullWidth margin="normal">
            <InputLabel>Priority</InputLabel>
            <Select
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
              required
              disabled={isSubmitting}
            >
              <MenuItem value="High">High</MenuItem>
              <MenuItem value="Medium">Medium</MenuItem>
              <MenuItem value="Low">Low</MenuItem>
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
            {isSubmitting ? "Updating..." : "Update"}
          </Button>
        </form>
      </Box>
    </Modal>
  );
};

export default EditAssignment;
