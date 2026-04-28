import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Chip,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Snackbar,
  List,
  ListItem,
  ListItemText
} from '@mui/material';
import { Work as WorkIcon } from '@mui/icons-material';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider, DateTimePicker } from '@mui/x-date-pickers';
import { format } from 'date-fns';

function WorkspaceList() {
  const { token, isAuthenticated } = useAuth();
  const queryClient = useQueryClient();
  const [selectedWorkspace, setSelectedWorkspace] = useState(null);
  const [startTime, setStartTime] = useState(new Date());
  const [endTime, setEndTime] = useState(new Date());
  const [openDialog, setOpenDialog] = useState(false);
  const [message, setMessage] = useState({ text: '', severity: 'success' });
  const [showSnackbar, setShowSnackbar] = useState(false);

  // State for View Details
  const [selectedWorkspaceForDetails, setSelectedWorkspaceForDetails] = useState(null);
  const [workspaceSchedule, setWorkspaceSchedule] = useState([]);
  const [isDetailsDialogOpen, setIsDetailsDialogOpen] = useState(false);
  const [scheduleLoading, setScheduleLoading] = useState(false);
  const [scheduleError, setScheduleError] = useState(null);

  const { data: workspaces, isLoading, error } = useQuery({
    queryKey: ['workspaces'],
    queryFn: async () => {
      try {
        console.log('Fetching workspaces with token:', token);
        const response = await axios.get('http://localhost:5000/api/workspaces/', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        console.log('Workspaces response:', response.data);
        return response.data;
      } catch (error) {
        console.error('Error fetching workspaces:', error);
        throw error;
      }
    },
    enabled: !!token && isAuthenticated,
    retry: 1,
    staleTime: 30000
  });

  const createBookingMutation = useMutation({
    mutationFn: async (bookingData) => {
      try {
        console.log('Creating booking with data:', bookingData);
        const response = await axios.post(
          'http://localhost:5000/api/bookings/',
          bookingData,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        );
        console.log('Booking response:', response.data);
        return response.data;
      } catch (error) {
        console.error('Error creating booking:', error);
        throw error;
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['bookings']);
      setMessage({ text: 'Booking created successfully!', severity: 'success' });
      setShowSnackbar(true);
      setOpenDialog(false);
    },
    onError: (error) => {
      setMessage({ 
        text: error.response?.data?.message || 'Failed to create booking', 
        severity: 'error' 
      });
      setShowSnackbar(true);
    }
  });

  const handleBookNow = (workspace) => {
    setSelectedWorkspace(workspace);
    setStartTime(new Date());
    setEndTime(new Date(new Date().getTime() + 60 * 60 * 1000)); // Default to 1 hour
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setSelectedWorkspace(null);
  };

  const handleViewDetails = async (workspace) => {
    setSelectedWorkspaceForDetails(workspace);
    setIsDetailsDialogOpen(true);
    setScheduleLoading(true);
    setScheduleError(null);
    try {
      const response = await axios.get(`http://localhost:5000/api/workspaces/${workspace.id}/bookings`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setWorkspaceSchedule(response.data);
    } catch (err) {
      console.error("Error fetching workspace schedule:", err);
      setScheduleError(err.response?.data?.message || "Failed to load schedule.");
    } finally {
      setScheduleLoading(false);
    }
  };

  const handleCloseDetailsDialog = () => {
    setIsDetailsDialogOpen(false);
    setSelectedWorkspaceForDetails(null);
    setWorkspaceSchedule([]);
    setScheduleError(null);
  };

  const handleCreateBooking = () => {
    if (!selectedWorkspace) return;

    const bookingData = {
      workspace_id: selectedWorkspace.id,
      start_time: startTime.toISOString(),
      end_time: endTime.toISOString()
    };

    createBookingMutation.mutate(bookingData);
  };

  if (!isAuthenticated) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="warning">
          Please log in to view and book workspaces.
        </Alert>
      </Container>
    );
  }

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
          Error loading workspaces: {error.message}
          {error.response?.data?.message && (
            <Box sx={{ mt: 1 }}>
              Details: {error.response.data.message}
            </Box>
          )}
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Available Workspaces
        </Typography>
        <Grid container spacing={4}>
          {workspaces?.map((workspace) => (
            <Grid item xs={12} sm={6} md={4} key={workspace.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <WorkIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="h6" component="h2">
                      {workspace.name}
                    </Typography>
                  </Box>
                  <Typography color="text.secondary" paragraph>
                    {workspace.description}
                  </Typography>
                  <Box sx={{ mb: 2 }}>
                    <Chip
                      label={`Capacity: ${workspace.capacity} people`}
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    <Chip
                      label={workspace.is_available ? 'Available' : 'Occupied'}
                      color={workspace.is_available ? 'success' : 'error'}
                      size="small"
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    Price: ${workspace.price_per_hour}/hour
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button
                    size="small"
                    variant="contained"
                    disabled={!workspace.is_available}
                    onClick={() => handleBookNow(workspace)}
                  >
                    Book Now
                  </Button>
                  <Button size="small" onClick={() => handleViewDetails(workspace)}>View Details</Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>Book Workspace</DialogTitle>
        <DialogContent>
          {selectedWorkspace && (
            <Box sx={{ pt: 2 }}>
              <Typography variant="h6" gutterBottom>
                {selectedWorkspace.name}
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
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button 
            onClick={handleCreateBooking}
            variant="contained"
            disabled={createBookingMutation.isLoading}
          >
            {createBookingMutation.isLoading ? 'Creating...' : 'Confirm Booking'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Workspace Details Dialog */}
      <Dialog open={isDetailsDialogOpen} onClose={handleCloseDetailsDialog} fullWidth maxWidth="sm">
        <DialogTitle>
          {selectedWorkspaceForDetails ? `${selectedWorkspaceForDetails.name} - Schedule` : 'Workspace Schedule'}
        </DialogTitle>
        <DialogContent>
          {scheduleLoading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
              <CircularProgress />
            </Box>
          )}
          {scheduleError && (
            <Alert severity="error" sx={{ mb: 2 }}>{scheduleError}</Alert>
          )}
          {!scheduleLoading && !scheduleError && selectedWorkspaceForDetails && (
            <>
              {workspaceSchedule.length > 0 ? (
                <List dense>
                  {workspaceSchedule.map((booking) => (
                    <ListItem key={booking.id}>
                      <ListItemText
                        primary={`Booked: ${format(new Date(booking.start_time), 'PP HH:mm')} - ${format(new Date(booking.end_time), 'PP HH:mm')}`}
                        secondary={`Status: ${booking.status}`}
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body1">No current bookings for this workspace.</Typography>
              )}
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDetailsDialog}>Close</Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={showSnackbar}
        autoHideDuration={6000}
        onClose={() => setShowSnackbar(false)}
      >
        <Alert 
          onClose={() => setShowSnackbar(false)} 
          severity={message.severity}
          sx={{ width: '100%' }}
        >
          {message.text}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default WorkspaceList; 