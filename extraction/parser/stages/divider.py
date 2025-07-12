import re

from config import SECTION_BREAK_IDENTIFIER, INCLUDE_ARCHIVED_LINES


class Divider:
    def __init__(self, filepath, sections, identifiers):
        self.filepath = filepath
        self.identifiers = identifiers

        self.split_content = { section : [] for section in sections }

    def divide(self):
        with open(self.filepath, 'r') as file:
            current_section = None
            for line in file:
                if SECTION_BREAK_IDENTIFIER in line:
                    for identifier, section in self.identifiers.items():
                        if identifier in line:
                            current_section = section
                            break
                    continue # skip to the next line
                
                if not current_section:
                    continue
                
                if re.match(r'^\s*%', line):
                    if not INCLUDE_ARCHIVED_LINES:
                        continue
                    else: 
                        line = line.split('%')[1]

                self.split_content[current_section].append(line.strip())

        return self.split_content