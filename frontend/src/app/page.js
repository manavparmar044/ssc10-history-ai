"use client";

import { useState } from "react";
import { fetchAnswer } from "./utils/api";
import InputBox from "./components/InputBox";
import AnswerBox from "./components/AnswerBox";

export default function Home() {
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleQuery = async (query) => {
    setLoading(true);
  setResponse(null); // Clear previous response

  const answer = await fetchAnswer(query);

  setResponse({
    query,  // Store user question
    answer, // Store bot response
  });

  setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4">
      {/* Header */}
      <div className="w-full max-w-2xl text-center mb-8">
        <h1 className="text-4xl font-bold mb-2">Q&A Chatbot</h1>
        <p className="text-gray-400">Ask me anything about history!</p>
      </div>

      {/* Chat Container */}
      <div className="w-full max-w-2xl bg-gray-800 rounded-lg shadow-lg flex flex-col h-[600px] text-white">
        {/* Chat History */}
        <div className="flex-1 p-6 overflow-y-auto">
          {response ? (
            <div className="space-y-4">
              {/* User Query */}
              <div className="flex justify-end">
                <div className="bg-blue-500 text-white rounded-lg p-3 max-w-[70%]">
                  <p>{response?.query}</p>
                </div>
              </div>

              {/* Bot Response */}
              <div className="flex justify-start">
                <div className="bg-gray-700 text-white rounded-lg p-3 max-w-[70%]">
                  <p className="text-white">{response?.answer}</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-full">
              <p className="text-gray-400">No conversation yet. Ask me something!</p>
            </div>
          )}
        </div>

        {/* Input Box */}
        <div className="p-4 border-t border-gray-700">
          <InputBox onSubmit={handleQuery} loading={loading} />
        </div>
      </div>
    </div>
  );
}