import { CodeBlock } from '@/components/CodeBlock';

export const metadata = {
  title: 'Telegram Bot Setup - TuxDroid',
  description: 'Set up Telegram remote control for your Tux Droid.',
};

const botCommands = [
  { cmd: '/start', desc: 'Show main menu with inline keyboard buttons' },
  { cmd: '/connect', desc: 'Connect to Tux Droid hardware' },
  { cmd: '/disconnect', desc: 'Disconnect from Tux Droid' },
  { cmd: '/status', desc: 'Check connection and music status' },
  { cmd: '/flap', desc: 'Flap wings' },
  { cmd: '/blink', desc: 'Blink eyes' },
  { cmd: '/dance', desc: 'Dance animation' },
  { cmd: '/say <text>', desc: 'Make Tux speak with lip sync' },
  { cmd: '/combo<n>', desc: 'Run a combo (1-55)' },
  { cmd: '/music', desc: 'Show music menu' },
  { cmd: '/stop', desc: 'Stop music playback' },
  { cmd: '/help', desc: 'Show help message' },
];

export default function TelegramDocs() {
  return (
    <div className="pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-4">Telegram Bot Setup</h1>
        <p className="text-lg text-tux-muted mb-12">Control your Tux Droid from anywhere via Telegram.</p>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Setup Guide</h2>

          <div className="space-y-8">
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-3">
                <span className="w-7 h-7 rounded-full bg-tux-orange/10 text-tux-orange flex items-center justify-center text-sm font-bold">1</span>
                Create a Bot
              </h3>
              <ol className="text-tux-muted text-sm space-y-2 ml-10 list-decimal">
                <li>Open Telegram and search for <a href="https://t.me/BotFather" className="text-tux-orange hover:underline" target="_blank" rel="noopener noreferrer">@BotFather</a></li>
                <li>Send <code className="text-tux-orange">/newbot</code></li>
                <li>Choose a name (e.g., &ldquo;My Tux Controller&rdquo;)</li>
                <li>Choose a username ending in &ldquo;bot&rdquo; (e.g., &ldquo;my_tux_bot&rdquo;)</li>
                <li>Copy the <strong>bot token</strong> (looks like <code className="text-tux-subtle">123456789:ABCdefGHIjklMNO...</code>)</li>
              </ol>
            </div>

            <div className="card p-6">
              <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-3">
                <span className="w-7 h-7 rounded-full bg-tux-orange/10 text-tux-orange flex items-center justify-center text-sm font-bold">2</span>
                Get Your Chat ID
              </h3>
              <ol className="text-tux-muted text-sm space-y-2 ml-10 list-decimal">
                <li>Search for <a href="https://t.me/userinfobot" className="text-tux-orange hover:underline" target="_blank" rel="noopener noreferrer">@userinfobot</a> in Telegram</li>
                <li>Send <code className="text-tux-orange">/start</code></li>
                <li>Copy your <strong>numeric Chat ID</strong></li>
              </ol>
              <p className="text-xs text-tux-subtle mt-3 ml-10">
                The Chat ID is used for security - only messages from this ID will be accepted.
              </p>
            </div>

            <div className="card p-6">
              <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-3">
                <span className="w-7 h-7 rounded-full bg-tux-orange/10 text-tux-orange flex items-center justify-center text-sm font-bold">3</span>
                Configure in ScayTux
              </h3>
              <p className="text-tux-muted text-sm ml-10 mb-3">
                Launch ScayTux and go to <strong>Telegram Control</strong> &rarr; <strong>Configure Bot</strong>:
              </p>
              <CodeBlock code={`java -jar target/ScayTux.jar
# Select: 3 (Telegram Control)
# Select: 1 (Configure Bot)
# Enter your bot token and chat ID`} lang="bash" />
              <p className="text-xs text-tux-subtle mt-3 ml-10">
                Configuration is saved to <code>telegram_config.json</code> for persistence.
              </p>
            </div>

            <div className="card p-6">
              <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-3">
                <span className="w-7 h-7 rounded-full bg-tux-orange/10 text-tux-orange flex items-center justify-center text-sm font-bold">4</span>
                Start the Bot
              </h3>
              <p className="text-tux-muted text-sm ml-10">
                Select <strong>Start Bot</strong> from the Telegram menu. Then open Telegram and send <code className="text-tux-orange">/start</code> to your bot. You will see an inline keyboard with all controls!
              </p>
            </div>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Bot Commands</h2>
          <div className="bg-tux-card border border-tux-border rounded-xl overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/[0.04]">
                  <th className="text-left p-4 text-tux-muted font-medium">Command</th>
                  <th className="text-left p-4 text-tux-muted font-medium">Description</th>
                </tr>
              </thead>
              <tbody className="text-tux-text">
                {botCommands.map((c, i) => (
                  <tr key={i} className="border-b border-white/[0.04] hover:bg-white/[0.02]">
                    <td className="p-4 font-mono text-tux-orange text-xs">{c.cmd}</td>
                    <td className="p-4">{c.desc}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-white mb-6">Features</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="card p-5">
              <h3 className="text-white font-semibold mb-2">Inline Keyboards</h3>
              <p className="text-sm text-tux-muted">Navigate menus with button taps - no typing needed.</p>
            </div>
            <div className="card p-5">
              <h3 className="text-white font-semibold mb-2">Security</h3>
              <p className="text-sm text-tux-muted">Only your authorized Chat ID can control the bot.</p>
            </div>
            <div className="card p-5">
              <h3 className="text-white font-semibold mb-2">Background Mode</h3>
              <p className="text-sm text-tux-muted">Bot runs in the background while you use other features.</p>
            </div>
            <div className="card p-5">
              <h3 className="text-white font-semibold mb-2">Music Control</h3>
              <p className="text-sm text-tux-muted">Play/stop music and trigger dance combos remotely.</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
