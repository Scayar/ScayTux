import { CodeBlock } from '@/components/CodeBlock';
import { Download, Github, ExternalLink } from '@/components/Icons';

export const metadata = {
  title: 'Download - TuxDroid',
  description: 'Download ScayTux - The Ultimate Tux Droid Controller.',
};

export default function DownloadPage() {
  return (
    <div className="pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">Download</h1>
        <p className="text-lg text-tux-muted mb-12">Get ScayTux and bring your Tux Droid back to life.</p>

        {/* Main Download */}
        <section className="mb-12">
          <div className="glass glow-border rounded-2xl p-8 text-center">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-tux-orange to-tux-orange-light flex items-center justify-center mx-auto mb-6">
              <Download className="w-8 h-8 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">ScayTux v3.0</h2>
            <p className="text-tux-muted mb-6">Latest release - Cross-platform fat JAR</p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <a
                href="https://github.com/Scayar/ScayTux/releases/latest"
                target="_blank"
                rel="noopener noreferrer"
                className="px-8 py-3.5 rounded-xl bg-gradient-to-r from-tux-orange to-tux-orange-light text-white font-semibold hover:opacity-90 transition-opacity flex items-center gap-2"
              >
                <Download className="w-4 h-4" /> Download from GitHub
              </a>
              <a
                href="https://github.com/Scayar/ScayTux"
                target="_blank"
                rel="noopener noreferrer"
                className="px-8 py-3.5 rounded-xl card text-tux-text font-semibold flex items-center gap-2"
              >
                <Github className="w-4 h-4" /> Source Code
              </a>
            </div>
          </div>
        </section>

        {/* Quick Install */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Quick Install</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                <span className="text-blue-400">Windows</span>
              </h3>
              <CodeBlock code={`git clone https://github.com/Scayar/ScayTux
cd ScayTux
START_WINDOWS.bat`} lang="powershell" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                <span className="text-green-400">Linux</span>
              </h3>
              <CodeBlock code={`git clone https://github.com/Scayar/ScayTux
cd ScayTux
chmod +x START_LINUX.sh
./START_LINUX.sh`} lang="bash" />
            </div>
          </div>
        </section>

        {/* Build from Source */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Build from Source</h2>
          <p className="text-tux-muted mb-4">
            Requires Java 8+ and Maven 3.6+ installed on your system.
          </p>
          <CodeBlock code={`git clone https://github.com/Scayar/ScayTux
cd ScayTux
mvn clean package -DskipTests
java -jar target/ScayTux.jar`} lang="bash" />
        </section>

        {/* Dependencies */}
        <section>
          <h2 className="text-2xl font-bold text-white mb-6">Dependencies</h2>
          <p className="text-tux-muted mb-4 text-sm">
            All dependencies are bundled in the fat JAR via Maven Shade plugin.
          </p>
          <div className="card overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/[0.04]">
                  <th className="text-left p-4 text-tux-muted font-medium">Library</th>
                  <th className="text-left p-4 text-tux-muted font-medium">Version</th>
                  <th className="text-left p-4 text-tux-muted font-medium">Purpose</th>
                </tr>
              </thead>
              <tbody className="text-tux-text">
                {[
                  { name: 'hid4java', ver: '0.8.0', purpose: 'USB HID communication' },
                  { name: 'Picocli', ver: '4.7.5', purpose: 'CLI argument parsing' },
                  { name: 'JLayer', ver: '1.0.1', purpose: 'MP3 decoding' },
                  { name: 'TelegramBots', ver: '6.8.0', purpose: 'Telegram Bot API' },
                  { name: 'Gson', ver: '2.10.1', purpose: 'JSON configuration' },
                  { name: 'JUnit 5', ver: '5.10.0', purpose: 'Unit testing' },
                ].map((d, i) => (
                  <tr key={i} className="border-b border-white/[0.04]">
                    <td className="p-4 font-semibold text-tux-orange">{d.name}</td>
                    <td className="p-4 font-mono text-xs text-tux-subtle">{d.ver}</td>
                    <td className="p-4">{d.purpose}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}
