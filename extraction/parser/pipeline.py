import json
import pprint

from logger_config import get_logger
logger = get_logger(__name__)

from parser.stages.divider import Divider
from parser.stages.section_parsers import ParserFactory


class ProcessingPipeline:
    def __init__(self, filepath, sections):
        self.filepath = filepath
        self.sections = sections
        self.identifiers = { section.replace('_', ' ').upper() : section for section in sections }

        # self.split_content = None  # TODO: is this needed?
        self.res = {}

    def execute(self):
        divider = Divider(
            filepath=self.filepath,
            sections=self.sections,
            identifiers=self.identifiers,
        )
        self.split_content = divider.divide()
        
        for section, content in self.split_content.items():
            try:
                parser = ParserFactory.get_parser(section, content)
            except KeyError:
                logger.warning(f'parser not implemented for section: {section}')
                continue
            
            self.res[section] = parser.parse()
            # pprint.pprint(self.res[section], indent=2, width=100)

        output_file = self.filepath.replace('.tex', '.json')
        with open(output_file, 'w') as f:
            json.dump(self.res, f, indent=2)
        logger.info(f"Results saved to {output_file}")
