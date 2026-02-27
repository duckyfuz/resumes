import re
from abc import ABC, abstractmethod

from logger_config import get_logger
logger = get_logger(__name__)


class BasicParser(ABC):
    replace_set = [
        '\\', 
        'textbf{', 'large{', 'underline{', 'textit{', 'emph{',
        'resumeSubheading{', 'resumeDescription{', 'resumeItem{', 'resumeProjectHeading{',
        '}', '{',
        ':'
    ]

    @abstractmethod
    def parse(self, content):
        pass

    def sanitize(self, line):
        for item in self.replace_set:
            line = line.replace(item, '')
        return line.strip()


class HeadingParser(BasicParser):
    def __init__(self, content):
        self.content = content
        
    def parse(self):
        # NOTE: this is hardcoded as there are only 2 useful lines
        name, mail_link, site_link = re.split(r'\s*(?:\$\|\$|&)\s*', self.content[1])
        linkedin, github, phone = self.content[2].split('$|$')

        return {
            "email": self.sanitize(mail_link.split('}{')[1]),
            "github": self.sanitize(github.split('}{')[1]),
            "linkedin": self.sanitize(linkedin.split('}{')[1]),
            "name": self.sanitize(name),
            "phone": self.sanitize(phone),
            "website": self.sanitize(site_link.split('}{')[1]),
        }


class EducationParser(BasicParser):
    def __init__(self, content):
        self.content = content
        
    def parse(self):
        res = []
        for line in self.content:
            if line.startswith('\\resumeSubheading{'):  # title line
                res.append({
                    "company": self.sanitize(line.split('}{')[0]),
                    "dates": self.sanitize(line.split('}{')[1]),
                })
            elif line.startswith('\\resumeDescription{'):
                res[-1]["description"] = self.sanitize(line.replace('$|$', '|'))
        return res


class ExperienceParser(BasicParser):
    def __init__(self, content):
        self.content = content
        
    def parse(self):
        res = []
        for line in self.content:
            if line.startswith('\\resumeSubheading{'):
                role, company, dates = re.split(r'\s*(?:}{|@)\s*', line)
                res.append({
                    "role": self.sanitize(role),
                    "company": self.sanitize(company),
                    "dates": self.sanitize(dates),
                    "items": []
                })
            if line.startswith('\\resumeDescription{'):
                res[-1]["description"] = self.sanitize(line)
            if line.startswith('\\resumeItem{'):
                res[-1]["items"].append(self.sanitize(line))
        return res


class ProjectsParser(BasicParser):
    def __init__(self, content):
        self.content = content
        
    def parse(self):
        res = []
        for line in self.content:
            if line.startswith('\\resumeSubheading{'):
                name, description_and_dates = line.split('$|$', 1)
                description, dates = description_and_dates.rsplit('}{', 1)
                res.append({
                    "name": self.sanitize(name),
                    "description": self.sanitize(description),
                    "dates": self.sanitize(dates),
                    "items": []
                })
            if line.startswith('\\resumeItem{'):
                res[-1]["items"].append(self.sanitize(line))
        return res


class AwardsParser(BasicParser):
    def __init__(self, content):
        self.content = content
        
    def parse(self):
        res = []
        for line in self.content:
            if line.startswith('\\resumeProjectHeading{'):
                awards = line.split('$|$')
                for award in awards:
                    event, achievement = award.split(' - ', 1)
                    res.append({
                        "event": self.sanitize(event),
                        "achievement": self.sanitize(achievement)
                    })
        return res


class TechnicalSkillsParser(BasicParser):
    def __init__(self, content):
        self.content = content
        
    def parse(self):
        res = {}
        for line in self.content:
            if line.startswith('\\textbf{'):
                key, entries = line.split('}{', 1)
                res[self.sanitize(key)] = [self.sanitize(entry) for entry in entries.split(',')]
        return res


class ParserFactory:
    parser_map = {
        "heading": HeadingParser,
        "education": EducationParser,
        "experience": ExperienceParser,
        "projects": ProjectsParser,
        "awards": AwardsParser,
        "technical_skills": TechnicalSkillsParser,
    }

    @staticmethod
    def get_parser(parser_type, content):
        if parser_type not in ParserFactory.parser_map.keys():
            raise KeyError(f"Parser type '{parser_type}' is not recognized.")

        return ParserFactory.parser_map[parser_type](content)
