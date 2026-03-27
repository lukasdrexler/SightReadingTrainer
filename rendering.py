import subprocess
from music21 import stream, note


def render_note(note_string):
    # Create a stream (container for musical elements)
    s = stream.Stream()

    # Add a single C4 quarter note to the stream
    n = note.Note(note_string)
    #n = note.Note(note_string)
    n.quarterLength = 1  # Set the duration to a quarter note
    s.append(n)

    # Define the output LilyPond file path
    lilypond_path = 'pdfs/{}.ly'.format(note_string)

    # Write the musical score to a LilyPond (.ly) file
    s.write('lilypond', fp=lilypond_path)

    # Customizing the .ly file to omit the time signature and set the page layout
    with open(lilypond_path, 'a') as f:
        f.write('''
    \\layout {
      \\context {
        \\Score
        \\remove "Time_signature_engraver" % Remove the time signature
      }
    }

    \\paper {
      #(set-paper-size "a6landscape")
      indent = 0\\mm
      line-width = 50\\mm
      top-margin = 10\\mm
      bottom-margin = 10\\mm
      left-margin = 10\\mm
      right-margin = 10\\mm
      oddHeaderMarkup = ##f
      evenHeaderMarkup = ##f
      oddFooterMarkup = ##f
      evenFooterMarkup = ##f
    }
    ''')

    # Compile the .ly file to a PDF using LilyPond
    subprocess.run(['lilypond', lilypond_path])

    print(f"PDF saved at: note.pdf")


if __name__ == '__main__':

    notes = ['F3', 'F#3',
         'Gb3', 'G3', 'G#3', 'Ab3', 'A3', 'A#3', 'Bb3', 'B3','C4', 'C#4', 'Db4', 'D4', 'D#4', 'Eb4', 'E4', 'F4', 'F#4',
         'Gb4', 'G4', 'G#4', 'Ab4', 'A4', 'A#4', 'Bb4', 'B4', 'C5', 'C#5', 'Db5', 'D5', 'D#5', 'Eb5', 'E5', 'F5', 'F#5',
         'Gb5', 'G5', 'G#5', 'Ab5', 'A5', 'A#5', 'Bb5', 'B5', 'C6']


    for notestr in notes:
        render_note(notestr)
