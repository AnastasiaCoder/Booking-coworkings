import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Container,
  Grid,
  Typography,
  Card,
  CardContent,
  CardActions,
} from '@mui/material';
import {
  Work as WorkIcon,
  EventNote as EventNoteIcon,
  Person as PersonIcon,
} from '@mui/icons-material';

const features = [
  {
    title: 'Find Workspaces',
    description: 'Browse and book available workspaces in our coworking space.',
    icon: <WorkIcon sx={{ fontSize: 40 }} />,
    action: 'View Workspaces',
    path: '/workspaces',
  },
  {
    title: 'Manage Bookings',
    description: 'View and manage your workspace bookings.',
    icon: <EventNoteIcon sx={{ fontSize: 40 }} />,
    action: 'View Bookings',
    path: '/bookings',
  },
  {
    title: 'Your Profile',
    description: 'Manage your account settings and preferences.',
    icon: <PersonIcon sx={{ fontSize: 40 }} />,
    action: 'View Profile',
    path: '/profile',
  },
];

function Home() {
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 8, textAlign: 'center' }}>
        <Typography variant="h2" component="h1" gutterBottom>
          Welcome to Coworking Space
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          Find and book workspaces that suit your needs
        </Typography>
        <Button
          variant="contained"
          size="large"
          onClick={() => navigate('/workspaces')}
          sx={{ mt: 2 }}
        >
          Get Started
        </Button>
      </Box>

      <Grid container spacing={4}>
        {features.map((feature) => (
          <Grid item xs={12} md={4} key={feature.title}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                textAlign: 'center',
                p: 2,
              }}
            >
              <Box sx={{ color: 'primary.main', mb: 2 }}>{feature.icon}</Box>
              <CardContent>
                <Typography gutterBottom variant="h5" component="h2">
                  {feature.title}
                </Typography>
                <Typography color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={() => navigate(feature.path)}
                >
                  {feature.action}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

export default Home; 