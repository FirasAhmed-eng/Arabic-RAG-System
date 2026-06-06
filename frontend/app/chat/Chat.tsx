
import { useState } from "react";
import axios from "axios";

export default function Chat() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");

  const handleChat = async () => {
    try {
      const response = await axios.get(
        "http://localhost:8000/api/chat",
        {
          params: {
            query,
            collection_name: "rag",
          },
        }
      );

      setAnswer(response.data.answer);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question..."
      />

      <button onClick={handleChat}>
        Send
      </button>

      <p>{answer}</p>
    </div>
  );
}