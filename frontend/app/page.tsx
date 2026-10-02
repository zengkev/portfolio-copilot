"use client";

import { useState, useRef, useEffect } from "react";
import { Send, User, Building2, Loader2 } from "lucide-react";

type Message = {
  role: "user" | "ai";
  content: string;
};

export default function ChatCopilot() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "ai",
      content: "Hello! I am your Kensington Manor Property Copilot. Ask me about building rules, alterations, or lease clauses.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  
  // Auto-scroll to the bottom when new messages arrive
  const messagesEndRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) throw new Error("Failed to fetch response");

      const data = await response.json();

      // Guard against objects by converting to string safely
      const rawResponse = data.response;
      const aiResponseText = typeof rawResponse === "object" 
        ? JSON.stringify(rawResponse) 
        : String(rawResponse);
        
      setMessages((prev) => [...prev, { role: "ai", content: aiResponseText }]);
    } catch (error) {
      console.error("Error connecting to backend:", error);
      setMessages((prev) => [
        ...prev,
        { role: "ai", content: "Error: Could not connect to the backend API. Is FastAPI running?" },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50 font-sans">
      {/* Header */}
      <header className="bg-white border-b shadow-sm py-4 px-6 flex items-center gap-3">
        <div className="p-2 bg-blue-600 rounded-lg text-white">
          <Building2 size={24} />
        </div>
        <div>
          <h1 className="text-xl font-bold text-slate-800">Portfolio Copilot</h1>
          <p className="text-xs text-slate-500">Powered by LangGraph & Gemini</p>
        </div>
      </header>

      {/* Chat Window */}
      <main className="flex-1 overflow-y-auto p-4 md:p-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex gap-4 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              {msg.role === "ai" && (
                <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 shrink-0">
                  <Building2 size={18} />
                </div>
              )}
              
              <div
                className={`px-4 py-3 rounded-2xl max-w-[85%] leading-relaxed ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white rounded-br-sm"
                    : "bg-white text-slate-800 border shadow-sm rounded-bl-sm"
                }`}
              >
                {msg.content}
              </div>

              {msg.role === "user" && (
                <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center text-slate-600 shrink-0">
                  <User size={18} />
                </div>
              )}
            </div>
          ))}
          
          {isLoading && (
            <div className="flex gap-4 justify-start">
              <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 shrink-0">
                <Building2 size={18} />
              </div>
              <div className="px-4 py-3 rounded-2xl bg-white border shadow-sm rounded-bl-sm flex items-center gap-2 text-slate-500">
                <Loader2 size={16} className="animate-spin" />
                <span className="text-sm">Searching building documents...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Bar */}
      <footer className="bg-white border-t p-4 md:p-6">
        <div className="max-w-3xl mx-auto">
          <form
            onSubmit={sendMessage}
            className="flex items-center gap-2 bg-slate-100 p-2 rounded-full border focus-within:ring-2 focus-within:ring-blue-500 transition-all"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about sublet rules, alteration policies, or HVAC maintenance..."
              className="flex-1 bg-transparent px-4 py-2 outline-none text-slate-800 placeholder-slate-400"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="p-3 rounded-full bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send size={18} />
            </button>
          </form>
        </div>
      </footer>
    </div>
  );
}