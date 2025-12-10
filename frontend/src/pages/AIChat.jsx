import { useState, useEffect, useRef } from 'react';
import { sendChatMessage } from '../services/api';
import { IoChatbubbleEllipsesOutline } from 'react-icons/io5';

const AIChat = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m your AI Business Consultant. How can I help you today?',
      timestamp: new Date().toISOString(),
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    setInput('');
    setLoading(true);

    try {
      const response = await sendChatMessage({ message: currentInput });
      
      const assistantMessage = {
        role: 'assistant',
        content: response.answer || 'I received your message.',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center gap-2">
          <IoChatbubbleEllipsesOutline className="w-7 h-7 text-gray-800" />
          <h1 className="text-2xl font-bold text-gray-800">AI Business Consultant</h1>
        </div>
        <p className="text-sm text-gray-500 ml-9">Ask me anything about your business</p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-3xl rounded-lg px-4 py-3 ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-800 shadow border border-gray-200'
              }`}
            >
              <p className="whitespace-pre-wrap">{message.content}</p>
              <div className="mt-1 text-xs opacity-60">
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white rounded-lg px-4 py-3 shadow border border-gray-200">
              <div className="flex gap-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="bg-white border-t border-gray-200 px-6 py-4">
        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask me anything..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIChat;
