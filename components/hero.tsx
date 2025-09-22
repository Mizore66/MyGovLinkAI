import { Button } from "@/components/ui/button";
import Image from "next/image";
import { FaDiscord, FaTelegramPlane } from "react-icons/fa";

export function Hero() {
  return (
    <section className="relative isolate overflow-hidden mt-20">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-center py-14 sm:py-20 gap-16">
          {/* Left side - Hero text */}
          <div className="flex-1 max-w-[70%] text-right">
            <div className="mb-5 flex items-center justify-end gap-2">
              <Image
                src="/icons/govlink-logo.png"
                alt="govlink logo"
                width={32}
                height={32}
                className="h-8 w-8"
              />
              <p className="text-sm uppercase tracking-[0.25em] text-cyan-300/80">GovLink</p>
            </div>
            <h1 className="mt-3 text-right text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl">
              <span className="block">GOVERNMENT SERVICES</span>
              <span className="block">
                MADE{" "}
                <span className="text-cyan-300 drop-shadow-[0_0_20px_rgba(132,204,22,0.35)]">
                  SIMPLE{" "}
                </span>
                WITH AI
              </span>
            </h1>
            <div className="mt-6 flex flex-col items-end gap-3">
              <p className="text-md font-extrabold text-white">Try It Now On</p>
              <div className="flex gap-3">
                <Button asChild className="rounded-full bg-[#5865F2] text-white hover:bg-[#4752C4]">
                  <a
                    href="https://discord.com/oauth2/authorize?client_id=1418806394634633254"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <FaDiscord className="inline" size={20} />
                    <span className="font-bold tracking-wide">Discord</span>
                  </a>
                </Button>
                <Button
                  asChild
                  className="rounded-full bg-[#0088cc] px-6 text-white hover:bg-[#006699]"
                >
                  <a href="https://t.me/MyGovLinkBot" target="_blank" rel="noopener noreferrer">
                    <FaTelegramPlane className="inline" size={20} />
                    <span className="font-bold tracking-wide">Telegram</span>
                  </a>
                </Button>
              </div>
            </div>
          </div>

          {/* Right side - Phone */}
          <div className="flex-shrink-0">
            <div className="w-64">
              <PhoneCard title={""} sub={""} tone={""} gradient={phoneData[0].gradient} />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function PhoneCard({
  title = "8°",
  sub = "Clear night. Great for render farm runs.",
  tone = "calm",
  gradient = "from-[#0f172a] via-[#14532d] to-[#052e16]",
}: {
  title?: string;
  sub?: string;
  tone?: string;
  gradient?: string;
}) {
  return (
    <div className="relative rounded-[28px] glass-border bg-neutral-900 p-2">
      <div className="relative aspect-[9/19] w-full overflow-hidden rounded-2xl bg-black">
        <Image src="/images/discord-light.png" alt="placeholder" fill className="object-cover" />

        <div className="relative z-10 p-3">
          <div className="mx-auto mb-3 h-1.5 w-16 rounded-full bg-white/20" />
          <div className="space-y-1 px-1">
            <div className="text-3xl font-bold leading-snug text-white/90">{title}</div>
            <p className="text-xs text-white/70">{sub}</p>
            <div className="mt-3 inline-flex items-center rounded-full bg-black/40 px-2 py-0.5 text-[10px] uppercase tracking-wider text-cyan-300">
              {tone === "calm" ? "govlink app" : tone}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const phoneData = [
  {
    gradient: "from-[#0b0b0b] via-[#0f172a] to-[#020617]",
  },
];
