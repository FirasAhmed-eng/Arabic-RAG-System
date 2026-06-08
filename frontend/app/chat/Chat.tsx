"use client";

import { useState } from "react";
import axios from "axios";
import { SendHorizontal } from "lucide-react";
export default function Chat() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChat = async () => {
    if (!query.trim()) return;

    setLoading(true);

    try {
      const response = await axios.get("http://localhost:8000/api/chat", {
        params: {
          query,
          collection_name: "rag",
        },
      });

      setAnswer(response.data.answer);
    } catch (error) {
      console.error(error);
      setAnswer("حدث خطأ أثناء جلب الإجابة");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <div className="bg-card text-card-foreground border border-border rounded-xl p-6 space-y-4">
        <div className="space-y-2">
          <label className="text-sm text-muted-foreground">
            اطرح سؤالاً حول المستندات
          </label>

          <input
            dir="rtl"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="اكتب سؤالك هنا..."
            className="
              w-full
              rounded-lg
              border
              border-border
              bg-background
              px-4
              py-3
              focus:outline-none
              focus:ring-2
              focus:ring-ring
            "
          />
        </div>

        <div className="flex justify-end">
          <button
            onClick={handleChat}
            disabled={loading}
            className="
      cursor-pointer
      bg-primary
      text-primary-foreground
      px-5
      py-2
      rounded-lg
      font-medium
      disabled:opacity-50
      disabled:cursor-not-allowed
    "
          >
            <SendHorizontal size={18} />
            {loading ? "جاري البحث..." : "إرسال"}
          </button>
        </div>

        {answer && (
          <div
            dir="rtl"
            className="
              bg-muted
              rounded-xl
              p-4
              border
              border-border
            "
          >
            <h2 className="font-semibold mb-2">الإجابة</h2>

            <p className="leading-7 whitespace-pre-wrap">{answer}</p>
          </div>
        )}
      </div>
    </div>
  );
}
