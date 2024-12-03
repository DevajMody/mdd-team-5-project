import React from "react";
import { Select, MenuItem, FormControl, InputLabel } from "@mui/material";

const SortByPriority = ({ priority, setPriority }) => {
  return (
    <FormControl fullWidth>
      <InputLabel id="priority-sort-label">Sort By Priority</InputLabel>
      <Select
        labelId="priority-sort-label"
        value={priority}
        onChange={(e) => setPriority(e.target.value)}
      >
        <MenuItem value="All">All</MenuItem>
        <MenuItem value="High">High</MenuItem>
        <MenuItem value="Normal">Normal</MenuItem>
        <MenuItem value="Low">Low</MenuItem>
      </Select>
    </FormControl>
  );
};

export default SortByPriority;
