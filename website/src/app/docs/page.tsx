import Link from 'next/link';
import { Terminal, Smartphone, Music, Eye, Cpu } from '@/components/Icons';

export const metadata = {
  title: 'Documentation - TuxDroid',
  description: 'Complete documentation for ScayTux - The Ultimate Tux Droid Controller.',
};

const sections = [
  {
    href: '/docs/commands',
    icon: <Terminal className="w-6 h-6" />,
    title: 'Command Reference',
    desc: 'All CLI flags, options, and usage examples for controlling your Tux Droid from the command line.',
  },
  {
    href: '/docs/combos',
    icon: <Eye className="w-6 h-6" />,
    title: '100 Cinematic Combos',
    desc: 'Complete list of all pre-programmed animation combos with descriptions and IDs.',
  },
  {
    href: '/docs/telegram',
    icon: <Smartphone className="w-6 h-6" />,
    title: 'Telegram Bot Setup',
    desc: 'Step-by-step guide to set up remote control via Telegram with inline keyboards.',
  },
  {
    href: '/docs/tts',
    icon: <Music className="w-6 h-6" />,
    title: 'Text-to-Speech & Audio',
    desc: 'TTS voices, MP3 playback, and audio device configuration on Windows and Linux.',
  },
  {
    href: '/docs/troubleshooting',
    icon: <Cpu className="w-6 h-6" />,
    title: 'Troubleshooting',
    desc: 'Solutions for common issues on Windows, Linux, and USB connectivity problems.',
  },
];

export default function Docs() {
  return (
    <div className="pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="mb-12">
          <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">Documentation</h1>
          <p className="text-lg text-tux-muted">Everything you need to know about ScayTux.</p>
        </div>

        <div className="space-y-4">
          {sections.map((s) => (
            <Link key={s.href} href={s.href} className="card p-6 flex items-start gap-5 transition-all block">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-tux-orange/10 to-tux-orange/5 flex items-center justify-center text-tux-orange shrink-0">
                {s.icon}
              </div>
              <div>
                <h2 className="text-lg font-semibold text-white mb-1">{s.title}</h2>
                <p className="text-sm text-tux-muted">{s.desc}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
