import Link from 'next/link';
import Image from 'next/image';
import { Github } from './Icons';

export function Footer() {
  return (
    <footer className="border-t border-white/[0.04] bg-tux-darker/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10">
          <div className="col-span-1">
            <Link href="/" className="flex items-center gap-2.5 mb-4">
              <Image src="/images/tuxdroidlogo.png" alt="Tux Droid Logo" width={28} height={28} className="h-7 w-auto object-contain" />
              <span className="text-lg font-bold gradient-text-orange">TuxDroid</span>
            </Link>
            <p className="text-sm text-tux-subtle leading-relaxed">
              The ultimate modern controller for the classic Tux Droid robot. Bring your penguin back to life!
            </p>
          </div>

          <div>
            <h3 className="text-xs font-semibold text-tux-muted uppercase tracking-widest mb-4">Product</h3>
            <ul className="space-y-2.5">
              <li><Link href="/getting-started" className="text-sm text-tux-subtle hover:text-tux-orange transition-colors duration-200">Getting Started</Link></li>
              <li><Link href="/download" className="text-sm text-tux-subtle hover:text-tux-orange transition-colors duration-200">Download</Link></li>
              <li><Link href="/docs" className="text-sm text-tux-subtle hover:text-tux-orange transition-colors duration-200">Documentation</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-xs font-semibold text-tux-muted uppercase tracking-widest mb-4">Docs</h3>
            <ul className="space-y-2.5">
              <li><Link href="/docs/commands" className="text-sm text-tux-subtle hover:text-tux-orange transition-colors duration-200">Command Reference</Link></li>
              <li><Link href="/docs/combos" className="text-sm text-tux-subtle hover:text-tux-orange transition-colors duration-200">100 Combos</Link></li>
              <li><Link href="/docs/telegram" className="text-sm text-tux-subtle hover:text-tux-orange transition-colors duration-200">Telegram Bot</Link></li>
              <li><Link href="/docs/troubleshooting" className="text-sm text-tux-subtle hover:text-tux-orange transition-colors duration-200">Troubleshooting</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-xs font-semibold text-tux-muted uppercase tracking-widest mb-4">Community</h3>
            <ul className="space-y-2.5">
              <li>
                <a href="https://github.com/Scayar/ScayTux" target="_blank" rel="noopener noreferrer" className="text-sm text-tux-subtle hover:text-tux-orange transition-colors duration-200 flex items-center gap-1.5">
                  <Github className="w-3.5 h-3.5" /> GitHub
                </a>
              </li>
              <li><a href="https://t.me/im_scayar" target="_blank" rel="noopener noreferrer" className="text-sm text-tux-subtle hover:text-tux-orange transition-colors duration-200">Telegram</a></li>
              <li><a href="https://buymeacoffee.com/scayar" target="_blank" rel="noopener noreferrer" className="text-sm text-tux-subtle hover:text-tux-orange transition-colors duration-200">Support the Project</a></li>
            </ul>
          </div>
        </div>

        <div className="mt-14 pt-8 border-t border-white/[0.04] flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-tux-subtle">&copy; {new Date().getFullYear()} ScayTux by Scayar. Licensed under LGPL-3.0.</p>
          <p className="text-xs text-tux-subtle">&ldquo;Tux Droid Never Dies!&rdquo;</p>
        </div>
      </div>
    </footer>
  );
}
