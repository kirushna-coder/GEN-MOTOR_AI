import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { Code, Sparkles, Loader2, Search } from 'lucide-react';

export default function Projects() {
  const [stack, setStack] = useState('React, Node.js, MongoDB');
  const [difficulty, setDifficulty] = useState('Intermediate');
  const [domain, setDomain] = useState('E-commerce');
  const [projects, setProjects] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const { token } = useAuth();

  const handleGenerate = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:5000/api/generate-project', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify({ stack, difficulty, domain })
      });
      const data = await res.json();
      if (data.status === 'success') {
        setProjects(data.data);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold flex items-center gap-3">
          <Code className="text-primary" size={32} />
          AI Project Generator
        </h1>
        <p className="text-muted-foreground mt-2">Generate tailored project ideas with full architectures.</p>
      </div>

      <div className="bg-card border border-border p-6 rounded-xl shadow-sm">
        <form onSubmit={handleGenerate} className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium mb-1">Tech Stack</label>
            <input 
              type="text" 
              value={stack}
              onChange={(e) => setStack(e.target.value)}
              className="w-full bg-background border border-border rounded-lg px-4 py-2"
              placeholder="e.g. Python, Flask, React"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Difficulty</label>
            <select 
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="w-full bg-background border border-border rounded-lg px-4 py-2"
            >
              <option>Beginner</option>
              <option>Intermediate</option>
              <option>Advanced</option>
            </select>
          </div>
          <button 
            type="submit" 
            disabled={isLoading}
            className="w-full bg-primary text-primary-foreground py-2 px-4 rounded-lg font-medium flex items-center justify-center gap-2 hover:opacity-90 disabled:opacity-50"
          >
            {isLoading ? <Loader2 className="animate-spin" size={18} /> : <Sparkles size={18} />}
            Generate
          </button>
        </form>
      </div>

      {projects.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {projects.map((proj, idx) => (
            <div key={idx} className="bg-card border border-border rounded-xl p-6 hover:shadow-md transition-shadow flex flex-col">
              <div className="text-4xl mb-4">{proj.icon}</div>
              <h3 className="text-xl font-bold mb-2">{proj.title}</h3>
              <p className="text-muted-foreground mb-4 flex-1">{proj.desc}</p>
              <div className="flex flex-wrap gap-2 mb-6">
                {proj.tags.map(tag => (
                  <span key={tag} className="bg-secondary text-secondary-foreground text-xs px-2 py-1 rounded-full font-medium">
                    {tag}
                  </span>
                ))}
              </div>
              <button className="w-full border border-primary text-primary hover:bg-primary/10 py-2 rounded-lg font-medium transition-colors flex items-center justify-center gap-2">
                <Search size={16} /> View Architecture
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
