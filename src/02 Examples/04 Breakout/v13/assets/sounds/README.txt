Breakout – original synthetisierte Retro-Sounds

start.ogg     Freundliches Startmenue, 120 BPM, 16 Sekunden
play.ogg      Tiefer, weicher Arcade-Loop, 150 BPM, 12,8 Sekunden
pause.ogg     Schwebende Dur-Akkorde ohne Schlagzeug, 72 BPM, ca. 26,67 Sekunden
help.ogg      Helle, rhythmische Retro-Arpeggien, 128 BPM, 15 Sekunden
gameover.ogg  Langsame Moll-Akkorde und fallende Melodie, 64 BPM, 30 Sekunden
levelup.ogg   Sehr froehliche aufsteigende Dur-Fanfare, 2,8 Sekunden, einmal abspielen
wall.ogg      Kurzer hoher Abpraller
paddle.ogg    Aufwaerts gerichteter Paddle-Effekt
brick.ogg     Zerbrechender Arcade-Ziegel

Alle Dateien: OGG Vorbis, 44.100 Hz, Stereo.
Die fuenf Musikstuecke umfassen jeweils acht vollstaendige 4/4-Takte.
Samplegenaue Loops ohne eingefuegte Stille; reale Wiedergabe haengt vom Player ab.
Retro-Klang durch synthetische Puls-/Dreieckwellen und Rauschen.
Keine fremden Aufnahmen, Samples oder Melodien verwendet.
Diese eigens erzeugten Audiodateien duerfen frei verwendet, veraendert
und weitergegeben werden, auch kommerziell; Namensnennung ist nicht erforderlich.

Pygame:
pygame.mixer.music.load("play.ogg")
pygame.mixer.music.play(-1)
wall = pygame.mixer.Sound("wall.ogg")
wall.play()

generate_breakout_audio.py enthaelt den Generator (benoetigt numpy und soundfile).
validation.json enthaelt die Ergebnisse der Dekodierungspruefung.

balllost.ogg  Kurze fallende Moll-Tonfolge bei Ballverlust, 0,72 Sekunden, einmal abspielen.
