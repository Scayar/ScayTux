export const metadata = {
  title: 'Troubleshooting - TuxDroid',
  description: 'Solutions for common ScayTux issues on Windows and Linux.',
};

const windowsIssues = [
  { issue: '"Java is not installed"', solution: 'Download Java from Adoptium (adoptium.net) or Oracle. Make sure java is in your PATH.' },
  { issue: '"Build failed"', solution: 'Delete the target/ folder and retry. Run START_WINDOWS.bat again.' },
  { issue: '"Device not found"', solution: 'Try a different USB port. Make sure the Tux Droid dongle is plugged in firmly.' },
  { issue: 'No audio from Tux', solution: 'Check Windows Sound Mixer for "TuxDroid-Audio" device. Make sure it is not muted.' },
  { issue: 'Antivirus blocks JAR', solution: 'Add an exception for the ScayTux folder in your antivirus settings.' },
];

const linuxIssues = [
  { issue: '"Permission denied" for USB', solution: 'Run the launcher script (START_LINUX.sh) which auto-configures udev rules. Or set them up manually.' },
  { issue: '"espeak not found"', solution: 'Install with: sudo apt install espeak' },
  { issue: '"libhidapi not found"', solution: 'Install with: sudo apt install libhidapi-hidraw0 libhidapi-dev' },
  { issue: 'Need to logout after setup', solution: 'Group membership (plugdev) requires a re-login or reboot to take effect.' },
  { issue: 'No audio on Linux', solution: 'Check that PulseAudio or PipeWire is running. Try: aplay -l to list devices.' },
];

const commonIssues = [
  { issue: 'Tux not responding', solution: '1. Unplug the dongle. 2. Wait 5 seconds. 3. Plug it back in. 4. Try again.' },
  { issue: 'Spin stutters or is weak', solution: 'Increase the --val value to 100 or more for a longer spin duration.' },
  { issue: 'TTS sounds robotic', solution: 'Expected on Linux (espeak). Windows uses native speech synthesis which sounds more natural.' },
  { issue: 'Music plays but no dance', solution: 'Make sure you are using --play (which auto-dances) or music combos (51-55).' },
  { issue: 'Telegram bot not connecting', solution: 'Check your internet connection, verify the bot token is correct, and ensure no firewall blocks outbound HTTPS.' },
];

function IssueTable({ issues }: { issues: { issue: string; solution: string }[] }) {
  return (
    <div className="bg-tux-card border border-tux-border rounded-xl overflow-hidden">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-white/[0.04]">
            <th className="text-left p-4 text-tux-muted font-medium w-1/3">Issue</th>
            <th className="text-left p-4 text-tux-muted font-medium">Solution</th>
          </tr>
        </thead>
        <tbody className="text-tux-text">
          {issues.map((item, i) => (
            <tr key={i} className="border-b border-white/[0.04] hover:bg-white/[0.02]">
              <td className="p-4 text-red-400/80 font-medium">{item.issue}</td>
              <td className="p-4 text-tux-muted">{item.solution}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function Troubleshooting() {
  return (
    <div className="pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-4">Troubleshooting</h1>
        <p className="text-lg text-tux-muted mb-12">Solutions for common issues.</p>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
            <span className="text-blue-400">Windows</span> Issues
          </h2>
          <IssueTable issues={windowsIssues} />
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
            <span className="text-green-400">Linux</span> Issues
          </h2>
          <IssueTable issues={linuxIssues} />
        </section>

        <section className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Common Issues</h2>
          <IssueTable issues={commonIssues} />
        </section>

        <section>
          <h2 className="text-2xl font-bold text-white mb-4">Still Need Help?</h2>
          <div className="card p-6">
            <p className="text-tux-muted mb-4">
              If your issue is not listed here:
            </p>
            <ul className="text-sm text-tux-muted space-y-2">
              <li>Open an issue on <a href="https://github.com/Scayar/ScayTux/issues" className="text-tux-orange hover:underline" target="_blank" rel="noopener noreferrer">GitHub Issues</a></li>
              <li>Contact on Telegram: <a href="https://t.me/im_scayar" className="text-tux-orange hover:underline" target="_blank" rel="noopener noreferrer">@im_scayar</a></li>
              <li>Email: <a href="mailto:Scayar.exe@gmail.com" className="text-tux-orange hover:underline">Scayar.exe@gmail.com</a></li>
            </ul>
          </div>
        </section>
      </div>
    </div>
  );
}
