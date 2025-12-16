# 🐧 Tux Droid Command Reference Guide (Ultimate Edition)

This document lists **all** available commands for your Tux Droid using the `run.sh` script.

## 🚀 Basic Hardware Control
Control individual parts of the robot.

| Command | Example | Description |
| :--- | :--- | :--- |
| **Wings** | `./run.sh --flap` | Flaps the wings up and down. |
| **Eyes** | `./run.sh --eyes true` | Opens eyes. Use `false` to close. |
| **Blink** | `./run.sh --blink 5` | Blinks the eyes N times. |
| **Mouth** | `./run.sh --mouth true` | Opens the beak. Use `false` to close. |
| **Spin** | `./run.sh --spin left --val 100` | Spins left. **Value controls duration** (loops). Higher = longer spin. |
| **Talk** | `./run.sh --say "Hello"` | Speaks text with **Organic Lip Sync** (mouth moves naturally). |
| **LED** | `./run.sh --led 1 --intensity 200` | Sets LED. `1`=Red, `2`=Blue, `3`=Yellow/Green. |

---

## 🎭 The 50 Cinematic Combos (Ultimate List)
Run any of these using `./run.sh --combo <ID>`

| ID | Name | Description |
| :--- | :--- | :--- |
| **1** | **Royal Entrance** | "I have arrived." Slow eye open, blue light. |
| **2** | **Bird Flex** | Rapid wing flapping show-off. |
| **3** | **Brain Loading** | Thinking animation with red light and robot voice. |
| **4** | **Sleep Mode** | Yawn, eyes close, lights out. |
| **5** | **Hacker Alert** | Emergency red flash and alarm voice. |
| **6** | **Police Mode** | Red/Blue siren loop + "Pull over". |
| **7** | **Shy Bird** | Whispers and hides eyes. |
| **8** | **Laugh Mode** | Ha ha ha! Happy movements. |
| **9** | **Kiss 😘** | Smack sound + Wink. |
| **10** | **Bird Crying** | Sad voice + dim blue light. |
| **11** | **Death Restart** | System crash simulation -> Reboot. |
| **12** | **Power Up** | LED gets brighter and brighter. |
| **13** | **Wake from Dead** | "Where am I?" sequence. |
| **14** | **Celebration Jump** | "Woo hoo!" with fast flaps. |
| **15** | **Virus Mode** | Glitchy voice and erratic movements. |
| **16** | **TikTok Headshake** | Fast left-right head shaking. |
| **17** | **Bird Beatbox** | "Boots cats" rhythm. |
| **18** | **Matrix Enter** | "Follow the white rabbit" (Whisper). |
| **19** | **Soldier Salute** | "Sir yes sir!" firm stance. |
| **20** | **Confused Bird** | "Huh?" Mouth hangs open. |
| **21** | **Wait WHAT?** | Shocked reaction. |
| **22** | **Suspicious** | "I am watching you" (Whisper). |
| **23** | **Sir Yes Sir** | Military confirmation. |
| **24** | **CyberScan** | Scanning area led pattern. |
| **25** | **Great Idea 💡** | "Eureka!" Yellow light flash. |
| **26** | **No No No** | Head shaking "No". |
| **27** | **YESSS** | "Oh yeah!" victory flap. |
| **28** | **Broken Robot** | Stuttering speech and glitchy LEDs. |
| **29** | **Romantic Bird ❤️** | "Hey baby" + Wink. |
| **30** | **Mafia Don** | "You come to me..." (Deep voice). |
| **31** | **Ninja Silent** | Lights out. Stealth mode. |
| **32** | **Wake Ninja** | "Hiiyaaa!" Surprise attack. |
| **33** | **JumpScare** | **BOO!** Sudden loud noise and red light. |
| **34** | **Sad Apology** | "I am sorry." Head down. |
| **35** | **Switch OFF** | "Shutting down." Everything off. |
| **36** | **Magic Portal** | "Entering the void." Swirling lights. |
| **37** | **Taunting** | "Try again loser." Head shake. |
| **38** | **Game Won** | Victory fanfare animation. |
| **39** | **Game Lost** | Game over sadness. |
| **40** | **Loading 100%** | LED progress bar animation. |
| **41** | **Binary Speak** | Speaks in 0s and 1s. |
| **42** | **Shout Mode** | "CAN YOU HEAR ME NOW?" (Angry). |
| **43** | **Fake Shutoff** | Pretends to die... then "Just kidding!". |
| **44** | **Notification** | "You have one new message." |
| **45** | **Dad Joke** | Tells a bad penguin joke. |
| **46** | **Rap Mode 🔥** | Raps about Linux. |
| **47** | **Helicopter** | Wings + Spin combo. |
| **48** | **Cyber Knight** | "I serve the code." Blue stance. |
| **49** | **DJ Mode** | "Drop the beat!" Club lights. |
| **50** | **Grand Closing** | The goodbye show. |

---

## 🎵 Music Player (DJ Mode)
Play MP3 files while Tux dances automatically.

| Command | Example | Requirement |
| :--- | :--- | :--- |
| **Play** | `./run.sh --play "music/song.mp3"` | Requires `mpg123` installed. |

> **Setup:** Run `sudo apt install mpg123` on the Tux Droid host to enable this feature.

---

## 🛠️ Diagnostics
| Command | Description |
| :--- | :--- |
| `./run.sh --spin-doctor` | Tests motor at various durations. |
| `./run.sh --list` | Quick check if USB is active. |

---
**Enjoy your Tux Droid!** 🐧
