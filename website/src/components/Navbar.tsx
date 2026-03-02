'use client';

import Link from 'next/link';
import Image from 'next/image';
import { useState } from 'react';
import { Menu, X, Github } from './Icons';

const navLinks = [
  { href: '/', label: 'Home' },
  { href: '/getting-started', label: 'Getting Started' },
  { href: '/docs', label: 'Documentation' },
  { href: '/download', label: 'Download' },
  { href: '/about', label: 'About' },
  { href: '/commercial-license', label: 'Commercial License' },
];

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-tux-black/80 backdrop-blur-xl border-b border-white/[0.04]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2.5 group">
            <Image
              src="/images/tuxdroidlogo.png"
              alt="Tux Droid - Linux Penguin Robot Logo"
              width={36}
              height={36}
              className="h-9 w-auto object-contain group-hover:scale-110 transition-transform duration-200"
            />
            <span className="text-xl font-bold gradient-text-orange">TuxDroid</span>
          </Link>

          <div className="hidden md:flex items-center gap-0.5">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="px-4 py-2 text-sm text-tux-muted hover:text-white rounded-lg hover:bg-white/[0.04] transition-all duration-200"
              >
                {link.label}
              </Link>
            ))}
            <div className="w-px h-5 bg-white/[0.06] mx-2" />
            <a
              href="https://github.com/Scayar/ScayTux"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 text-tux-subtle hover:text-tux-orange rounded-lg hover:bg-white/[0.04] transition-all duration-200"
            >
              <Github className="w-5 h-5" />
            </a>
          </div>

          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 text-tux-muted hover:text-white"
          >
            {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {isOpen && (
        <div className="md:hidden bg-tux-black/95 backdrop-blur-xl border-t border-white/[0.04]">
          <div className="px-4 py-3 space-y-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setIsOpen(false)}
                className="block px-4 py-3 text-tux-muted hover:text-tux-orange rounded-lg hover:bg-white/[0.04] transition-all"
              >
                {link.label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
}
