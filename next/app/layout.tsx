// next/app/layout.tsx
import "../styles/global.css";
import Navbar from "@/components/Navbar";

export const metadata = {
  title: "AIDPA - Smart Personal Assistant",
  description: "Voice + AI-powered task/health/finance assistant",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-800">
        <Navbar />
        <main className="max-w-5xl mx-auto p-4">{children}</main>
      </body>
    </html>
  );
}
