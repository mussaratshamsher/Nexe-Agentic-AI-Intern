"use client";
import { ProjectCard } from "@/components/dashboard/ProjectCard";

const projects = [
  {
    title: "AI Employee (Advanced)",
    techStack: "Next.js / AI Agents",
    features: ["Autonomous Task Execution", "Complex Workflow Orchestration"],
    href: "https://ai-employee.vercel.app/"
  },
  {
    title: "Humanoid Robotics Book",
    techStack: "Next.js / Tailwind",
    features: ["Interactive learning", "3D visualizations"],
    href: "https://humanoid-robotics-book-sepia.vercel.app/"
  },
  {
    title: "AI Calculator & Agent",
    techStack: "Streamlit / Python",
    features: ["Agentic computation", "Real-time analysis"],
    href: "https://ai-agent-and-calculate.streamlit.app/"
  }
];

export default function ProjectsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-foreground">AI Projects</h1>
        <p className="text-muted-foreground mt-2">Explore my latest AI-driven projects and experiments.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {projects.map((project, index) => (
          <ProjectCard key={index} {...project} />
        ))}
      </div>
    </div>
  );
}
