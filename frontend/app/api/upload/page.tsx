"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("");

  async function fetchData() {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/health`);

      const data = await res.json();
      setMessage(data.message);
    } catch (error) {
      console.error("Failed to fetch:", error);
    }
  }

  fetchData();

  return (
    <div>
      <h1>{message}</h1>
    </div>
  );
}
