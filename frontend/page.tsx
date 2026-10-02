'use client';
import { useEffect, useState } from 'react';

export default function Home() {
  const [apiStatus, setApiStatus] = useState<string>('Pinging backend...');

  useEffect(() => {
    // Fetch data from our FastAPI health endpoint
    fetch('http://127.0.0.1:8000/api/health')
      .then((res) => res.json())
      .then((data) => setApiStatus(data.status))
      .catch(() => setApiStatus('Failed to connect to backend.'));
  }, []);

  return (
    <main className="min-h-screen p-12 bg-gray-50 font-sans text-gray-900">
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold tracking-tight">Portfolio Analysis Copilot</h1>
        
        <div className="p-6 bg-white rounded-lg shadow-sm border border-gray-200">
          <h2 className="text-sm font-medium text-gray-500 uppercase tracking-wider mb-2">
            System Status
          </h2>
          <div className="flex items-center space-x-3">
            <div className={`h-3 w-3 rounded-full ${apiStatus.includes('online') ? 'bg-green-500' : 'bg-yellow-500 animate-pulse'}`} />
            <p className="font-mono text-sm">{apiStatus}</p>
          </div>
        </div>
      </div>
    </main>
  );
}