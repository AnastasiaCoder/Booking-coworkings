import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  Grid,
  Alert,
  Snackbar
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';

const Profile = () => {
  const { user, token } = useAuth();
  const [profile, setProfile] = useState({
    first_name: '',
    last_name: '',
    email: ''
  });
  const [password, setPassword] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);

  useEffect(() => {
    if (user) {
      setProfile({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email
      });
    }
  }, [user]);

  const handleProfileChange = (e) => {
    setProfile({
      ...profile,
      [e.target.name]: e.target.value
    });
  };

  const handlePasswordChange = (e) => {
    setPassword({
      ...password,
      [e.target.name]: e.target.value
    });
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/api/auth/me', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          first_name: profile.first_name,
          last_name: profile.last_name
        })
      });

      if (!response.ok) {
        throw new Error('Failed to update profile');
      }

      setMessage('Profile updated successfully');
      setOpenSnackbar(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update profile');
      setOpenSnackbar(true);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    if (password.new_password !== password.confirm_password) {
      setError('New passwords do not match');
      setOpenSnackbar(true);
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/auth/me/password', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          current_password: password.current_password,
          new_password: password.new_password
        })
      });

      if (!response.ok) {
        throw new Error('Failed to update password');
      }

      setPassword({
        current_password: '',
        new_password: '',
        confirm_password: ''
      });
      setMessage('Password updated successfully');
      setOpenSnackbar(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update password');
      setOpenSnackbar(true);
    }
  };

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
    setMessage('');
    setError('');
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Profile Information
            </Typography>
            <Box component="form" onSubmit={handleProfileSubmit}>
              <TextField
                fullWidth
                label="Email"
                value={profile.email}
                disabled
                margin="normal"
              />
              <TextField
                fullWidth
                label="First Name"
                name="first_name"
                value={profile.first_name}
                onChange={handleProfileChange}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Last Name"
                name="last_name"
                value={profile.last_name}
                onChange={handleProfileChange}
                margin="normal"
              />
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                sx={{ mt: 2 }}
              >
                Update Profile
              </Button>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Change Password
            </Typography>
            <Box component="form" onSubmit={handlePasswordSubmit}>
              <TextField
                fullWidth
                label="Current Password"
                name="current_password"
                type="password"
                value={password.current_password}
                onChange={handlePasswordChange}
                margin="normal"
              />
              <TextField
                fullWidth
                label="New Password"
                name="new_password"
                type="password"
                value={password.new_password}
                onChange={handlePasswordChange}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Confirm New Password"
                name="confirm_password"
                type="password"
                value={password.confirm_password}
                onChange={handlePasswordChange}
                margin="normal"
              />
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                sx={{ mt: 2 }}
              >
                Change Password
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      <Snackbar
        open={openSnackbar}
        autoHideDuration={6000}
        onClose={handleCloseSnackbar}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity={error ? 'error' : 'success'}
          sx={{ width: '100%' }}
        >
          {error || message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Profile; 