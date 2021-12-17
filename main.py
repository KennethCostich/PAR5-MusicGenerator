import composer
import argparse

def main(file_path, key, addHarmony=True, addToms=True, addSnare=True, addKick=True, addCyms=True):
    my_midi = composer.MidiComposer(file_path, key)
    my_midi.compose(addHarmony, addToms, addSnare, addKick, addCyms)

my_parser = argparse.ArgumentParser()
my_parser.add_argument('--file_path', action='store', type=str, required=True)
my_parser.add_argument('--key', action='store', type=str, required=True)

args = my_parser.parse_args()

main(file_path=args.file_path, key=args.key)
