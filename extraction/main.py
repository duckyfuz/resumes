import os 
import sys

from logger_config import get_logger
logger = get_logger(__name__)

from parser.pipeline import ProcessingPipeline


def main(filepath):
    pipeline = ProcessingPipeline(
        filepath=filepath,
        sections=['heading', 'education', 'experience', 'projects', 'awards', 'technical_skills'],
    )
    pipeline.execute()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        logger.error('filepath not provided')
        sys.exit()

    filepath = os.path.abspath(sys.argv[1])
    if not os.path.exists(filepath):
        logger.error(f'file not found: {filepath}')
        sys.exit()
    logger.info(f'parsing file: {filepath}')

    main(filepath)
