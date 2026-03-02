import Link from 'next/link';
import { ExternalLink, Check } from '@/components/Icons';

export const metadata = {
  title: 'Commercial License - TuxDroid',
  description: 'Commercial licensing for ScayTux. Companies, stores, and businesses must obtain a license to use, promote, or bundle ScayTux on their websites or products.',
};

export default function CommercialLicense() {
  return (
    <div className="pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">Commercial License</h1>
        <p className="text-lg text-tux-muted mb-12">
          Use ScayTux in your business? You need a commercial license.
        </p>

        <section className="mb-12">
          <div className="card p-8 border-tux-orange/20 border">
            <h2 className="text-2xl font-bold text-white mb-4">Personal Use — FREE</h2>
            <p className="text-tux-muted leading-relaxed mb-4">
              ScayTux is free for personal, educational, and non-commercial use under LGPL-3.0.
              Use it at home, in school, or for hobbies—no license required.
            </p>
            <ul className="space-y-2 text-tux-subtle">
              <li className="flex items-center gap-2">
                <Check className="w-5 h-5 text-tux-orange flex-shrink-0" />
                Individual users at home
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-5 h-5 text-tux-orange flex-shrink-0" />
                Educational institutions
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-5 h-5 text-tux-orange flex-shrink-0" />
                Open-source projects (LGPL-compatible)
              </li>
            </ul>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Commercial Use — License Required</h2>
          <div className="card p-8 border-tux-blue/20 border">
            <p className="text-tux-muted leading-relaxed mb-6">
              If you are a <strong className="text-white">company</strong>, <strong className="text-white">store</strong>, 
              or <strong className="text-white">business</strong> and want to:
            </p>
            <ul className="space-y-3 text-tux-subtle mb-6">
              <li>• Include ScayTux on your website or product listings</li>
              <li>• Promote or advertise ScayTux as part of your offerings</li>
              <li>• Bundle ScayTux with hardware or sell it as part of a package</li>
              <li>• Use ScayTux branding in marketing or social media</li>
              <li>• Redistribute ScayTux for commercial purposes</li>
            </ul>
            <p className="text-white font-semibold mb-4">
              You must obtain a Commercial License by contacting the author.
            </p>
            <p className="text-tux-muted text-sm leading-relaxed">
              Licensing terms and pricing are negotiated case-by-case. Contact us to discuss your use case.
            </p>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Contact for Licensing</h2>
          <div className="card p-8">
            <p className="text-tux-muted leading-relaxed mb-6">
              To request a Commercial License or discuss licensing options, please reach out:
            </p>
            <div className="space-y-4">
              <a
                href="mailto:Scayar.exe@gmail.com?subject=ScayTux%20Commercial%20License%20Inquiry"
                className="block card p-5 rounded-lg hover:border-tux-orange/50 transition-all group"
              >
                <div className="flex items-center gap-3">
                  <span className="text-tux-orange font-semibold group-hover:underline">Scayar.exe@gmail.com</span>
                  <ExternalLink className="w-4 h-4 text-tux-muted" />
                </div>
                <p className="text-sm text-tux-subtle mt-2">Email with subject: &quot;ScayTux Commercial License Inquiry&quot;</p>
              </a>
              <a
                href="https://t.me/im_scayar"
                target="_blank"
                rel="noopener noreferrer"
                className="block card p-5 rounded-lg hover:border-tux-orange/50 transition-all group"
              >
                <div className="flex items-center gap-3">
                  <span className="text-tux-orange font-semibold group-hover:underline">Telegram: @im_scayar</span>
                  <ExternalLink className="w-4 h-4 text-tux-muted" />
                </div>
                <p className="text-sm text-tux-subtle mt-2">Direct message for quick inquiries</p>
              </a>
            </div>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-white mb-6">Summary</h2>
          <div className="card p-6">
            <table className="w-full text-sm">
              <tbody className="text-tux-text">
                <tr className="border-b border-white/[0.04]">
                  <td className="py-3 text-tux-subtle font-medium">Personal / Hobby</td>
                  <td className="py-3 text-tux-orange font-medium">FREE (LGPL)</td>
                </tr>
                <tr className="border-b border-white/[0.04]">
                  <td className="py-3 text-tux-subtle font-medium">Educational</td>
                  <td className="py-3 text-tux-orange font-medium">FREE (LGPL)</td>
                </tr>
                <tr>
                  <td className="py-3 text-tux-subtle font-medium">Commercial (stores, companies, marketing)</td>
                  <td className="py-3 text-white font-semibold">Contact required — paid license</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <div className="mt-12 text-center">
          <Link
            href="/about"
            className="text-tux-orange hover:underline text-sm"
          >
            ← Back to About
          </Link>
        </div>
      </div>
    </div>
  );
}
