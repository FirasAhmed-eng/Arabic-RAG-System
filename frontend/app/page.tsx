"use client";

import Chat from "./chat/Chat";
import Upload from "./upload/Upload";

export default function Home() {
  return (
    <main>
      <h1>Hello</h1>
      <Upload />
      <Chat />
    </main>
  );
}
