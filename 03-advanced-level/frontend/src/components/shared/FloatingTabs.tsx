"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { MessageSquare, Briefcase } from "lucide-react";

export const FloatingTabs = () => {
  const router = useRouter();
  const [hoveredTab, setHoveredTab] = useState<string | null>(null);

  const tabs = [
    {
      id: "projects",
      label: "Our Projects",
      icon: Briefcase,
      color: "bg-primary/20 hover:bg-primary/30 text-primary border-primary/50",
      glow: "glow-blue",
      onClick: () => router.push("/contact#projects"),
    },
    {
      id: "contact",
      label: "Contact Us",
      icon: MessageSquare,
      color: "bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-400 border-emerald-500/50",
      glow: "glow-green",
      onClick: () => router.push("/contact"),
    },
  ];

  return (
    <div className="fixed bottom-8 right-8 flex flex-col gap-6 z-50">
      {tabs.map((tab) => (
        <div key={tab.id} className="relative flex items-center justify-end">
          <AnimatePresence>
            {hoveredTab === tab.id && (
              <motion.span
                initial={{ opacity: 0, x: 20, scale: 0.8 }}
                animate={{ opacity: 1, x: 0, scale: 1 }}
                exit={{ opacity: 0, x: 10, scale: 0.8 }}
                transition={{ type: "spring", stiffness: 400, damping: 25 }}
                className="absolute right-full mr-4 px-4 py-2 rounded-xl bg-card/90 backdrop-blur-xl border border-white/10 text-white text-[10px] font-black uppercase tracking-[0.2em] whitespace-nowrap shadow-2xl pointer-events-none italic"
              >
                {tab.label}
              </motion.span>
            )}
          </AnimatePresence>

          <motion.button
            whileHover={{ scale: 1.1, rotate: 5 }}
            whileTap={{ scale: 0.9, rotate: -5 }}
            onHoverStart={() => setHoveredTab(tab.id)}
            onHoverEnd={() => setHoveredTab(null)}
            onClick={tab.onClick}
            className={`
              w-16 h-16 rounded-2xl border-2 flex items-center justify-center shadow-2xl 
              backdrop-blur-md transition-all duration-300
              ${tab.color} ${tab.glow}
            `}
          >
            <tab.icon size={28} className="drop-shadow-[0_0_8px_currentColor]" />
          </motion.button>
        </div>
      ))}
    </div>
  );
};
