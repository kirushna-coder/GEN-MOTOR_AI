import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { MessageSquare, Code, Map, FileText } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const { user } = useAuth();

  const tools = [
    { title: 'AI Chat Assistant', desc: 'Ask anything, get instant code help.', icon: <MessageSquare size={24} />, path: '/chat', color: 'bg-blue-500/10 text-blue-500' },
    { title: 'AI Project Generator', desc: 'Generate complete project architectures.', icon: <Code size={24} />, path: '/projects', color: 'bg-green-500/10 text-green-500' },
    { title: 'Career Roadmap', desc: 'Personalized step-by-step learning paths.', icon: <Map size={24} />, path: '/roadmap', color: 'bg-purple-500/10 text-purple-500' },
    { title: 'Resume Builder', desc: 'AI-driven resume feedback and improvement.', icon: <FileText size={24} />, path: '/resume', color: 'bg-orange-500/10 text-orange-500' }
  ];

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Welcome back, {user?.name}! 👋</h1>
        <p className="text-muted-foreground mt-2 text-lg">What would you like to build today?</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {tools.map((tool) => (
          <Link key={tool.path} to={tool.path} className="block group">
            <div className="bg-card border border-border hover:border-primary/50 rounded-xl p-6 transition-all shadow-sm hover:shadow-md h-full flex flex-col">
              <div className={`w-12 h-12 rounded-lg flex items-center justify-center mb-4 ${tool.color}`}>
                {tool.icon}
              </div>
              <h3 className="text-xl font-semibold text-foreground group-hover:text-primary transition-colors">{tool.title}</h3>
              <p className="text-muted-foreground mt-2 flex-1">{tool.desc}</p>
            </div>
          </Link>
        ))}
      </div>
      
      <div className="bg-secondary rounded-xl p-6 border border-border">
        <h3 className="text-lg font-semibold text-foreground mb-2">Recent Activity</h3>
        <p className="text-muted-foreground text-sm">Your recent chats and generations will appear here.</p>
        <div className="mt-4 p-4 border border-dashed border-border rounded-lg text-center text-muted-foreground">
          No recent activity found.
        </div>
      </div>
    </div>
  );
}
