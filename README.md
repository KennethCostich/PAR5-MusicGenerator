# PAR-5: LSTM-CSP Music Composition 🎶

This will review how to use the program. For an overview of how the algorithms work, read over our paper.

Unfortunately, incorperating the LSTM into our full pipeline is out of the scope of this current iteration and will be implemented in later versions. For now, we have provided example monophonic melodies in **data/** to run PAR-5 on.

To start, install the libraries **pretty_midi** and **music21**. Here is how to do it using pip:
	
~~~~
pip install music21
pip install pretty_midi
~~~~

If you do not have pip, you can find installation for music21 at https://web.mit.edu/music21/doc/installing/index.html and pretty_midi at https://github.com/craffel/pretty-midi.

Next, find a piece from the **/data** directory that you enjoy and find out what key it is in (use that musical prowess we all know you have!). Once you have recognized the key, get the file path of the melody you selected.

You can then run this command to generate an accompaniment for the melody:

~~~~
python main.py --file_path 'data/1.mid' --key 'Bm'
~~~~

Where **--file_path** specifies the desired monophonic melody to compose on and **--key** specifies the key of the piece.

When inputing the key, follow these four rules:
1. Capitalize the note.
2. Lower case for the flat.
3. Only use flat keys.
4. If it is minor, add an 'm' at the end.

For example, **A flat minor** would be **Abm** or **C sharp** would be **Db**.
We do not use sharps here, as they are for ***squares***.

If you're feeling less adventurous, you can find finished songs in the **examples/** directory. Simply open them up with any MIDI capable application such as **MuseScore** (https://musescore.org/).

If you have any questions, do not hesitate to reach us at salvadore.m@northeastern.edu or costich.k@northeastern.edu.