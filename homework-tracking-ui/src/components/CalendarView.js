import React from "react";
import { Calendar as BigCalendar, dateFnsLocalizer } from "react-big-calendar";
import { format, parse, startOfWeek, getDay } from "date-fns";
import "react-big-calendar/lib/css/react-big-calendar.css";
import enUS from "date-fns/locale/en-US";
import { Typography, Box } from "@mui/material";

const locales = { "en-US": enUS };

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

const CalendarView = ({ dueDates }) => {
  // Map dueDates to calendar events
  const calendarEvents = dueDates.map((hw) => ({
    title: hw.title, // Extract title
    start: new Date(hw.due_date), // Use due_date as start date
    end: new Date(hw.due_date), // Use due_date as end date
  }));

  // Define event styles
  const eventStyleGetter = (event) => {
    const style = {
      backgroundColor: "#2196f3", // Blue background
      borderRadius: "5px",
      color: "white",
      border: "0",
      display: "block",
      padding: "5px",
    };
    return { style };
  };

  return (
    <Box sx={{ padding: 3 }}>
      <Typography variant="h5" gutterBottom>
        Homework Calendar
      </Typography>
      <BigCalendar
        localizer={localizer}
        events={calendarEvents}
        startAccessor="start"
        endAccessor="end"
        style={{ height: 500 }}
        eventPropGetter={eventStyleGetter}
        onSelectEvent={(event) => alert(`Homework: ${event.title}`)} // Optional click handler
      />
    </Box>
  );
};

export default CalendarView;
