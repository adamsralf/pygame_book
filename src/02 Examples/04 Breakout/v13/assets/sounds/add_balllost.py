from pathlib import Path
import sys, threading, runpy, json, zipfile
if __name__ == '__main__':
    threading.stack_size(16*1024*1024)
    thread = threading.Thread(target=lambda: runpy.run_path(__file__, run_name='audio_worker'))
    thread.start()
    thread.join()
    sys.exit(0)
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT/'.audio-libs'))
import numpy as np
import soundfile as sf
OUT = ROOT/'breakout-audio-v2'
sr = 44100
audio = np.zeros(round(.72*sr))
# Four falling minor notes: immediately recognizable, brief enough for gameplay.
for start, freq, duration, gain in [(0,523.25,.14,.65),(.12,415.30,.15,.60),(.25,311.13,.17,.55),(.40,196,.28,.50)]:
    t = np.arange(round(duration*sr))/sr
    wave = np.sin(2*np.pi*freq*t)+.20*np.sin(2*np.pi*3*freq*t)
    envelope = np.minimum(t/.003,1)*np.minimum((duration-t)/.045,1)*np.exp(-t*4)
    offset = round(start*sr)
    audio[offset:offset+len(t)] += gain*wave*envelope
audio *= .70/np.max(np.abs(audio))
path = OUT/'balllost.ogg'
sf.write(path, np.column_stack([audio,audio]), sr, format='OGG', subtype='VORBIS')
decoded, rate = sf.read(path, always_2d=True)
assert rate==sr and len(decoded)==len(audio) and np.isfinite(decoded).all()
assert np.max(np.abs(decoded)) < 1
report = json.loads((OUT/'validation.json').read_text(encoding='utf-8'))
report['balllost'] = {'seconds':len(decoded)/rate, 'peak':float(np.max(np.abs(decoded))), 'format':sf.info(path).subtype}
(OUT/'validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
readme = OUT/'README.txt'
content = readme.read_text(encoding='utf-8')
if 'balllost.ogg' not in content:
    readme.write_text(content+'\nballlost.ogg  Kurze fallende Moll-Tonfolge bei Ballverlust, 0,72 Sekunden, einmal abspielen.\n', encoding='utf-8')
with zipfile.ZipFile(ROOT/'breakout-audio-v3.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for file in OUT.iterdir(): archive.write(file, file.name)
    archive.write(ROOT/'generate_breakout_audio.py', 'generate_breakout_audio.py')
    archive.write(Path(__file__), 'add_balllost.py')
print(json.dumps(report['balllost']))
