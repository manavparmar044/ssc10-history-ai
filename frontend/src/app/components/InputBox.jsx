import { useState } from "react";

export default function InputBox({ onSubmit, loading }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return; // Prevent empty queries
    onSubmit(query);
    setQuery("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Type your question..."
        className="flex-1 p-3 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        disabled={loading}
      />
      <button
        type="submit"
        disabled={loading}
        className="p-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {loading ? "Sending..." : "Send"}
      </button>
    </form>
  );
}