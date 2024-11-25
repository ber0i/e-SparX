import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Header from "../components/Header";
import "./globals.css";

const inter = Inter({ weight: "400", subsets: ["latin"] });

export const metadata: Metadata = {
  title: " e-SparX | The Space for Artifact Exchange in ML Research",
  description: "Share your ML model pipelines and accelerate your ML research.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Header />
        <div className="pt-4">{children}</div>
      </body>
    </html>
  );
}
