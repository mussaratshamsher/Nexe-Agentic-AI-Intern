"use client";
import Link from "next/link";
import { FloatingTabs } from "@/components/shared/FloatingTabs";

export default function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 md:p-8 space-y-8 md:space-y-12 bg-background text-foreground text-center">
      <h1 className="text-4xl md:text-6xl font-extralight tracking-tight text-white leading-tight">
        AI Business{" "}
        <span className="block md:inline mt-2 md:mt-0 relative md:ml-4 px-4 py-1 rounded-lg border-animate glow-blue text-white font-semibold">
          Operations
        </span>
      </h1>
      <p className="text-lg md:text-xl text-muted-foreground max-w-2xl font-light">
        Transform your business with our multi-agent AI workspace. Automate workflows, manage CRM data, and track agent execution in real-time.
      </p>
      
      <div className="flex flex-col md:flex-row gap-4 w-full justify-center md:w-auto">
        <div className="btn-wrap">
          <Link href="/dashboard" className="cyber-btn w-full md:w-auto text-center">
            Launch Command Center
          </Link>
        </div>
        <Link href="/auth/register" className="glow-blue flex items-center justify-center gap-2 px-10 py-3 bg-secondary text-secondary-foreground rounded-full hover:opacity-90 transition font-semibold w-full md:w-auto">
          Sign Up / Login
        </Link>
      </div>

      <FloatingTabs />
    </div>
  );
}
