"use client";


import Chat from "./chat/Chat";
import SideBarComponent from "./components/SideBarComponent";
import Upload from "./upload/UploadFile";

export default function Home() {
  return (
    <main className="min-h-screen bg-background text-foreground p-8 dark  ">
      <h1 className="text-3xl font-bold text-center mb-3">
        Arabic RAG System
      </h1>
      <div className="bg-card text-card-foreground border border-border rounded-xl p-6">
        <Upload />
        <h1 className="font-semibold text-center mt-4 text-2xl">
          ماذا تريد ان تسأل عن الملف؟
        </h1>
        <Chat />
        <SideBarComponent />
      </div>
    </main>
  );
}
