from pathlib import Path
import sys, json, zipfile, threading, runpy, shutil
if __name__ == '__main__':
    threading.stack_size(16 * 1024 * 1024)
    worker = threading.Thread(target=lambda: runpy.run_path(__file__, run_name='audio_worker'))
    worker.start()
    worker.join()
    sys.exit(0)
sys.path.insert(0, str(Path(__file__).parent / '.audio-libs'))
import numpy as np
import soundfile as sf

OUT = Path(__file__).parent / 'breakout-audio-v2'
OUT.mkdir(exist_ok=True)
for unchanged in ('start', 'wall', 'paddle', 'brick'):
    shutil.copyfile(OUT.parent/'breakout-audio'/(unchanged+'.ogg'), OUT/(unchanged+'.ogg'))
SR = 44100
rng = np.random.default_rng(20261018)

def tone(freq, duration, kind='pulse', release=.025):
    n = int(round(duration * SR))
    t = np.arange(n) / SR
    if kind == 'soft':
        y = np.sin(2*np.pi*freq*t) + .12*np.sin(2*np.pi*freq*2*t)
    elif kind == 'triangle':
        y = sum((-1)**((h-1)//2) * np.sin(2*np.pi*h*freq*t)/h**2 for h in range(1, 16, 2))
    else:
        y = sum(np.sin(2*np.pi*h*freq*t)/h for h in range(1, min(20, int(18000/freq)), 2))
    env = np.minimum(1, t/(.035 if kind=='soft' else .004)) * np.minimum(1, (n-1-np.arange(n))/max(1, release*SR))
    return y * env * .7

def hz(note): return 440 * 2**((note-69)/12)

def add(dst, wave, start, gain=1, pan=0):
    idx = (np.arange(len(wave)) + int(round(start*SR))) % len(dst)
    np.add.at(dst[:,0], idx, wave * gain * np.sqrt((1-pan)/2))
    np.add.at(dst[:,1], idx, wave * gain * np.sqrt((1+pan)/2))

def drum(kind):
    t = np.arange(int(.13*SR))/SR
    if kind == 'kick': return np.sin(2*np.pi*(48*t + 9*(1-np.exp(-t*45)))) * np.exp(-t*35) * np.minimum(t/.002, 1)
    return rng.uniform(-1,1,len(t)) * np.exp(-t*(85 if kind=='hat' else 32)) * np.minimum(t/.001,1)

configs = {
 'start': (120, [60,65,67,60,69,65,67,60], [0,4,7,12,7,4,2,7], 'pulse', .8),
 'play': (150, [57,53,60,55,57,53,55,57], [0,7,12,10,7,3,5,7], 'pulse', 1),
 'pause': (90, [60,57,65,67,60,57,65,67], [7,12,4,7,9,4,2,7], 'triangle', .25),
 'help': (108, [65,60,62,67,65,60,67,60], [0,4,7,4,2,5,9,7], 'triangle', .45),
 'gameover': (96, [57,53,50,52,57,53,52,52], [12,7,3,0,10,7,3,2], 'pulse', .4),
}
report = {}
def save(name, audio):
    audio *= .78 / max(float(np.max(np.abs(audio))), .001)
    path = OUT / (name+'.ogg')
    sf.write(path, audio, SR, format='OGG', subtype='VORBIS')
    decoded, rate = sf.read(path, always_2d=True)
    assert len(decoded)==len(audio) and rate==SR and np.isfinite(decoded).all()
    assert np.max(np.abs(decoded)) < 1
    report[name] = {'seconds': round(len(decoded)/rate, 4), 'frames': len(decoded),
                    'peak': round(float(np.max(np.abs(decoded))),4),
                    'boundary_jump': round(float(np.max(np.abs(decoded[-1]-decoded[0]))),6),
                    'format': sf.info(path).subtype}

for name, (bpm, roots, melody, kind, energy) in configs.items():
    if name == 'start':
        continue
    if name in ('pause', 'gameover'):
        bpm = 72 if name == 'pause' else 64
        roots = [48,55,53,48,48,55,53,55] if name=='pause' else [45,41,38,40,45,41,38,40]
    elif name == 'help':
        bpm = 128
    # Integer beat lengths keep the loop grid sample-exact.
    beat_frames = round(SR*60/bpm)
    beat = beat_frames/SR
    audio = np.zeros((beat_frames*32,2))
    if name in ('pause', 'gameover'):
        sad = name == 'gameover'
        # Slow sustained harmony, no percussion; the minor melody descends.
        lead = [76,72,71,68,72,69,65,64] if sad else [72,79,76,74,72,79,76,74]
        for bar, root in enumerate(roots):
            for interval in (0,3 if sad else 4,7,14 if not sad else 12):
                add(audio, tone(hz(root+interval), beat*4.5, 'soft', .65), bar*4*beat, .11, (interval-6)/20)
            add(audio, tone(hz(lead[bar]), beat*(3.3 if sad else 2), 'triangle' if sad else 'soft', .45), (bar*4+.25)*beat, .16)
            if sad:
                add(audio, tone(hz(lead[bar]-2), beat*.8, 'triangle', .2), (bar*4+3.3)*beat, .10)
        save(name, audio)
        continue
    if name == 'play':
        # Low, sustained tonal lines, no sweeps or noisy attacks like the SFX.
        for bar, root in enumerate(roots):
            for step, interval in enumerate([0,3,7,5]):
                add(audio, tone(hz(root+interval), beat*.88, 'soft', .09), (bar*4+step)*beat, .23, -.15)
                add(audio, tone(hz(root-12), beat*.85, 'triangle', .07), (bar*4+step)*beat, .22)
                add(audio, drum('kick'), (bar*4+step)*beat, .06)
            for interval in (0,3,7):
                add(audio, tone(hz(root-12+interval), beat*3.9, 'soft', .15), bar*4*beat, .055, .3)
        save(name, audio)
        continue
    for bar, root in enumerate(roots):
        for step in range(8):
            at = (bar*4+step*.5)*beat
            note = root + 12 + melody[(step+bar*2)%8]
            add(audio, tone(hz(note), beat*.38, kind), at, .21, -.18)
            chord = [0, 3 if name in ('play','gameover') else 4, 7, 12]
            add(audio, tone(hz(root+chord[step%4]), beat*.30, 'triangle'), at, .11, .35)
        for b in range(4):
            at = (bar*4+b)*beat
            add(audio, tone(hz(root-24+(7 if b==3 else 0)), beat*.72, 'triangle'), at, .30)
            if b%2==0: add(audio, drum('kick'), at, .18*energy)
            else: add(audio, drum('snare'), at, .09*energy, .1)
            add(audio, drum('hat'), at+beat*.5, .045*energy, -.3)
    save(name, audio)

for name, f0, f1, duration in []:  # Keep the original effects byte-for-byte.
    t = np.arange(round(duration*SR))/SR
    phase = 2*np.pi*(f0*t + (f1-f0)*t*t/(2*duration))
    y = (np.sin(phase)+.25*np.sin(3*phase)) * np.exp(-t/(duration*.3))
    if name=='brick': y += .28*rng.uniform(-1,1,len(t))*np.exp(-t*32)
    y *= np.minimum(t/.002,1)*np.minimum((duration-t)/.012,1)
    save(name, np.column_stack([y,y]))

fanfare = np.zeros((round(2.8*SR), 2))
for at, note, dur in [(0,72,.14),(.16,76,.14),(.32,79,.14),(.48,84,.26),(.80,79,.14),(.96,84,.14),(1.12,88,.18),(1.36,91,.85)]:
    add(fanfare, tone(hz(note), dur, 'pulse', .08), at, .22, -.15)
    add(fanfare, tone(hz(note-12), dur, 'triangle', .08), at, .18, .15)
for note in (60,64,67,72):
    add(fanfare, tone(hz(note), 1.15, 'triangle', .4), 1.36, .15)
save('levelup', fanfare)
for unchanged in ('start','wall','paddle','brick'):
    data, rate = sf.read(OUT/(unchanged+'.ogg'), always_2d=True)
    assert rate == SR and np.isfinite(data).all() and np.max(np.abs(data)) < 1
    report[unchanged] = {'seconds':len(data)/rate, 'unchanged':True}
(OUT/'validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
(OUT/'README.txt').write_text('''Breakout – original synthetisierte Retro-Sounds

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
''', encoding='utf-8')
with zipfile.ZipFile(OUT.parent/'breakout-audio-v2.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in OUT.iterdir(): z.write(p, p.name)
    z.write(Path(__file__), 'generate_breakout_audio.py')
print(json.dumps(report, indent=2))
