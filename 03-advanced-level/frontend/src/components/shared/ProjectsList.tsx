"use client";

import React from "react";
import { motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Globe, Code, Layers, Zap } from "lucide-react";

const projects = [
  {
    title: "AI Employee (Advanced)",
    description: "An advanced agentic AI employee capable of handling complex business operations, multi-step workflows, and autonomous decision-making.",
    tech: ["Next.js", "AI Agents", "Agentic Workflows", "GROQ API"],
    features: [
      "Autonomous Task Execution",
      "Complex Workflow Orchestration",
      "Real-time Decision Making",
      "Advanced Tool Integration"
    ],
    demo: "https://ai-employee.vercel.app/",
    code: "https://github.com/mussaratshamsher/Nexe-Agentic-AI-Intern/tree/master/03-advanced-level",
    color: "from-purple-500/20 to-indigo-500/20",
    border: "border-purple-500/50"
  },
  {
    title: "Humanoid Robotics Book (Intermediate)",
    description: "An interactive digital textbook about Physical AI and Humanoid Robotics, featuring interactive learning modules and technical deep-dives.",
    tech: ["Next.js", "Tailwind CSS", "Interactive UI", "Physical AI"],
    features: [
      "Interactive Learning Modules",
      "Robotics Fundamentals",
      "AI & Control Systems",
      "Responsive Digital Experience"
    ],
    demo: "https://humanoid-robotics-book-sepia.vercel.app/",
    code: "https://github.com/mussaratshamsher/Nexe-Agentic-AI-Intern/tree/master/02-Intermediate-level",
    color: "from-blue-500/20 to-cyan-500/20",
    border: "border-blue-500/50"
  },
  {
    title: "AI Agent & Calculator (Beginner)",
    description: "A foundational project showcasing agentic computation and real-time analysis through an intelligent calculator interface.",
    tech: ["Streamlit", "Python", "LLMs", "Data Analysis"],
    features: [
      "Agentic Computation",
      "Real-time Data Processing",
      "Natural Language Interface",
      "Mathematical Reasoning"
    ],
    demo: "https://ai-agent-and-calculate.streamlit.app/",
    code: "https://github.com/mussaratshamsher/Nexe-Agentic-AI-Intern/tree/master/01-beginner-level",
    color: "from-emerald-500/20 to-teal-500/20",
    border: "border-emerald-500/50"
  }
];

export function ProjectsList() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-2">
      {projects.map((project, index) => (
        <motion.div
          key={project.title}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          whileHover={{ y: -5 }}
          className="h-full"
        >
          <Card className={`h-full flex flex-col overflow-hidden border-2 bg-gradient-to-br ${project.color} ${project.border} backdrop-blur-sm`}>
            <CardHeader>
              <div className="flex justify-between items-start mb-2">
                <div className="p-2 rounded-lg bg-background/50">
                  <Layers className="w-5 h-5 text-primary" />
                </div>
                <Badge variant="outline" className="bg-background/50">Featured</Badge>
              </div>
              <CardTitle className="text-xl font-bold">{project.title}</CardTitle>
              <CardDescription className="text-foreground/80 line-clamp-3">
                {project.description}
              </CardDescription>
            </CardHeader>
            <CardContent className="flex-grow">
              <div className="mb-4">
                <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2 flex items-center gap-1">
                  <Zap className="w-3 h-3" /> Key Features
                </h4>
                <ul className="space-y-1">
                  {project.features.map(feature => (
                    <li key={feature} className="text-sm flex items-start gap-2">
                      <span className="mt-1.5 w-1 h-1 rounded-full bg-primary shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Tech Stack</h4>
                <div className="flex flex-wrap gap-2">
                  {project.tech.map(t => (
                    <Badge key={t} variant="secondary" className="text-[10px] px-2 py-0">
                      {t}
                    </Badge>
                  ))}
                </div>
              </div>
            </CardContent>
            <CardFooter className="pt-4 border-t bg-background/30 flex justify-between">
              <a 
                href={project.demo} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-xs flex items-center gap-1 hover:text-primary transition-colors"
              >
                <Globe className="w-3 h-3" /> Live Demo
              </a>
              <a 
                href={project.code} 
                target="_blank" 
                rel="noopener noreferrer" 
                className="text-xs flex items-center gap-1 hover:text-primary transition-colors"
              >
                <Code className="w-3 h-3" /> View Code
              </a>
            </CardFooter>
          </Card>
        </motion.div>
      ))}
    </div>
  );
}
