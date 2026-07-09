import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';

import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import Dashboard from './pages/Dashboard/Dashboard';
import Chat from './pages/Chat/Chat';
import Projects from './pages/Tools/Projects';
import Layout from './components/Layout';

const ProtectedRoute = ({ children }) => {
  const { token, loading } = useAuth();
  if (loading) return <div>Loading...</div>;
  if (!token) return <Navigate to="/login" />;
  return <Layout>{children}</Layout>;
};

const Home = () => <div className="p-8 text-center"><h1 className="text-3xl font-bold">Home Page</h1></div>;

// Placeholders for other tools
const Roadmap = () => <div className="p-8"><h1 className="text-2xl font-bold">Career Roadmap Builder</h1><p className="mt-2 text-muted-foreground">Coming soon!</p></div>;
const Resume = () => <div className="p-8"><h1 className="text-2xl font-bold">AI Resume Builder</h1><p className="mt-2 text-muted-foreground">Coming soon!</p></div>;

function App() {
  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col font-sans">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/chat" 
          element={
            <ProtectedRoute>
              <Chat />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/projects" 
          element={
            <ProtectedRoute>
              <Projects />
            </ProtectedRoute>
          } 
        />
        <Route path="/roadmap" element={<ProtectedRoute><Roadmap /></ProtectedRoute>} />
        <Route path="/resume" element={<ProtectedRoute><Resume /></ProtectedRoute>} />
      </Routes>
    </div>
  );
}

export default App;
