import type { Metadata, Viewport } from 'next';
import './globals.css';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';

const SITE_URL = 'https://tuxdroid.com';

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: 'Tux Droid - TuxDroid Software | Control Your Linux Penguin Robot',
    template: '%s | Tux Droid - TuxDroid Software',
  },
  description: 'Tux Droid software & controller. ScayTux brings your Tux Droid robot back to life on Windows & Linux. 100 combos, Telegram remote, TTS, USB HID. The ultimate Tux Droid controller software.',
  keywords: [
    'tux',
    'tux droid',
    'tux droid software',
    'tux droid controller',
    'tuxdroid',
    'tux robot',
    'linux penguin robot',
    'Tux Droid robot',
    'ScayTux',
    'Tux Droid driver',
    'Tux Droid Windows',
    'Tux Droid Linux',
    'USB HID penguin',
    'Kysoh Tux Droid',
    'Tux Droid app',
    'control Tux Droid',
    'Tux Droid firmware',
    'penguin robot software',
  ],
  authors: [{ name: 'Scayar', url: 'https://github.com/Scayar' }],
  creator: 'Scayar',
  publisher: 'Scayar',
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
    },
  },
  alternates: {
    canonical: SITE_URL,
  },
  openGraph: {
    type: 'website',
    url: SITE_URL,
    siteName: 'Tux Droid - TuxDroid',
    title: 'Tux Droid Software - Control Your Linux Penguin Robot | TuxDroid',
    description: 'Official Tux Droid controller software. Bring your Tux Droid robot back to life with ScayTux. 100 combos, Telegram remote, TTS.',
    images: ['/images/tuxdroidlogo.png'],
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Tux Droid Software - TuxDroid | Control Your Penguin Robot',
    description: 'Official Tux Droid controller. ScayTux for Windows & Linux. 100 combos, Telegram, TTS.',
    images: ['/images/tuxdroidlogo.png'],
  },
  icons: {
    icon: '/images/tuxdroidlogo.png',
    shortcut: '/images/tuxdroidlogo.png',
    apple: '/images/tuxdroidlogo.png',
  },
  category: 'technology',
  verification: {
    google: 'K3kNPBVuQW45IjJfRDfITsnReXgubzSCpIojXBlnHjs',
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  themeColor: '#0d0d0d',
};

const jsonLd = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'WebSite',
      '@id': `${SITE_URL}/#website`,
      url: SITE_URL,
      name: 'Tux Droid - TuxDroid',
      description: 'Official Tux Droid software. Control your Tux Droid robot on Windows & Linux.',
      publisher: { '@id': `${SITE_URL}/#organization` },
      potentialAction: {
        '@type': 'SearchAction',
        target: { '@type': 'EntryPoint', urlTemplate: `${SITE_URL}/?q={search_term_string}` },
        'query-input': 'required name=search_term_string',
      },
    },
    {
      '@type': 'SoftwareApplication',
      name: 'ScayTux - Tux Droid Controller',
      applicationCategory: 'UtilitiesApplication',
      operatingSystem: 'Windows, Linux',
      description: 'ScayTux is the ultimate Tux Droid controller software. 100 cinematic combos, Telegram remote control, text-to-speech, MP3 playback with dancing. Cross-platform Java application.',
      offers: { '@type': 'Offer', price: '0', priceCurrency: 'USD' },
      downloadUrl: 'https://github.com/Scayar/ScayTux/releases',
      screenshot: `${SITE_URL}/images/tuxdroidlogo.png`,
    },
    {
      '@type': 'Organization',
      '@id': `${SITE_URL}/#organization`,
      name: 'Tux Droid - TuxDroid',
      url: SITE_URL,
      logo: { '@type': 'ImageObject', url: `${SITE_URL}/images/tuxdroidlogo.png` },
    },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-tux-black antialiased stripe-bg">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        <Navbar />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
