import { CodeBlock } from '@/components/CodeBlock';

export const metadata = {
  title: 'Command Reference - TuxDroid',
  description: 'Complete CLI command reference for ScayTux.',
};

const commands = [
  { flag: '-i, --interactive', desc: 'Force interactive mode', example: '-i' },
  { flag: '--flap', desc: 'Flap wings up and down', example: '--flap' },
  { flag: '--eyes <bool>', desc: 'Open (true) or close (false) eyes', example: '--eyes true' },
  { flag: '--blink <n>', desc: 'Blink eyes N times', example: '--blink 5' },
  { flag: '--mouth <bool>', desc: 'Open (true) or close (false) mouth', example: '--mouth true' },
  { flag: '--talk <n>', desc: 'Move mouth N times (simulate talking)', example: '--talk 10' },
  { flag: '--spin <dir>', desc: 'Spin left or right', example: '--spin left' },
  { flag: '--val <n>', desc: 'Duration/loops for spin (default 20)', example: '--val 100' },
  { flag: '--led <color>', desc: 'LED color (1=Red, 2=Blue, 3=Yellow)', example: '--led 2' },
  { flag: '--intensity <n>', desc: 'LED intensity (0-255)', example: '--intensity 255' },
  { flag: '--say <text>', desc: 'Speak text with TTS and lip sync', example: '--say "Hello World"' },
  { flag: '--combo <id>', desc: 'Run a cinematic combo (1-55)', example: '--combo 6' },
  { flag: '--play <file>', desc: 'Play MP3 file with auto dance', example: '--play song.mp3' },
  { flag: '--spin-doctor', desc: 'Run spin motor diagnostic', example: '--spin-doctor' },
  { flag: '-l, --list', desc: 'Check device connection', example: '-l' },
  { flag: '-d, --debug', desc: 'Debug HID input monitor', example: '-d' },
];

export default function Commands() {
  return (
    <div className="pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-4">Command Reference</h1>
        <p className="text-lg text-tux-muted mb-12">All available CLI flags and options.</p>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Basic Usage</h2>
          <CodeBlock code="java -jar target/ScayTux.jar [OPTIONS]" lang="bash" />
          <p className="mt-3 text-sm text-tux-subtle">
            Run with no arguments to launch Interactive Mode. Add flags for direct command execution.
          </p>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">All Commands</h2>
          <div className="bg-tux-card border border-tux-border rounded-xl overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/[0.04]">
                  <th className="text-left p-4 text-tux-muted font-medium">Flag</th>
                  <th className="text-left p-4 text-tux-muted font-medium">Description</th>
                  <th className="text-left p-4 text-tux-muted font-medium hidden sm:table-cell">Example</th>
                </tr>
              </thead>
              <tbody className="text-tux-text">
                {commands.map((cmd, i) => (
                  <tr key={i} className="border-b border-white/[0.04] hover:bg-white/[0.02]">
                    <td className="p-4 font-mono text-tux-orange text-xs">{cmd.flag}</td>
                    <td className="p-4">{cmd.desc}</td>
                    <td className="p-4 font-mono text-xs text-tux-subtle hidden sm:table-cell">{cmd.example}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Examples</h2>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-tux-muted mb-2">Make Tux flap, blink, and speak:</p>
              <CodeBlock code='java -jar target/ScayTux.jar --flap --blink 3 --say "Hello!"' lang="bash" />
            </div>
            <div>
              <p className="text-sm text-tux-muted mb-2">Spin left for a long time with blue LED:</p>
              <CodeBlock code='java -jar target/ScayTux.jar --spin left --val 200 --led 2 --intensity 255' lang="bash" />
            </div>
            <div>
              <p className="text-sm text-tux-muted mb-2">Play music with auto-dance:</p>
              <CodeBlock code='java -jar target/ScayTux.jar --play assets/audio/billie.mp3' lang="bash" />
            </div>
            <div>
              <p className="text-sm text-tux-muted mb-2">Run the Police Mode combo:</p>
              <CodeBlock code='java -jar target/ScayTux.jar --combo 6' lang="bash" />
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
