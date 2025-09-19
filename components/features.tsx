"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BsFillLightningFill } from "react-icons/bs";
import { RxCross2 } from "react-icons/rx";
import { IoLanguageOutline } from "react-icons/io5";

interface FeaturesContent {
  title: string;
  subtitle: string;
}

const defaultContent: FeaturesContent = {
  title: "What makes us the best service for you.",
  subtitle: "Discover our unique approach to 3D animation",
};

export function Features() {
  const [content, setContent] = useState<FeaturesContent>(defaultContent);

  useEffect(() => {
    // Load content from localStorage
    const savedContent = localStorage.getItem("skitbit-content");
    if (savedContent) {
      try {
        const parsed = JSON.parse(savedContent);
        if (parsed.features) {
          setContent(parsed.features);
        }
      } catch (error) {
        console.error("Error parsing saved content:", error);
      }
    }
  }, []);

  return (
    <section id="features" className="container mx-auto px-4 py-16 sm:py-20 mt-32">
      <h2 className="mb-8 text-center text-4xl font-extrabold tracking-tight text-white sm:text-5xl">
        {content.title}
      </h2>

      <div className="grid gap-6 md:grid-cols-3">
        <Card className="hidden md:block liquid-glass border border-white/10 bg-white/5 backdrop-blur-xl">
          <div className="flex justify-center items-center mt-16">
            <BsFillLightningFill color="#FFFFFF" size={196} />
          </div>
          <CardHeader className="mt-12">
            <p className="text-[11px] tracking-widest text-neutral-400">INSTANT UPDATES</p>
            <CardTitle className="mt-1 text-xl text-white">
              Get instant updates on your status without the wait.
            </CardTitle>
          </CardHeader>
        </Card>

        <Card className="hidden md:block liquid-glass border border-white/10 bg-white/5 backdrop-blur-xl">
          <div className="flex justify-center items-center mt-16">
            <RxCross2 color="#FFFFFF" size={196} />
          </div>
          <CardHeader className="mt-12">
            <p className="text-[11px] tracking-widest text-neutral-400">NO MORE BOOKMARKS</p>
            <CardTitle className="mt-1 text-xl text-white">
              Our AI Assistant will guide you to the right government service portal.
            </CardTitle>
          </CardHeader>
        </Card>

        <Card className="block liquid-glass border border-white/10 bg-white/5 backdrop-blur-xl">
          <div className="flex justify-center items-center mt-16">
            <IoLanguageOutline color="#FFFFFF" size={196} />
          </div>
          <CardHeader className="mt-12">
            <p className="text-[11px] tracking-widest text-neutral-400">AI-POWERED SIMPLICITY</p>
            <CardTitle className="mt-1 text-xl text-semibold text-white">
              Ask in plain language and get clear answers.
            </CardTitle>
          </CardHeader>
        </Card>
      </div>
    </section>
  );
}
