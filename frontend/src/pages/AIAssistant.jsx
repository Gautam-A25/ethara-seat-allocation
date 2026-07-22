import { useState, useRef, useEffect } from "react";
import api from "../services/api";
import { FaRobot, FaUser, FaPaperPlane } from "react-icons/fa";

export default function AIAssistant() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([
    {
      sender: "ai",
      text: "Hello! I'm Ethara AI. Ask me anything about employees, seats, projects or the dashboard.",
    },
  ]);

  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  async function sendMessage() {
    if (!question.trim()) return;

    const userMessage = {
      sender: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    const currentQuestion = question;

    setQuestion("");
    setLoading(true);

    try {
      const res = await api.post("/ai/query", {
        query: currentQuestion,
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: res.data.answer,
        },
      ]);
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: "Sorry, I couldn't process your request.",
        },
      ]);
    }

    setLoading(false);
  }

  return (
    <div className="h-[82vh] flex flex-col">
      <h2 className="text-3xl font-bold mb-6">Ethara AI Assistant</h2>

      <div className="bg-white rounded-xl shadow flex flex-col flex-1">
        <div className="flex-1 overflow-y-auto p-6 space-y-5">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${
                msg.sender === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`flex gap-3 max-w-[75%] ${
                  msg.sender === "user" ? "flex-row-reverse" : ""
                }`}
              >
                <div className="mt-1">
                  {msg.sender === "user" ? (
                    <FaUser size={18} />
                  ) : (
                    <FaRobot size={18} />
                  )}
                </div>

                <div
                  className={`rounded-xl px-4 py-3 whitespace-pre-wrap ${
                    msg.sender === "user"
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100"
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex gap-3">
              <FaRobot size={18} />

              <div className="bg-gray-100 rounded-xl px-4 py-3">
                Thinking...
              </div>
            </div>
          )}

          <div ref={bottomRef}></div>
        </div>

        <div className="border-t p-4 flex gap-3">
          <input
            className="flex-1 border rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Ask about employees, seats, projects..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") sendMessage();
            }}
          />

          <button
            onClick={sendMessage}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 rounded-lg flex items-center gap-2 disabled:bg-gray-400"
          >
            <FaPaperPlane />
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
