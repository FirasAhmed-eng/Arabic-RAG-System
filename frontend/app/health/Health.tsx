"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("Loading...");

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/health`,
        );

        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }

        const data = await res.json();

        setMessage(data.status);
      } catch (error) {
        console.error(error);
        setMessage("Failed to connect to backend");
      }
    }

    fetchData();
  }, []);

  return (
    <main>
      <h1>Backend Status</h1>
      <p>{message}</p>
    </main>
  );
}
console.log("API URL =", process.env.NEXT_PUBLIC_API_URL);