import { CodeBlock } from '@/components/CodeBlock';

export const metadata = {
  title: 'Text-to-Speech & Audio - TuxDroid',
  description: 'TTS configuration and audio playback guide for Tux Droid.',
};

const voices = [
  { name: 'NORMAL', desc: 'Default voice, standard speed and pitch' },
  { name: 'WHISPER', desc: 'Quiet and slow, great for secrets' },
  { name: 'ANGRY', desc: 'Deep pitch, fast and aggressive' },
  { name: 'CUTE', desc: 'High pitch, cheerful' },
  { name: 'SAD', desc: 'Deep and slow, melancholic' },
  { name: 'ROBOT', desc: 'Monotone, mechanical' },
  { name: 'ANNOUNCER', desc: 'Deep and authoritarian' },
];

export default function TTSDocs() {
  return (
    <div className="pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-4">Text-to-Speech &amp; Audio</h1>
        <p className="text-lg text-tux-muted mb-12">Make your Tux Droid talk and play music.</p>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Text-to-Speech</h2>

          <div className="card p-6 mb-6">
            <h3 className="text-lg font-semibold text-white mb-3">How It Works</h3>
            <ul className="text-sm text-tux-muted space-y-2">
              <li><strong className="text-blue-400">Windows:</strong> Uses built-in PowerShell Speech Synthesis (System.Speech) - no installation needed.</li>
              <li><strong className="text-green-400">Linux:</strong> Uses espeak or espeak-ng. Install with: <code className="text-tux-orange">sudo apt install espeak</code></li>
            </ul>
          </div>

          <div className="mb-6">
            <h3 className="text-lg font-semibold text-white mb-3">Basic Usage</h3>
            <CodeBlock code='java -jar target/ScayTux.jar --say "Hello, I am Tux Droid!"' lang="bash" />
            <p className="text-sm text-tux-subtle mt-2">
              TTS includes organic lip sync - Tux&apos;s mouth moves naturally while speaking.
            </p>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-white mb-4">Available Voices</h3>
            <p className="text-sm text-tux-muted mb-4">
              Voices are used internally by combos to create different character personalities:
            </p>
            <div className="bg-tux-card border border-tux-border rounded-xl overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/[0.04]">
                    <th className="text-left p-4 text-tux-muted font-medium">Voice</th>
                    <th className="text-left p-4 text-tux-muted font-medium">Description</th>
                  </tr>
                </thead>
                <tbody className="text-tux-text">
                  {voices.map((v) => (
                    <tr key={v.name} className="border-b border-white/[0.04]">
                      <td className="p-4 font-mono text-tux-orange text-xs">{v.name}</td>
                      <td className="p-4">{v.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Audio Player</h2>

          <div className="card p-6 mb-6">
            <h3 className="text-lg font-semibold text-white mb-3">Supported Formats</h3>
            <ul className="text-sm text-tux-muted space-y-1">
              <li><strong>MP3</strong> - Primary format, decoded with JLayer</li>
              <li><strong>WAV / FLAC / M4A / AAC</strong> - Played via system audio player</li>
            </ul>
          </div>

          <div className="mb-6">
            <h3 className="text-lg font-semibold text-white mb-3">Play Music with Dance</h3>
            <CodeBlock code='java -jar target/ScayTux.jar --play assets/audio/billie.mp3' lang="bash" />
            <p className="text-sm text-tux-subtle mt-2">
              Tux automatically dances while the music plays, picking random dance moves.
            </p>
          </div>

          <div>
            <h3 className="text-lg font-semibold text-white mb-3">Audio File Location</h3>
            <p className="text-sm text-tux-muted mb-3">
              Place audio files in <code className="text-tux-orange">assets/audio/</code>. The player searches in this order:
            </p>
            <ol className="text-sm text-tux-muted list-decimal ml-6 space-y-1">
              <li>Exact path as given</li>
              <li>Current directory</li>
              <li><code>assets/audio/</code> folder</li>
              <li><code>../assets/audio/</code> folder</li>
            </ol>
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-white mb-6">TuxDroid Audio Hardware (Windows)</h2>
          <p className="text-sm text-tux-muted mb-4">
            On Windows, ScayTux automatically detects the TuxDroid-Audio USB device and routes audio through it. 
            The audio is converted to 8-bit mono for hardware compatibility and maximum volume is set automatically.
          </p>
          <p className="text-sm text-tux-muted">
            If TuxDroid-Audio is not detected, playback falls back to the default system audio device.
          </p>
        </section>
      </div>
    </div>
  );
}
