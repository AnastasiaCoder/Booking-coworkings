import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './theme';
import { AuthProvider } from './contexts/AuthContext';

// Pages
import Home from './pages/Home';
import WorkspaceList from './pages/WorkspaceList';
import BookingList from './pages/BookingList';
import Profile from './pages/Profile';
import Login from './pages/Login';
import Register from './pages/Register';

// Components
import Layout from './components/Layout';

const queryClient = new QueryClient();

const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/" element={<Layout />}>
              <Route index element={<Home />} />
              <Route path="workspaces" element={<WorkspaceList />} />
              <Route path="bookings" element={<BookingList />} />
              <Route path="profile" element={<Profile />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
};

export default App; 