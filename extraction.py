import re
import json
from collections import defaultdict


def extract_header(lines):
    header = {}
    availability_pattern = re.compile(r'\\textbf{Availability: }(.*?)(\\\\|$)')
    href_pattern = re.compile(r'\\href{([^}]+)}{([^}]+)}')
    phone_pattern = re.compile(r'{([+0-9 ]+)}')

    for i, line in enumerate(lines):
        if '\\begin{tabular*}' in line:
            line1 = lines[i+1].strip()
            line2 = lines[i+2].strip()
            
            # Extract name
            name_match = re.search(r'\\textbf{\\href{[^}]+}{\\Large\\s*([^}]+)}}', line1)
            if name_match:
                header['name'] = name_match.group(1).strip()
            
            # Extract email, website
            hrefs = href_pattern.findall(line1)
            for url, text in hrefs:
                if 'mailto:' in url:
                    header['email'] = url.split('mailto:')[1]
                else:
                    if 'website' not in header:
                        header['website'] = url
            
            # Extract availability
            avail_match = availability_pattern.search(line1)
            if avail_match:
                header['availability'] = avail_match.group(1).strip()
            
            # Process second line
            hrefs_line2 = href_pattern.findall(line2)
            for url, text in hrefs_line2:
                if 'linkedin.com' in text:
                    header['linkedin'] = url
                elif 'github.com' in text:
                    header['github'] = url
            
            phone_match = phone_pattern.search(line2)
            if phone_match:
                header['phone'] = phone_match.group(1).strip()
            
            break
    return header


def preprocess_line(line): # TODO: remove this bandaid
    replacements = [
        ('\\%', '%'),
        ('\\&', '&')
    ]
    for old, new in replacements:
        line = line.replace(old, new)
    return line
    

def extract_section(lines, section_name, start_idx):
    entries = []
    i = start_idx
    while i < len(lines):
        line = preprocess_line(lines[i].strip())

        if line.startswith('% END OF SECTION'): break

        if line.startswith('\\resumeSubheading'):
            entry = {}
            formatting_to_remove = ['\\resumeSubheading{', '\\textbf{', '\\textit{']
            for formatting in formatting_to_remove:
                line = line.replace(formatting, '')
            title_part, date_part = [part.replace('{', '').replace('}', '') for part in line.split('}{')]
            
            # Handle company formatting with \textit
            if '@' in title_part:
                role, company = title_part.split('@', 1)
                entry['role'] = role.strip()
                company = re.sub(r'\\textit{([^}]+)}', r'\1', company.strip())
                entry['company'] = company.strip()
            else:
                entry['company'] = re.sub(r'\\textit{([^}]+)}', r'\1', title_part.strip())
            
            entry['dates'] = date_part
            
            # Process description
            i += 1
            desc_line = preprocess_line(lines[i].strip())
            desc_match = re.search(r'\\resumeDescription{([^}]+)}', desc_line)
            if desc_match:
                entry['description'] = desc_match.group(1).strip()
            
            # Process items
            entry['items'] = []
            i += 1
            if i < len(lines) and 'resumeItemListStart' in lines[i]:
                i += 1
                while i < len(lines) and 'resumeItemListEnd' not in lines[i]:
                    item_line = lines[i].strip()
                    if item_line.startswith('%'):
                        i += 1
                        continue
                    item_match = re.search(r'\\resumeItem{([^}]+)}', item_line)
                    if item_match:
                        entry['items'].append(preprocess_line(item_match.group(1).strip()))
                    i += 1
            entries.append(entry)
        i += 1
    return entries, i


def extract_projects(lines, start_idx):
    projects = []
    i = start_idx
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('% END OF SECTION'): break

        if line.startswith('\\resumeSubheading'):
            project = {}
            
            formatting_to_remove = ['\\resumeSubheading{', '\\textbf{', '\\textit{']
            for formatting in formatting_to_remove:
                line = line.replace(formatting, '')
            name_desc_part, dates = [part.replace('{', '').replace('}', '') for part in line.rsplit('}{', 1)]
            name_part, desc_part = [part.strip() for part in name_desc_part.split("$|$", 1)]
            
            # Extract URL from description if present
            url_match = re.search(r'\\href{([^}]+)}{([^}]+)}', desc_part)
            if url_match:
                project['url'] = url_match.group(1).strip()
                desc_part = desc_part.replace(url_match.group(0), '').strip(' -')
            
            project['name'] = name_part
            project['description'] = desc_part.replace('\\href', '')
            project['dates'] = dates
            
            # Process items
            project['items'] = []
            i += 1
            if i < len(lines) and 'resumeItemListStart' in lines[i]:
                i += 1
                while i < len(lines) and 'resumeItemListEnd' not in lines[i]:
                    item_line = lines[i].strip()
                    item_match = re.search(r'\\resumeItem{([^}]+)}', item_line)
                    if item_match:
                        project['items'].append(item_match.group(1).strip())
                    i += 1
            projects.append(project)
        i += 1
    return projects, i


def extract_awards(lines, start_idx):
    awards = []
    i = start_idx
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('% END OF SECTION'): break

        if line.startswith('\\resumeProjectHeading{'):
            # award_line = re.search(r'\\resumeProjectHeading{([^}]+)}', line)

            # parts = re.split(r'\s*\\$\\|\\$\s*', award_line.group(1))
            formatting_to_remove = ['\\resumeProjectHeading{', '\\resumeSubheading{', '\\emph,' '\\textbf{', '\\textit{']
            for formatting in formatting_to_remove:
                line = line.replace(formatting, '')
            parts = [preprocess_line(part).replace('{', '').replace('}', '').strip() for part in line.split("$|$")]
            
            for part in parts:
                part = part.strip()
                if ' - ' in part:
                    event, achievement = part.split(' - ', 1)
                    event = re.sub(r'\\textbf{([^}]+)}', r'\1', event).strip()
                    event = re.sub(r'\\emph{([^}]+)}', r'\1', event).strip().replace('\\textbf', '')
                    achievement = re.sub(r'\\emph{([^}]+)}', r'\1', achievement).replace('\\emph', '').strip()
                    awards.append({
                        'event': event,
                        'achievement': achievement
                    })
        i += 1
    return awards, i


def extract_technical_skills(lines, start_idx):
    skills = defaultdict(list)
    i = start_idx
    in_itemize = False
    current_items = []
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('\\begin{itemize}'):
            in_itemize = True
            i +=1
            continue
        if line.startswith('\\end{itemize}'):
            in_itemize = False
            i +=1
            break
        if in_itemize:
            lines_content = [s.strip() for s in line.split('\\\\')]
            for l in lines_content:
                if l:
                    parts = l.split(':', 1)
                    if len(parts) == 2:
                        category = parts[0].replace('\\textbf', '').strip('{} ')
                        skills_list = [s.replace('{', '').replace('}', '').strip() for s in parts[1].split(',')]
                        skills[category] = skills_list
        i +=1
    return dict(skills), i


def parse_latex_to_json(lines):
    resume_data = {
        'header': {},
        'education': [],
        'experience': [],
        'projects': [],
        'awards': [],
        'technical_skills': {}
    }
    
    resume_data['header'] = extract_header(lines)
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('%'):
            i += 1
            continue
        if line.startswith('\\section{Education}'):
            print("📚 Extracting Education Section...")
            education, i = extract_section(lines, 'Education', i+1)
            resume_data['education'] = education
        elif line.startswith('\\section{Experience}'):
            print("💼 Extracting Experience Section...")
            experience, i = extract_section(lines, 'Experience', i+1)
            resume_data['experience'] = experience
        elif line.startswith('\\section{Projects / Extracurriculars}'):
            print("📂 Extracting Projects Section...")
            projects, i = extract_projects(lines, i+1)
            resume_data['projects'] = projects
        elif line.startswith('\\section{Awards}'):
            print("🏆 Extracting Awards Section...")
            awards, i = extract_awards(lines, i+1)
            resume_data['awards'] = awards
        elif line.startswith('\\section{Technical Skills}'):
            print("🛠 Extracting Technical Skills Section...")
            technical_skills, i = extract_technical_skills(lines, i+1)
            resume_data['technical_skills'] = technical_skills
        i += 1
    
    return resume_data


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    with open(args.input, 'r') as f:
        lines = f.readlines()
    
    resume_json = parse_latex_to_json(lines)
    
    with open(args.output, 'w') as f:
        json.dump(resume_json, f, indent=2)


if __name__ == '__main__':
    main()
