import React, { useEffect } from "react";
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
    priority: hw.priority || "unknown", // Include priority for styling
  }));

  // Update the eventStyleGetter function
  const eventStyleGetter = (event) => {
    let backgroundColor;
    switch (event.priority?.toLowerCase()) {
      case "high":
        backgroundColor = "#ffcccc"; // Light red
        break;
      case "medium":
      case "normal": // Handle "Normal" as "Medium"
        backgroundColor = "#ffeaa7"; // Light orange
        break;
      case "low":
        backgroundColor = "#ccffcc"; // Light green
        break;
      default:
        backgroundColor = "#d3d3d3"; // Default gray for unknown priority
    }

    return {
      style: {
        backgroundColor,
        color: "black", // Ensure text is readable
        borderRadius: "5px",
        border: `1px solid ${backgroundColor}`,
      },
    };
  };

  useEffect(() => {
    console.log("calendarEvents:", calendarEvents);
  }, [calendarEvents]);

  return (
    <Box sx={{ padding: 3 }}>
      <Typography variant="h5" gutterBottom>
        Homework Calendar
      </Typography>
      <BigCalendar
        localizer={localizer}
        events={calendarEvents} // Use the generated events
        startAccessor="start"
        endAccessor="end"
        style={{ height: 600, margin: "20px" }}
        eventPropGetter={eventStyleGetter} // Apply dynamic styling
      />
    </Box>
  );
};

export default CalendarView;
