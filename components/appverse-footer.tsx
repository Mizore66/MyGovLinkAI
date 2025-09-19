"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Instagram, Twitter, Youtube, MessageCircle } from "lucide-react";
import Image from "next/image";

interface FooterContent {
  tagline: string;
  copyright: string;
}

const defaultContent: FooterContent = {
  tagline:
    "Experience 3D animation like never before. We craft cinematic visuals for brands and products.",
  copyright: "© 2025 — GovLink",
};

export function AppverseFooter() {
  const [content, setContent] = useState<FooterContent>(defaultContent);

  useEffect(() => {
    // Load content from localStorage
    const savedContent = localStorage.getItem("GovLink-content");
    if (savedContent) {
      try {
        const parsed = JSON.parse(savedContent);
        if (parsed.footer) {
          setContent(parsed.footer);
        }
      } catch (error) {
        console.error("Error parsing saved content:", error);
      }
    }
  }, []);

  return (
    <section className="text-white">
      {/* Contact CTA */}
      {/* <div className="container mx-auto px-4 pt-12 sm:pt-16">
        <div className="flex justify-center">
          <Button
            asChild
            className="rounded-full bg-cyan-400 px-6 py-2 text-sm font-medium text-black shadow-[0_0_20px_rgba(163,230,53,0.35)] hover:bg-cyan-300"
          >
            <a href="https://wa.link/rc25na" target="_blank" rel="noopener noreferrer">
              Contact us
            </a>
          </Button>
        </div>
      </div> */}

      {/* Download the app */}
      <div className="container mx-auto px-4 py-12 sm:py-16 space-y-8">
        {/* First Card - Phone on left, text on right */}
        <Card className="relative overflow-hidden rounded-3xl liquid-glass p-6 sm:p-10">
          <div className="relative grid items-center gap-8 md:grid-cols-2">
            {/* Left mockup */}
            <div className="mx-auto w-full max-w-[320px]">
              <div className="relative rounded-[28px] liquid-glass p-2 shadow-2xl">
                <div className="relative aspect-[9/19] w-full overflow-hidden rounded-2xl bg-black">
                  <Image
                    src="/images/top-rated-1.png"
                    alt="placeholder"
                    fill
                    className="object-cover"
                  />
                  <div className="relative p-3">
                    <div className="mx-auto mb-3 h-1.5 w-16 rounded-full bg-white/20" />
                    <div className="space-y-1 px-1">
                      <div className="text-3xl font-extrabold text-cyan-300">Tax History</div>
                      <p className="text-xs text-white/80">
                        View past tax payments instantly via WhatsApp
                      </p>
                      <div className="mt-3 inline-flex items-center rounded-full bg-black/40 px-2 py-0.5 text-[10px] uppercase tracking-wider text-cyan-300">
                        govlink app
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Right copy */}
            <div>
              <p className="mb-2 text-[11px] tracking-widest text-cyan-300">TAX PAYMENT HISTORY</p>
              <h3 className="text-2xl font-bold leading-tight text-white sm:text-3xl">
                Access your complete tax payment records instantly
              </h3>
              <p className="mt-2 max-w-prose text-sm text-neutral-400">
                View your entire tax payment history, download receipts, and check compliance
                status. Our AI will guide you to the official tax portal when needed for detailed
                records or corrections.
              </p>
            </div>
          </div>
        </Card>

        {/* Second Card - Phone on right, text on left (right-aligned) */}
        <Card className="relative overflow-hidden rounded-3xl liquid-glass p-6 sm:p-10">
          <div className="relative grid items-center gap-8 md:grid-cols-2">
            {/* Left copy (right-aligned) */}
            <div className="text-right">
              <p className="mb-2 text-[11px] tracking-widest text-cyan-300">COURT SUMMONS CHECK</p>
              <h3 className="text-2xl font-bold leading-tight text-white sm:text-3xl">
                Check for any pending court summons or legal notices
              </h3>
              <p className="mt-2 max-w-prose text-sm text-neutral-400 ml-auto">
                Stay informed about any court summons, legal notices, or pending cases. Our AI will
                provide direct links to the official court systems when action is required.
              </p>
            </div>

            {/* Right mockup */}
            <div className="mx-auto w-full max-w-[320px]">
              <div className="relative rounded-[28px] liquid-glass p-2 shadow-2xl">
                <div className="relative aspect-[9/19] w-full overflow-hidden rounded-2xl bg-black">
                  <Image
                    src="/images/top-rated-1.png"
                    alt="placeholder"
                    fill
                    className="object-cover"
                  />
                  <div className="relative p-3">
                    <div className="mx-auto mb-3 h-1.5 w-16 rounded-full bg-white/20" />
                    <div className="space-y-1 px-1">
                      <div className="text-3xl font-extrabold text-cyan-300">Court Summons</div>
                      <p className="text-xs text-white/80">Check legal notices and summons</p>
                      <div className="mt-3 inline-flex items-center rounded-full bg-black/40 px-2 py-0.5 text-[10px] uppercase tracking-wider text-cyan-300">
                        govlink app
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Card>

        {/* Third Card - Phone on left, text on right */}
        <Card className="relative overflow-hidden rounded-3xl liquid-glass p-6 sm:p-10">
          <div className="relative grid items-center gap-8 md:grid-cols-2">
            {/* Left mockup */}
            <div className="mx-auto w-full max-w-[320px]">
              <div className="relative rounded-[28px] liquid-glass p-2 shadow-2xl">
                <div className="relative aspect-[9/19] w-full overflow-hidden rounded-2xl bg-black">
                  <Image
                    src="/images/top-rated-1.png"
                    alt="placeholder"
                    fill
                    className="object-cover"
                  />
                  <div className="relative p-3">
                    <div className="mx-auto mb-3 h-1.5 w-16 rounded-full bg-white/20" />
                    <div className="space-y-1 px-1">
                      <div className="text-3xl font-extrabold text-cyan-300">License Expiry</div>
                      <p className="text-xs text-white/80">Check all license expiration dates</p>
                      <div className="mt-3 inline-flex items-center rounded-full bg-black/40 px-2 py-0.5 text-[10px] uppercase tracking-wider text-cyan-300">
                        govlink app
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Right copy */}
            <div>
              <p className="mb-2 text-[11px] tracking-widest text-cyan-300">
                LICENSE EXPIRY ALERTS
              </p>
              <h3 className="text-2xl font-bold leading-tight text-white sm:text-3xl">
                Track all your license expiration dates in one place
              </h3>
              <p className="mt-2 max-w-prose text-sm text-neutral-400">
                Monitor driving licenses, professional licenses, permits, and certifications. Get
                timely reminders and direct links to official renewal portals when it's time to
                renew.
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Footer */}
      <footer className="border-t border-white/10 pb-20 md:pb-10">
        <div className="container mx-auto px-4 py-10">
          <div className="grid gap-8 md:grid-cols-[1.2fr_1fr_1fr]">
            {/* Brand */}
            <div className="space-y-3">
              <div className="flex items-center gap-1.5">
                <Image
                  src="/icons/govlink-logo.png"
                  alt="GovLink logo"
                  width={24}
                  height={24}
                  className="h-6 w-6"
                />
                <span className="text-xl font-semibold text-cyan-300">GovLink</span>
              </div>
              <p className="max-w-sm text-sm text-neutral-400">{content.tagline}</p>
            </div>

            {/* Navigation */}
            <div className="grid grid-cols-2 gap-6 sm:grid-cols-3 md:grid-cols-2">
              <div>
                <h5 className="mb-2 text-xs font-semibold uppercase tracking-widest text-neutral-400">
                  Navigation
                </h5>
                <ul className="space-y-2 text-sm text-neutral-300">
                  {["Home", "Features", "Testimonials", "Pricing", "Blog", "Download"].map(
                    (item) => (
                      <li key={item}>
                        <Link href={`#${item.toLowerCase()}`} className="hover:text-cyan-300">
                          {item}
                        </Link>
                      </li>
                    )
                  )}
                </ul>
              </div>
              <div>
                <h5 className="mb-2 text-xs font-semibold uppercase tracking-widest text-neutral-400">
                  Social media
                </h5>
                <ul className="space-y-2 text-sm text-neutral-300">
                  <li className="flex items-center gap-2">
                    <Twitter className="h-4 w-4 text-neutral-400" />
                    <a
                      href="https://twitter.com/theGovLink"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-cyan-300"
                      aria-label="Follow GovLink on Twitter"
                    >
                      X/Twitter
                    </a>
                  </li>
                  <li className="flex items-center gap-2">
                    <Youtube className="h-4 w-4 text-neutral-400" />
                    <a
                      href="https://www.youtube.com/@GovLinkinternational"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-cyan-300"
                      aria-label="Subscribe to GovLink on YouTube"
                    >
                      YouTube
                    </a>
                  </li>
                  <li className="flex items-center gap-2">
                    <Instagram className="h-4 w-4 text-neutral-400" />
                    <a
                      href="https://instagram.com/theGovLink"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-cyan-300"
                      aria-label="Follow GovLink on Instagram"
                    >
                      Instagram
                    </a>
                  </li>
                  <li className="flex items-center gap-2">
                    <MessageCircle className="h-4 w-4 text-neutral-400" />
                    <a
                      href="https://threads.com/theGovLink"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:text-cyan-300"
                      aria-label="Follow GovLink on Threads"
                    >
                      Threads
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Bottom bar */}
          <div className="mt-8 flex flex-col items-center justify-between gap-4 border-t border-white/10 pt-6 text-xs text-neutral-500 sm:flex-row">
            <p>{content.copyright}</p>
            <div className="flex items-center gap-6">
              <Link href="/revisions" className="hover:text-cyan-300">
                Revision Policy
              </Link>
              <Link href="/t&c" className="hover:text-cyan-300">
                Terms & Conditions
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </section>
  );
}
