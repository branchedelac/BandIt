import re
import shutil
from multiprocessing import Pool
import ntpath
import os
import glob
import pretty_midi

class FileProcessor:
    def __init__(self, output_folder):
        self.saved_songs = []
        self.errors = 0
        self.num_processed = 0
        self.output_folder = output_folder
        self.guitar_codes = list(range(24, 32))

    def parse_file(self, midi_path: str) -> None:
        '''
        Given the path of a .mid file, checks if the MIDI object has guitar and
        drum, and a time signature of 4/4. If these conditions are fulfilled,
        copies the .mid file to a given output folder.
        '''
        try:
            midi_file = pretty_midi.PrettyMIDI(midi_path)

            if self.has_drum_and_guitar(midi_file.instruments) and self.is_four_by_four(
                midi_file.time_signature_changes
            ):
                filename = ntpath.split(midi_path)[1]
                shutil.copyfile(midi_path, f'{self.output_folder}/{filename}')

                # If you wanT to write a new file instead:
                # midi_file.write(f"{self.output_folder}/{filename}")

        except KeyError as ke:
            print(f"Error for {midi_path}: {ke}")
            self.errors += 1
        except AttributeError as ae:
            print(f"Error for {midi_path}: {ae}")
            self.errors += 1
        except Exception as ee:
            print(f"Error for {midi_path}: {ee}")
            self.errors += 1

    def has_drum_and_guitar(self, instruments: list) -> bool:
        '''
        Given a list of PrettyMIDI instruments, returns True if at least one
        of the instruments is a drum and at least one is a guitar.
        '''
        programs = set(i.program for i in instruments)
        is_drum = [i.is_drum for i in instruments]
        return programs.intersection(self.guitar_codes) and any(is_drum)

    def is_four_by_four(self, time_signatures: list) -> bool:
        '''
        Given a list of PrettyMIDI time signature changes, returns True if there
        is only one time signature and it is 4/4.
        '''
        return len(time_signatures) == 1 and (
            (time_signatures[0].numerator == 4)
            and (time_signatures[0].denominator == 4)
        )

    def remove_duplicates(self) -> None:
        '''
        Loops through output folder, normalizes filenamds to alphabetic only,
        and removes subseqent files with the same normalized filename as a
        previously seen one.
        '''
        title_pattern = "[^a-zA-Z]+"
        already_seen = []
        saved_files = glob.glob(f"{self.output_folder}/*.mid")
        for midi_file in saved_files:
            title = re.sub(title_pattern, "", midi_file).lower()
            if title in already_seen:
                os.remove(midi_file)
            else:
                already_seen.append(title)
        print("Total number of non-duplicate songs with drums and guitar saved:", len(already_seen))
