import Link from 'next/link';
import { FeatureCard } from '@/components/FeatureCard';
import { CodeBlock } from '@/components/CodeBlock';
import { Zap, Smartphone, Music, Terminal, Cpu, Eye, ArrowRight, Download, Github } from '@/components/Icons';

export const metadata = {
  title: 'Tux Droid Software - Control Your Linux Penguin Robot | TuxDroid',
  description: 'Tux Droid software & controller. Download ScayTux to control your Tux Droid robot on Windows & Linux. 100 combos, Telegram, TTS. Official TuxDroid software.',
  openGraph: {
    title: 'Tux Droid Software - Control Your Penguin Robot | TuxDroid',
    description: 'Official Tux Droid controller software. ScayTux for Windows & Linux.',
  },
};

const features = [
  { icon: <Zap className="w-5 h-5" />, title: 'Cross-Platform', description: 'Single codebase runs on Windows 10/11 and Linux (Ubuntu/Debian). One JAR to rule them all.' },
  { icon: <Smartphone className="w-5 h-5" />, title: 'Telegram Remote', description: 'Control your Tux Droid from anywhere in the world via an inline-keyboard Telegram Bot.' },
  { icon: <Eye className="w-5 h-5" />, title: '100 Combos', description: 'Pre-programmed cinematic animations from "Royal Entrance" to "DJ Mode" with synchronized movements.' },
  { icon: <Music className="w-5 h-5" />, title: 'Music & Dance', description: 'Play MP3s through Tux with synchronized dancing. Michael Jackson, Chicken Dance, and more!' },
  { icon: <Terminal className="w-5 h-5" />, title: 'Interactive CLI', description: 'Beautiful ANSI-colored menu system. Interactive mode, REPL mode, or classic CLI arguments.' },
  { icon: <Cpu className="w-5 h-5" />, title: 'Full Motor Control', description: 'Eyes, Mouth, Wings, Spin, LED - smooth animations with thread-safe USB HID communication.' },
];

const steps = [
  { num: '01', title: 'Clone & Build', desc: 'Clone the repo and run the launcher script. Maven, dependencies - everything installs automatically.', color: 'text-tux-orange' },
  { num: '02', title: 'Plug In', desc: 'Connect the Tux Droid USB dongle. On Linux, udev rules are auto-configured.', color: 'text-tux-blue' },
  { num: '03', title: 'Control', desc: 'Use the interactive CLI, command line, or set up Telegram for remote control from your phone.', color: 'text-tux-orange' },
];

const combos = [
  { id: 1, name: 'Royal Entrance', desc: '"I have arrived." Slow eye open, blue light.' },
  { id: 5, name: 'Hacker Alert', desc: 'Emergency red strobe and panic spin.' },
  { id: 6, name: 'Police Mode', desc: 'Red/Blue siren + 360 spin x3.' },
  { id: 14, name: 'Celebration', desc: '"Woo hoo!" with fast flaps.' },
  { id: 30, name: 'Mafia Don', desc: '"You come to me..." Deep voice.' },
  { id: 49, name: 'DJ Mode', desc: '"Drop the beat!" Club lights.' },
];

export default function Home() {
  return (
    <div className="hero-glow">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center pt-16 overflow-hidden">
        <div className="relative z-10 max-w-5xl mx-auto px-4 text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2.5 px-5 py-2 rounded-full bg-tux-card border border-tux-border text-sm mb-10">
            <span className="dot-orange animate-pulse" />
            <span className="text-tux-muted">ScayTux v3.0</span>
            <span className="text-tux-subtle">&mdash;</span>
            <span className="text-tux-orange font-medium">Now with Telegram Remote</span>
          </div>

          {/* Heading */}
          <h1 className="text-5xl sm:text-7xl lg:text-[5.5rem] font-black tracking-tight mb-7 leading-[0.95] text-balance">
            <span className="text-white">Bring Your </span>
            <span className="gradient-text">Tux Droid</span>
            <br />
            <span className="text-white">Back to Life</span>
          </h1>

          {/* Subheading - SEO: tux, tux droid, tux droid software */}
          <p className="text-base sm:text-lg text-tux-muted max-w-2xl mx-auto mb-10 leading-relaxed">
            The official <strong className="text-white/80">Tux Droid software</strong> and controller for the classic Linux penguin robot.
            Cross-platform Tux Droid controller with 100 combos, Telegram bot,
            TTS, and a beautiful interactive CLI.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Link href="/getting-started" className="btn-primary flex items-center gap-2.5">
              Get Started <ArrowRight className="w-4 h-4" />
            </Link>
            <Link href="/download" className="btn-secondary flex items-center gap-2.5">
              <Download className="w-4 h-4 text-tux-subtle" /> Download
            </Link>
          </div>

          {/* Code Preview */}
          <div className="max-w-xl mx-auto">
            <CodeBlock
              code={`git clone https://github.com/Scayar/ScayTux
cd ScayTux
java -jar target/ScayTux.jar`}
              lang="bash"
            />
          </div>
        </div>

        <div className="absolute bottom-0 left-0 right-0 h-40 bg-gradient-to-t from-tux-black to-transparent pointer-events-none" />
      </section>

      {/* Features Grid */}
      <section className="py-28 px-4 relative">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <p className="text-xs font-semibold text-tux-orange uppercase tracking-[0.2em] mb-3">Features</p>
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">Everything You Need</h2>
            <p className="text-tux-muted max-w-lg mx-auto text-sm">
              A complete toolkit to control, animate, and breathe new life into your Tux Droid.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {features.map((f) => (
              <FeatureCard key={f.title} {...f} />
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-28 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <p className="text-xs font-semibold text-tux-blue uppercase tracking-[0.2em] mb-3">Setup</p>
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">Up &amp; Running in 3 Steps</h2>
            <p className="text-tux-muted text-sm">From zero to dancing penguin in under 5 minutes.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {steps.map((step) => (
              <div key={step.num} className="relative">
                <span className={`text-7xl font-black absolute -top-6 -left-1 ${step.color} opacity-[0.07]`}>{step.num}</span>
                <div className="card p-7 pt-12 relative">
                  <span className={`text-xs font-bold ${step.color} font-mono`}>STEP {step.num}</span>
                  <h3 className="text-lg font-bold text-white mt-2 mb-2">{step.title}</h3>
                  <p className="text-sm text-tux-subtle leading-relaxed">{step.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Combos Preview */}
      <section className="py-28 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <p className="text-xs font-semibold text-tux-orange uppercase tracking-[0.2em] mb-3">Animations</p>
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">100 Cinematic Combos</h2>
            <p className="text-tux-muted max-w-lg mx-auto text-sm">
              Pre-programmed animation sequences with synchronized eyes, mouth, wings, spin, LED, and TTS.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {combos.map((c) => (
              <div key={c.id} className="card p-5 group">
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-[11px] font-mono font-bold text-tux-orange bg-tux-orange/10 px-2.5 py-1 rounded-md">#{c.id}</span>
                  <h3 className="text-white font-semibold text-sm">{c.name}</h3>
                </div>
                <p className="text-xs text-tux-subtle leading-relaxed">{c.desc}</p>
              </div>
            ))}
          </div>

          <div className="text-center mt-10">
            <Link href="/docs/combos" className="text-tux-orange hover:text-tux-orange-light text-sm font-medium transition-colors">
              View all 100 combos &rarr;
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-28 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <div className="card p-14 glow-border relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-tux-orange/[0.03] to-tux-blue/[0.02] pointer-events-none" />
            <div className="relative z-10">
              <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">Ready to Resurrect Your Penguin?</h2>
              <p className="text-tux-muted mb-10 max-w-md mx-auto text-sm leading-relaxed">
                ScayTux is free, open-source, and built with love. Download it now and bring your Tux Droid back to life!
              </p>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Link href="/download" className="btn-primary">
                  Download ScayTux
                </Link>
                <a
                  href="https://github.com/Scayar/ScayTux"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-secondary flex items-center gap-2"
                >
                  <Github className="w-4 h-4" /> View on GitHub
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
