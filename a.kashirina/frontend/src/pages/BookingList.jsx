import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Box,
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  IconButton,
  Chip,
  CircularProgress,
  Alert,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import axios from 'axios';
import { format } from 'date-fns';
import { useAuth } from '../contexts/AuthContext';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';

function getStatusColor(status) {
  switch (status.toLowerCase()) {
    case 'confirmed':
      return 'success';
    case 'pending':
      return 'warning';
    case 'cancelled':
      return 'error';
    default:
      return 'default';
  }
}

function BookingList() {
  const { token } = useAuth();
  const queryClient = useQueryClient();
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [selectedBooking, setSelectedBooking] = useState(null);
  const [startTime, setStartTime] = useState(new Date());
  const [endTime, setEndTime] = useState(new Date());
  
  const { data: bookings, isLoading, error } = useQuery({
    queryKey: ['bookings'],
    queryFn: async () => {
      const response = await axios.get('http://localhost:5000/api/bookings/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      return response.data;
    },
    enabled: !!token
  });

  const confirmBookingMutation = useMutation({
    mutationFn: async (bookingId) => {
      const response = await axios.post(
        `http://localhost:5000/api/bookings/${bookingId}/confirm`,
        {},
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['bookings']);
    },
    onError: (error) => {
      console.error('Error confirming booking:', error);
    }
  });

  const deleteBookingMutation = useMutation({
    mutationFn: async (bookingId) => {
      const response = await axios.delete(
        `http://localhost:5000/api/bookings/${bookingId}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['bookings']);
    },
    onError: (error) => {
      console.error('Error deleting booking:', error);
    }
  });

  const updateBookingMutation = useMutation({
    mutationFn: async ({ bookingId, bookingData }) => {
      const response = await axios.put(
        `http://localhost:5000/api/bookings/${bookingId}`,
        bookingData,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['bookings']);
      setEditDialogOpen(false);
      setSelectedBooking(null);
    },
    onError: (error) => {
      console.error('Error updating booking:', error);
    }
  });

  const handleConfirmBooking = (bookingId) => {
    confirmBookingMutation.mutate(bookingId);
  };

  const handleDeleteBooking = (bookingId) => {
    if (window.confirm('Are you sure you want to delete this booking?')) {
      deleteBookingMutation.mutate(bookingId);
    }
  };

  const handleEditClick = (booking) => {
    setSelectedBooking(booking);
    setStartTime(new Date(booking.start_time));
    setEndTime(new Date(booking.end_time));
    setEditDialogOpen(true);
  };

  const handleCloseEditDialog = () => {
    setEditDialogOpen(false);
    setSelectedBooking(null);
  };

  const handleUpdateBooking = () => {
    if (!selectedBooking) return;

    const bookingData = {
      start_time: startTime.toISOString(),
      end_time: endTime.toISOString(),
      status: selectedBooking.status
    };

    updateBookingMutation.mutate({
      bookingId: selectedBooking.id,
      bookingData
    });
  };

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error">
          Error loading bookings: {error.message}
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Your Bookings
        </Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Workspace</TableCell>
                <TableCell>Start Time</TableCell>
                <TableCell>End Time</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {bookings?.map((booking) => (
                <TableRow key={booking.id}>
                  <TableCell>{booking.workspace_name}</TableCell>
                  <TableCell>
                    {format(new Date(booking.start_time), 'PP HH:mm')}
                  </TableCell>
                  <TableCell>
                    {format(new Date(booking.end_time), 'PP HH:mm')}
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={booking.status}
                      color={getStatusColor(booking.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    {booking.status === 'pending' && (
                      <IconButton
                        size="small"
                        color="success"
                        onClick={() => handleConfirmBooking(booking.id)}
                        disabled={confirmBookingMutation.isLoading}
                      >
                        <CheckCircleIcon />
                      </IconButton>
                    )}
                    <IconButton 
                      size="small" 
                      color="primary"
                      onClick={() => handleEditClick(booking)}
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton 
                      size="small" 
                      color="error"
                      onClick={() => handleDeleteBooking(booking.id)}
                      disabled={deleteBookingMutation.isLoading}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>

      {/* Edit Booking Dialog */}
      <Dialog open={editDialogOpen} onClose={handleCloseEditDialog}>
        <DialogTitle>Edit Booking</DialogTitle>
        <DialogContent>
          {selectedBooking && (
            <Box sx={{ pt: 2 }}>
              <Typography variant="h6" gutterBottom>
                {selectedBooking.workspace_name}
              </Typography>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <Box sx={{ mb: 2 }}>
                  <DateTimePicker
                    label="Start Time"
                    value={startTime}
                    onChange={setStartTime}
                    renderInput={(params) => <TextField {...params} fullWidth />}
                    ampm={false}
                  />
                </Box>
                <Box sx={{ mb: 2 }}>
                  <DateTimePicker
                    label="End Time"
                    value={endTime}
                    onChange={setEndTime}
                    renderInput={(params) => <TextField {...params} fullWidth />}
                    minDateTime={startTime}
                    ampm={false}
                  />
                </Box>
              </LocalizationProvider>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseEditDialog}>Cancel</Button>
          <Button 
            onClick={handleUpdateBooking}
            variant="contained"
            disabled={updateBookingMutation.isLoading}
          >
            {updateBookingMutation.isLoading ? 'Updating...' : 'Update Booking'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default BookingList; 