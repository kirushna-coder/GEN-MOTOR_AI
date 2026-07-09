import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Home, 
  LayoutDashboard, 
  MessageSquare, 
  FileText, 
  Map, 
  Code, 
  Bug,
  BookOpen,
  LogOut,
  Brain
} from 'lucide-react';

export default function Sidebar() {
  const { user, logout } = useAuth();

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: <LayoutDashboard size={20} /> },
    { name: 'AI Chat Assistant', path: '/chat', icon: <MessageSquare size={20} /> },
    { name: 'AI Projects', path: '/projects', icon: <Code size={20} /> },
    { name: 'Career Roadmap', path: '/roadmap', icon: <Map size={20} /> },
    { name: 'Resume Builder', path: '/resume', icon: <FileText size={20} /> },
    { name: 'Code Reviewer', path: '/code-review', icon: <Code size={20} /> },
    { name: 'Bug Fixer', path: '/bug-fixer', icon: <Bug size={20} /> },
    { name: 'Documentation', path: '/docs', icon: <BookOpen size={20} /> },
  ];

  return (
    <aside className="w-64 bg-card border-r border-border h-screen flex flex-col hidden md:flex sticky top-0">
      <div className="p-6 flex items-center gap-3 border-b border-border">
        <div className="bg-primary/10 p-2 rounded-lg">
          <Brain className="text-primary" size={24} />
        </div>
        <h1 className="font-bold text-xl text-foreground">Genmotor AI</h1>
      </div>
      
      <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => 
              `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors font-medium text-sm ${
                isActive 
                  ? 'bg-primary text-primary-foreground' 
                  : 'text-muted-foreground hover:bg-secondary hover:text-foreground'
              }`
            }
          >
            {item.icon}
            {item.name}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-border">
        <div className="flex items-center gap-3 mb-4 px-2">
          <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-primary-foreground font-bold">
            {user?.name?.charAt(0) || 'U'}
          </div>
          <div className="flex-1 overflow-hidden">
            <p className="text-sm font-medium text-foreground truncate">{user?.name || 'User'}</p>
            <p className="text-xs text-muted-foreground truncate">{user?.email || ''}</p>
          </div>
        </div>
        <button 
          onClick={logout}
          className="flex items-center gap-2 w-full px-3 py-2 text-sm font-medium text-destructive hover:bg-destructive/10 rounded-lg transition-colors"
        >
          <LogOut size={18} />
          Sign Out
        </button>
      </div>
    </aside>
  );
}
