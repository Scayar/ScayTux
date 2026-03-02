export const metadata = {
  title: '100 Combos - TuxDroid',
  description: 'Complete list of all 100 cinematic animation and dance combos for Tux Droid.',
};

const combos = [
  { id: 1, name: 'Royal Entrance', desc: '"I have arrived." Slow eye open, blue light.' },
  { id: 2, name: 'Bird Flex', desc: 'Rapid wing flapping show-off.' },
  { id: 3, name: 'Brain Loading', desc: 'Thinking animation with red light and robot voice.' },
  { id: 4, name: 'Sleep Mode', desc: 'Yawn, eyes close, lights out.' },
  { id: 5, name: 'Hacker Alert', desc: 'Emergency red flash and alarm voice.' },
  { id: 6, name: 'Police Mode', desc: 'Red/Blue siren loop + "Pull over".' },
  { id: 7, name: 'Shy Bird', desc: 'Whispers and hides eyes.' },
  { id: 8, name: 'Laugh Mode', desc: 'Ha ha ha! Happy movements.' },
  { id: 9, name: 'Kiss', desc: 'Smack sound + Wink.' },
  { id: 10, name: 'Bird Crying', desc: 'Sad voice + dim blue light.' },
  { id: 11, name: 'Death Restart', desc: 'System crash simulation -> Reboot.' },
  { id: 12, name: 'Power Up', desc: 'LED gets brighter and brighter.' },
  { id: 13, name: 'Wake from Dead', desc: '"Where am I?" sequence.' },
  { id: 14, name: 'Celebration Jump', desc: '"Woo hoo!" with fast flaps.' },
  { id: 15, name: 'Virus Mode', desc: 'Glitchy voice and erratic movements.' },
  { id: 16, name: 'TikTok Headshake', desc: 'Fast left-right head shaking.' },
  { id: 17, name: 'Bird Beatbox', desc: '"Boots cats" rhythm.' },
  { id: 18, name: 'Matrix Enter', desc: '"Follow the white rabbit" (Whisper).' },
  { id: 19, name: 'Soldier Salute', desc: '"Sir yes sir!" firm stance.' },
  { id: 20, name: 'Confused Bird', desc: '"Huh?" Mouth hangs open.' },
  { id: 21, name: 'Wait WHAT?', desc: 'Shocked reaction.' },
  { id: 22, name: 'Suspicious', desc: '"I am watching you" (Whisper).' },
  { id: 23, name: 'Sir Yes Sir', desc: 'Military confirmation.' },
  { id: 24, name: 'CyberScan', desc: 'Scanning area LED pattern.' },
  { id: 25, name: 'Great Idea', desc: '"Eureka!" Yellow light flash.' },
  { id: 26, name: 'No No No', desc: 'Head shaking "No".' },
  { id: 27, name: 'YESSS', desc: '"Oh yeah!" victory flap.' },
  { id: 28, name: 'Broken Robot', desc: 'Stuttering speech and glitchy LEDs.' },
  { id: 29, name: 'Romantic Bird', desc: '"Hey baby" + Wink.' },
  { id: 30, name: 'Mafia Don', desc: '"You come to me..." (Deep voice).' },
  { id: 31, name: 'Ninja Silent', desc: 'Lights out. Stealth mode.' },
  { id: 32, name: 'Wake Ninja', desc: '"Hiiyaaa!" Surprise attack.' },
  { id: 33, name: 'JumpScare', desc: 'BOO! Sudden loud noise and red light.' },
  { id: 34, name: 'Sad Apology', desc: '"I am sorry." Head down.' },
  { id: 35, name: 'Switch OFF', desc: '"Shutting down." Everything off.' },
  { id: 36, name: 'Magic Portal', desc: '"Entering the void." Swirling lights.' },
  { id: 37, name: 'Taunting', desc: '"Try again loser." Head shake.' },
  { id: 38, name: 'Game Won', desc: 'Victory fanfare animation.' },
  { id: 39, name: 'Game Lost', desc: 'Game over sadness.' },
  { id: 40, name: 'Loading 100%', desc: 'LED progress bar animation.' },
  { id: 41, name: 'Binary Speak', desc: 'Speaks in 0s and 1s.' },
  { id: 42, name: 'Shout Mode', desc: '"CAN YOU HEAR ME NOW?" (Angry).' },
  { id: 43, name: 'Fake Shutoff', desc: 'Pretends to die... then "Just kidding!".' },
  { id: 44, name: 'Notification', desc: '"You have one new message."' },
  { id: 45, name: 'Dad Joke', desc: 'Tells a bad penguin joke.' },
  { id: 46, name: 'Rap Mode', desc: 'Raps about Linux.' },
  { id: 47, name: 'Helicopter', desc: 'Wings + Spin combo.' },
  { id: 48, name: 'Cyber Knight', desc: '"I serve the code." Blue stance.' },
  { id: 49, name: 'DJ Mode', desc: '"Drop the beat!" Club lights.' },
  { id: 50, name: 'Grand Closing', desc: 'The goodbye show.' },
  { id: 51, name: 'Disco Fever', desc: 'Alternating color strobe + 360 spin dance.' },
  { id: 52, name: 'Morning Stretch', desc: 'Slow wing stretch, yawn, eyes open.' },
  { id: 53, name: 'Pirate Captain', desc: '"Arrr matey!" One eye closed, wing salute.' },
  { id: 54, name: 'Opera Singer', desc: 'Dramatic mouth movements with crescendo LED.' },
  { id: 55, name: 'Counting Sheep', desc: '"One sheep... two sheep..." Slow blinks, sleep.' },
  { id: 56, name: 'Thunder Storm', desc: 'White LED flash + scared reaction.' },
  { id: 57, name: 'Zen Meditation', desc: 'Slow breathing, calm blue pulse, silence.' },
  { id: 58, name: 'Rocket Launch', desc: '"3... 2... 1... Liftoff!" Spin upward motion.' },
  { id: 59, name: 'Penguin Walk', desc: 'Waddle side to side with wing flaps.' },
  { id: 60, name: 'Time Bomb', desc: 'Ticking sound, LED countdown, BOOM spin.' },
  { id: 61, name: 'Weatherman', desc: '"Cloudy with a chance of penguins."' },
  { id: 62, name: 'Fitness Coach', desc: '"Drop and give me 20!" Wing push-ups.' },
  { id: 63, name: 'Alarm Clock', desc: 'Annoying beeps + eyes flash rapidly.' },
  { id: 64, name: 'Moonwalk', desc: 'Smooth spin backward, Michael Jackson style.' },
  { id: 65, name: 'Karate Chop', desc: '"HI-YA!" Quick wing strikes.' },
  { id: 66, name: 'News Anchor', desc: '"Breaking news! Penguin takes over."' },
  { id: 67, name: 'Evil Villain', desc: '"Mwahahaha!" Red glow, slow spin.' },
  { id: 68, name: 'Cheerleader', desc: '"Go team!" Fast rhythmic flaps.' },
  { id: 69, name: 'Ghostly Haunt', desc: 'Spooky voice, flickering dim light.' },
  { id: 70, name: 'Cowboy Duel', desc: '"Draw!" Quick wing snap, dramatic pause.' },
  { id: 71, name: 'Science Lab', desc: '"Experiment in progress..." Bubbling sounds.' },
  { id: 72, name: 'Royal Wave', desc: 'Slow regal wing wave, queen style.' },
  { id: 73, name: 'Breakdance', desc: 'Fast spin + wing freeze pose.' },
  { id: 74, name: 'Sneezing Fit', desc: '"Ah... ah... ACHOO!" Head jerk + blink.' },
  { id: 75, name: 'Photo Pose', desc: '"Say cheese!" Freeze with LED flash.' },
  { id: 76, name: 'Hypnotize', desc: '"Look into my eyes..." Swirling LED pattern.' },
  { id: 77, name: 'Traffic Cop', desc: 'Stop! Go! Wing directing traffic.' },
  { id: 78, name: 'Submarine', desc: 'Dive sound, eyes narrow, blue deep glow.' },
  { id: 79, name: 'Birthday Party', desc: '"Happy birthday!" Celebration with color burst.' },
  { id: 80, name: 'Mime Artist', desc: 'Silent mouth movements, invisible wall push.' },
  { id: 81, name: 'Space Explorer', desc: '"Houston, we have a penguin." Zero-G float.' },
  { id: 82, name: 'Chef Kiss', desc: '"Magnifique!" Italian chef hand kiss.' },
  { id: 83, name: 'Drill Sergeant', desc: '"ATTENTION! LEFT! RIGHT! ABOUT FACE!"' },
  { id: 84, name: 'Morse Code', desc: 'LED blinks SOS pattern with beeps.' },
  { id: 85, name: 'Surfer Dude', desc: '"Cowabunga!" Balanced wing spread.' },
  { id: 86, name: 'Orchestra Conductor', desc: 'Wing conducting with rhythm, LED tempo.' },
  { id: 87, name: 'Spy Mode', desc: '"The name is Tux. James Tux." LED off stealth.' },
  { id: 88, name: 'Fortune Teller', desc: '"I see... your future... is penguins."' },
  { id: 89, name: 'Heavyweight Champ', desc: '"I am the champion!" Victory punch combo.' },
  { id: 90, name: 'Penguin Shuffle', desc: 'Side-to-side shuffle dance, happy feet.' },
];

const musicCombos = [
  { id: 91, name: 'Michael Jackson', desc: 'Billie Jean dance (2 min).', song: 'billie.mp3' },
  { id: 92, name: 'Chicken Dance', desc: 'Chicken Song dance (2 min).', song: 'chicken.mp3' },
  { id: 93, name: 'Syrian Dabkah', desc: 'Traditional Dabke dance (2 min).', song: 'Suirian dabkah.mp3' },
  { id: 94, name: 'Crazy Mode', desc: 'Crazy song dance (2 min).', song: 'crazy.mp3' },
  { id: 95, name: 'Say My Name', desc: 'Say My Name dance (2 min).', song: 'Say My Name.mp3' },
  { id: 96, name: 'Robot Rock', desc: 'Daft Punk robot dance (2 min).', song: 'robot-rock.mp3' },
  { id: 97, name: 'Macarena', desc: 'Classic Macarena dance (2 min).', song: 'macarena.mp3' },
  { id: 98, name: 'Egyptian Walk', desc: 'Walk Like an Egyptian dance (2 min).', song: 'egyptian.mp3' },
  { id: 99, name: 'Cha Cha Slide', desc: '"Slide to the left!" dance (2 min).', song: 'cha-cha.mp3' },
  { id: 100, name: 'Tux Anthem', desc: 'Original Tux Droid theme song finale (2 min).', song: 'tux-anthem.mp3' },
];

export default function Combos() {
  return (
    <div className="pt-24 pb-16 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-4">100 Cinematic Combos</h1>
        <p className="text-lg text-tux-muted mb-4">
          Pre-programmed animation sequences. Run any combo with:
        </p>
        <div className="code-block px-4 py-3 text-sm font-mono text-tux-text mb-12">
          java -jar target/ScayTux.jar --combo &lt;ID&gt;
        </div>

        <section className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-2">Animation Combos (1-90)</h2>
          <p className="text-sm text-tux-subtle mb-6">Solo animations using motors, LEDs, and TTS voice effects.</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {combos.map((c) => (
              <div key={c.id} className="card rounded-lg p-4 transition-all flex items-start gap-3">
                <span className="text-xs font-mono text-tux-orange bg-tux-orange/10 px-2 py-0.5 rounded shrink-0 mt-0.5">
                  #{c.id}
                </span>
                <div>
                  <h3 className="text-white font-medium text-sm">{c.name}</h3>
                  <p className="text-xs text-tux-subtle mt-0.5">{c.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-white mb-2">Music + Dance Combos (91-100)</h2>
          <p className="text-tux-muted text-sm mb-6">
            These combos play an MP3 file while Tux dances along. Place audio files in <code className="text-tux-orange">assets/audio/</code>.
          </p>
          <div className="space-y-3">
            {musicCombos.map((c) => (
              <div key={c.id} className="card rounded-lg p-5 transition-all flex items-center gap-4">
                <span className="text-sm font-mono text-tux-orange bg-tux-orange/10 px-3 py-1 rounded">
                  #{c.id}
                </span>
                <div className="flex-1">
                  <h3 className="text-white font-semibold">{c.name}</h3>
                  <p className="text-xs text-tux-subtle">{c.desc}</p>
                </div>
                <span className="text-xs font-mono text-tux-subtle hidden sm:block">{c.song}</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
