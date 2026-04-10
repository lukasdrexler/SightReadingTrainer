import os
import subprocess
from music21 import stream, note, key



def render_note(note_string, key_name, output_dir="pdfs"):
    s = stream.Stream()
    s.append(key.Key(key_name))

    n = note.Note(note_string)
    n.quarterLength = 1
    s.append(n)

    key_dir = os.path.join(output_dir, key_name.replace(" ", "_"))
    os.makedirs(key_dir, exist_ok=True)

    base_name = f"{note_string}"
    lilypond_path = os.path.join(key_dir, f"{base_name}.ly")
    output_base = os.path.join(key_dir, base_name)

    s.write("lilypond", fp=lilypond_path)

    with open(lilypond_path, "a") as f:
        f.write(r'''
\layout {
  \context {
    \Score
    \remove "Time_signature_engraver"
  }
}

\paper {
  #(set-paper-size "a6landscape")
  indent = 0\mm
  line-width = 50\mm
  top-margin = 10\mm
  bottom-margin = 10\mm
  left-margin = 10\mm
  right-margin = 10\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
}
''')

    subprocess.run(
        ["lilypond", "-o", output_base, lilypond_path],
        check=True
    )

    print(f"PDF saved at: {output_base}.pdf")

    for ext in [".tex", ".texi", ".count", ".eps", ".log"]:
        aux_path = output_base + ext
        if os.path.exists(aux_path):
            os.remove(aux_path)


if __name__ == '__main__':

    notes_by_key = {
        "F": ['F3', 'G3', 'A3', 'Bb3', 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'Bb4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5',
              'Bb5', 'C6'],
        "C": ['F3', 'G3', 'A3','B3', 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5',
              'C6'],
        "G": ['F#3', 'G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F#4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F#5', 'G5', 'A5',
              'B5', 'C6'],
        "D": ['F#3', 'G3', 'A3', 'B3', 'C#4','D4', 'E4', 'F#4', 'G4', 'A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'G5', 'A5',
              'B5', 'C#6'],
        "A": ['F#3', 'G#3', 'A3', 'B3', 'C#4', 'D4', 'E4', 'F#4', 'G#4', 'A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'G#5',
              'A5', 'B5', 'C#6'],
        "E": ['F#3', 'G#3', 'A3', 'B3', 'C#4', 'D#4','E4', 'F#4', 'G#4', 'A4', 'B4', 'C#5', 'D#5', 'E5', 'F#5', 'G#5',
              'A5', 'B5', 'C#6'],
        "B": ['F#3', 'G#3', 'A#3', 'B3', 'C#4', 'D#4', 'E4', 'F#4', 'G#4', 'A#4', 'B4', 'C#5', 'D#5', 'E5', 'F#5',
              'G#5', 'A#5', 'B5', 'C#6'],
        "F#": ['F#3', 'G#3', 'A#3', 'B3', 'C#4', 'D#4', 'E#4', 'F#4', 'G#4', 'A#4', 'B4', 'C#5', 'D#5', 'E#5', 'F#5',
               'G#5', 'A#5', 'B5', 'C#6'],
        "Gb": ['F3', 'Gb3', 'Ab3', 'Bb3', 'Cb4', 'Db4', 'Eb4', 'F4', 'Gb4', 'Ab4', 'Bb4', 'Cb5', 'Db5', 'Eb5', 'F5',
               'Gb5', 'Ab5', 'Bb5', 'Cb6'],
        "Db": ['F3', 'Gb3', 'Ab3', 'Bb3', 'C4', 'Db4', 'Eb4', 'F4', 'Gb4', 'Ab4', 'Bb4', 'C5', 'Db5', 'Eb5', 'F5',
               'Gb5', 'Ab5', 'Bb5', 'C6'],
        "Ab": ['F3', 'G3', 'Ab3', 'Bb3', 'C4', 'Db4', 'Eb4', 'F4', 'G4', 'Ab4', 'Bb4', 'C5', 'Db5', 'Eb5', 'F5', 'G5',
               'Ab5', 'Bb5', 'C6'],
        "Eb": ['F3', 'G3', 'Ab3', 'Bb3', 'C4', 'D4', 'Eb4', 'F4', 'G4', 'Ab4', 'Bb4', 'C5', 'D5', 'Eb5', 'F5', 'G5',
               'Ab5', 'Bb5', 'C6'],
        "Bb": ['F3', 'G3', 'A3', 'Bb3', 'C4', 'D4', 'Eb4', 'F4', 'G4', 'A4', 'Bb4', 'C5', 'D5', 'Eb5', 'F5', 'G5', 'A5',
               'Bb5', 'C6']
    }


    for key_name, notes in notes_by_key.items():
        for note_name in notes:
            render_note(note_name, key_name)
