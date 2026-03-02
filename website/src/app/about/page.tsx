import Image from 'next/image';
import Link from 'next/link';
import { Github, ExternalLink } from '@/components/Icons';

export const metadata = {
  title: 'About - TuxDroid',
  description: 'About ScayTux and the Tux Droid project.',
};

export default function About() {
  return (
    <div className="pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">About</h1>
        <p className="text-lg text-tux-muted mb-12">The story behind ScayTux.</p>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">What is Tux Droid?</h2>
          <div className="card p-6">
            <p className="text-tux-muted leading-relaxed mb-4">
              The <strong className="text-white">Tux Droid</strong> is a Linux mascot robot originally created by Kysoh in 2006. 
              It&apos;s a USB-connected penguin robot that can move its eyes, beak, wings, and body. It was originally 
              designed as an email notifier and desktop companion for Linux users, but the company shut down and 
              the original software became abandoned and incompatible with modern systems.
            </p>
            <p className="text-tux-muted leading-relaxed">
              The robot communicates through a wireless USB &ldquo;Fishtank&rdquo; dongle using the HID protocol, making it 
              possible to send commands directly over USB without any special drivers.
            </p>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">What is ScayTux?</h2>
          <div className="card p-6">
            <p className="text-tux-muted leading-relaxed mb-4">
              <strong className="text-white">ScayTux</strong> is a modern, from-scratch rewrite that brings the Tux Droid back to 
              life on modern Windows 10/11 and Linux systems. No more outdated Python scripts, broken dependencies, 
              or abandoned 32-bit libraries.
            </p>
            <p className="text-tux-muted leading-relaxed mb-4">
              Built with Java for true cross-platform support, ScayTux uses the hid4java library for direct USB HID 
              communication, providing reliable and fast control of the robot.
            </p>
            <p className="text-tux-muted leading-relaxed">
              Version 3.0 includes 100 pre-programmed cinematic animation combos, Telegram remote control, 
              text-to-speech with lip sync, MP3 playback with dancing, and a beautiful interactive CLI.
            </p>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Hardware Specifications</h2>
          <div className="card overflow-hidden">
            <table className="w-full text-sm">
              <tbody className="text-tux-text">
                {[
                  ['Connection', 'USB HID via Fishtank dongle'],
                  ['Vendor ID', '0x03eb (Atmel)'],
                  ['Product ID', '0xFF07'],
                  ['Packet Size', '64 bytes'],
                  ['Motors', 'Eyes, Mouth, Wings (Flippers), Body Spin'],
                  ['LEDs', 'RGB LED in nose (color + intensity control)'],
                  ['Audio', 'Built-in speaker via USB audio device (TuxDroid-Audio)'],
                  ['Buttons', 'Head button, Left wing, Right wing'],
                  ['Communication', 'Wireless RF between dongle and robot'],
                ].map(([label, value], i) => (
                  <tr key={i} className="border-b border-white/[0.04]">
                    <td className="p-4 text-tux-subtle font-medium w-1/3">{label}</td>
                    <td className="p-4 font-mono text-xs">{value}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Author</h2>
          <div className="card p-6">
            <div className="flex items-center gap-4 mb-4">
              <Image
                src="/images/me.jpg"
                alt="Scayar - Creator of ScayTux Tux Droid Software"
                width={64}
                height={64}
                className="w-16 h-16 rounded-full object-cover border-2 border-tux-orange/30"
              />
              <div>
                <h3 className="text-xl font-bold text-white">Scayar</h3>
                <p className="text-sm text-tux-muted">Creator of ScayTux</p>
              </div>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-6">
              <a href="https://github.com/Scayar" target="_blank" rel="noopener noreferrer" className="card rounded-lg p-3 flex items-center gap-3 transition-all">
                <Github className="w-5 h-5 text-tux-muted" />
                <span className="text-sm text-tux-text">github.com/Scayar</span>
              </a>
              <a href="https://t.me/im_scayar" target="_blank" rel="noopener noreferrer" className="card rounded-lg p-3 flex items-center gap-3 transition-all">
                <ExternalLink className="w-5 h-5 text-tux-muted" />
                <span className="text-sm text-tux-text">@im_scayar (Telegram)</span>
              </a>
              <a href="mailto:Scayar.exe@gmail.com" className="card rounded-lg p-3 flex items-center gap-3 transition-all">
                <ExternalLink className="w-5 h-5 text-tux-muted" />
                <span className="text-sm text-tux-text">Scayar.exe@gmail.com</span>
              </a>
              <a href="https://buymeacoffee.com/scayar" target="_blank" rel="noopener noreferrer" className="card rounded-lg p-3 flex items-center gap-3 transition-all">
                <ExternalLink className="w-5 h-5 text-tux-muted" />
                <span className="text-sm text-tux-text">Buy Me a Coffee</span>
              </a>
            </div>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-white mb-6">License</h2>
          <div className="card p-6">
            <p className="text-tux-muted leading-relaxed mb-4">
              ScayTux is licensed under the <strong className="text-white">GNU Lesser General Public License v3.0</strong> (LGPL-3.0) for personal and educational use.
            </p>
            <p className="text-tux-muted leading-relaxed mb-4 text-sm">
              Personal use is free. <strong className="text-white">Companies, stores, and businesses</strong> that want to use, promote, or bundle ScayTux on their websites or products must obtain a <Link href="/commercial-license" className="text-tux-orange hover:underline">Commercial License</Link>. Contact for pricing.
            </p>
            <p className="text-tux-muted leading-relaxed text-sm">
              See the full <Link href="/commercial-license" className="text-tux-orange hover:underline">Commercial License page</Link> for details.
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}
