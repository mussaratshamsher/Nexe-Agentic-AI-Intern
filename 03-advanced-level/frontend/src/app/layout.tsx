import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Toaster } from "@/components/ui/sonner";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AI CRM Digital Factory | Automated Business Workflow Solutions",
  description: "Transform your business with our AI-powered CRM Digital Factory. Automated lead qualification, project management, and customer support workflows for modern enterprises.",
  keywords: [
    "AI CRM",
    "Business Automation",
    "Digital Factory",
    "Workflow Optimization",
    "Lead Qualification",
    "Project Logistics",
    "Customer Support AI",
    "Agentic Workflows"
  ],
  authors: [{ name: "Hackathon Team" }],
  icons: {
    icon: "/fte.jpg",
  },
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className="h-full antialiased"
      suppressHydrationWarning
    >
      <body className={`${geistSans.variable} ${geistMono.variable} min-h-full flex flex-col`}>
        {children}
        <Toaster />
      </body>
    </html>
  );
}
