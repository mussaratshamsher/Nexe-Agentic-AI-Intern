"use client";

import React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { ChevronLeft, Mail, MessageSquare, Briefcase } from "lucide-react";
import { ContactForm } from "@/components/shared/ContactForm";
import { ProjectsList } from "@/components/shared/ProjectsList";

export default function ContactPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Navigation */}
      <nav className="p-6 border-b border-white/5">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 text-muted-foreground hover:text-white transition-colors group">
            <ChevronLeft size={20} className="group-hover:-translate-x-1 transition-transform" />
            <span>Back to Home</span>
          </Link>
          <div className="text-xl font-bold tracking-tighter">
            AI Business <span className="text-primary">Ops</span>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-12 md:py-20 space-y-24">
        {/* Contact Section */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
          <div className="space-y-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-4"
            >
              <h1 className="text-5xl md:text-7xl font-black tracking-tighter uppercase italic">
                Get In <span className="text-primary">Touch</span>
              </h1>
              <p className="text-xl text-muted-foreground leading-relaxed">
                Ready to transform your business with autonomous AI agents? Send us a message and our orchestrator will analyze your needs.
              </p>
            </motion.div>

            <div className="space-y-6">
              <div className="flex items-center gap-4 p-4 rounded-2xl bg-secondary/30 border border-white/5">
                <div className="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center text-primary">
                  <Mail size={24} />
                </div>
                <div>
                  <h3 className="font-bold">Email Us</h3>
                  <p className="text-muted-foreground text-sm">contact@fte-factory.com</p>
                </div>
              </div>
              <div className="flex items-center gap-4 p-4 rounded-2xl bg-secondary/30 border border-white/5">
                <div className="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center text-blue-500">
                  <MessageSquare size={24} />
                </div>
                <div>
                  <h3 className="font-bold">Chat Support</h3>
                  <p className="text-muted-foreground text-sm">Available 24/7 via AI agents</p>
                </div>
              </div>
            </div>
          </div>

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-card/50 backdrop-blur-xl border border-white/10 p-8 md:p-10 rounded-[2.5rem] shadow-2xl shadow-primary/5"
          >
            <ContactForm onSuccess={() => {}} />
          </motion.div>
        </section>

        {/* Projects Showcase Section */}
        <section className="space-y-12 pb-20" id="projects">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 border-b border-white/5 pb-8">
            <div className="space-y-2">
              <div className="inline-flex items-center gap-2 text-primary font-bold text-xs uppercase tracking-widest">
                <Briefcase size={14} />
                Showcase
              </div>
              <h2 className="text-4xl md:text-5xl font-black tracking-tighter uppercase italic">
                Our Featured <span className="text-primary">Projects</span>
              </h2>
            </div>
            <p className="text-muted-foreground max-w-md text-sm md:text-right">
              Explore the autonomous solutions we&apos;ve built to solve complex business challenges using multi-agent orchestration.
            </p>
          </div>

          <ProjectsList />
        </section>
      </main>

      {/* Footer */}
      <footer className="py-12 border-t border-white/5 text-center text-muted-foreground text-sm">
        <p>© 2026 AI Business Operations Manager. All rights reserved.</p>
      </footer>
    </div>
  );
}
