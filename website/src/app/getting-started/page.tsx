import { CodeBlock } from '@/components/CodeBlock';
import Link from 'next/link';

export const metadata = {
  title: 'Getting Started - TuxDroid',
  description: 'Set up ScayTux and control your Tux Droid in under 5 minutes.',
};

export default function GettingStarted() {
  return (
    <div className="pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="mb-12">
          <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">Getting Started</h1>
          <p className="text-lg text-tux-muted">From zero to dancing penguin in under 5 minutes.</p>
        </div>

        {/* Requirements */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
            <span className="w-8 h-8 rounded-lg bg-tux-orange/10 text-tux-orange flex items-center justify-center text-sm font-mono">1</span>
            System Requirements
          </h2>
          <div className="card overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/[0.04]">
                  <th className="text-left p-4 text-tux-muted font-medium">Platform</th>
                  <th className="text-left p-4 text-tux-muted font-medium">Requirement</th>
                  <th className="text-left p-4 text-tux-muted font-medium">How to Install</th>
                </tr>
              </thead>
              <tbody className="text-tux-text">
                <tr className="border-b border-white/[0.04]">
                  <td className="p-4">All</td>
                  <td className="p-4">Java 8+</td>
                  <td className="p-4"><a href="https://adoptium.net/" className="text-tux-orange hover:underline" target="_blank" rel="noopener noreferrer">Adoptium</a> or <a href="https://www.oracle.com/java/technologies/downloads/" className="text-tux-orange hover:underline" target="_blank" rel="noopener noreferrer">Oracle JDK</a></td>
                </tr>
                <tr className="border-b border-white/[0.04]">
                  <td className="p-4">All</td>
                  <td className="p-4">Maven 3.6+</td>
                  <td className="p-4">Auto-installed by launcher scripts</td>
                </tr>
                <tr className="border-b border-white/[0.04]">
                  <td className="p-4">Linux</td>
                  <td className="p-4">libhidapi</td>
                  <td className="p-4 font-mono text-xs">sudo apt install libhidapi-hidraw0 libhidapi-dev</td>
                </tr>
                <tr>
                  <td className="p-4">Linux</td>
                  <td className="p-4">espeak (for TTS)</td>
                  <td className="p-4 font-mono text-xs">sudo apt install espeak</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="mt-4 card p-4">
            <p className="text-sm text-tux-muted">
              <strong className="text-tux-orange">Hardware:</strong> Tux Droid robot with its USB &ldquo;Fishtank&rdquo; dongle (VID: 0x03eb, PID: 0xFF07).
            </p>
          </div>
        </section>

        {/* Windows */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
            <span className="w-8 h-8 rounded-lg bg-tux-orange/10 text-tux-orange flex items-center justify-center text-sm font-mono">2</span>
            Installation
          </h2>

          <div className="space-y-8">
            <div>
              <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                <span className="text-blue-400">Windows</span> (One-Click)
              </h3>
              <CodeBlock code={`# Clone the repository
git clone https://github.com/Scayar/ScayTux
cd ScayTux

# Double-click to run (or from terminal):
START_WINDOWS.bat`} lang="powershell" />
              <p className="mt-3 text-sm text-tux-subtle">
                The batch file automatically installs portable Maven, builds the project, and launches Interactive Mode.
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                <span className="text-green-400">Linux</span> (One-Command)
              </h3>
              <CodeBlock code={`git clone https://github.com/Scayar/ScayTux
cd ScayTux
chmod +x START_LINUX.sh && ./START_LINUX.sh`} lang="bash" />
              <p className="mt-3 text-sm text-tux-subtle">
                Automatically installs OpenJDK, Maven, espeak, libhidapi, and configures udev rules for USB access.
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                <span className="text-yellow-400">Manual Build</span> (Any Platform)
              </h3>
              <CodeBlock code={`git clone https://github.com/Scayar/ScayTux
cd ScayTux
mvn clean package -DskipTests
java -jar target/ScayTux.jar`} lang="bash" />
            </div>
          </div>
        </section>

        {/* Linux USB */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
            <span className="w-8 h-8 rounded-lg bg-tux-orange/10 text-tux-orange flex items-center justify-center text-sm font-mono">3</span>
            Linux USB Permissions
          </h2>
          <p className="text-tux-muted mb-4">
            The launcher script handles this automatically, but for manual setup:
          </p>
          <CodeBlock code={`# Create udev rule for Tux Droid dongle
sudo bash -c 'cat > /etc/udev/rules.d/99-tuxdroid.rules << EOF
SUBSYSTEM=="usb", ATTR{idVendor}=="03eb", ATTR{idProduct}=="ff07", MODE="0666", GROUP="plugdev"
KERNEL=="hidraw*", ATTR{idVendor}=="03eb", ATTR{idProduct}=="ff07", MODE="0666", GROUP="plugdev"
EOF'

# Reload rules and add yourself to plugdev
sudo udevadm control --reload-rules
sudo udevadm trigger
sudo usermod -aG plugdev $USER

# Log out and back in for group changes to take effect`} lang="bash" />
        </section>

        {/* First Run */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
            <span className="w-8 h-8 rounded-lg bg-tux-orange/10 text-tux-orange flex items-center justify-center text-sm font-mono">4</span>
            First Run
          </h2>
          <p className="text-tux-muted mb-4">
            Launch ScayTux with no arguments to enter Interactive Mode:
          </p>
          <CodeBlock code={`java -jar target/ScayTux.jar`} lang="bash" />
          <div className="mt-6 code-block p-4 text-sm text-tux-muted font-mono whitespace-pre leading-relaxed">{`[ MAIN MENU ]
1. Interactive Menu (Select combos by number)
2. Manual / REPL Mode (Type commands freely)
3. Telegram Control (Control via Telegram Bot)
4. Exit`}</div>
          <p className="mt-4 text-sm text-tux-subtle">
            Select option 1 to browse combos, option 2 to type commands manually, or option 3 to set up Telegram remote control.
          </p>
        </section>

        {/* Next Steps */}
        <section>
          <h2 className="text-2xl font-bold text-white mb-6">Next Steps</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Link href="/docs/commands" className="card p-5 block transition-all">
              <h3 className="text-white font-semibold mb-1">Command Reference</h3>
              <p className="text-sm text-tux-subtle">All CLI flags and options</p>
            </Link>
            <Link href="/docs/combos" className="card p-5 block transition-all">
              <h3 className="text-white font-semibold mb-1">100 Combos</h3>
              <p className="text-sm text-tux-subtle">Browse all animations</p>
            </Link>
            <Link href="/docs/telegram" className="card p-5 block transition-all">
              <h3 className="text-white font-semibold mb-1">Telegram Bot Setup</h3>
              <p className="text-sm text-tux-subtle">Control from your phone</p>
            </Link>
            <Link href="/docs/troubleshooting" className="card p-5 block transition-all">
              <h3 className="text-white font-semibold mb-1">Troubleshooting</h3>
              <p className="text-sm text-tux-subtle">Common issues and fixes</p>
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
}
