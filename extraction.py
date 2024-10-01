file_path = "/Users/ken/Developer/resumes/kennethgao_resume.tex"

ordered_sections = [
    "Experience",
    "Education",
    "Projects / Extracurriculars",
    "Awards",
    "Technical Skills",
]
begin_sections = {"\\section{" + section + "}": section for section in ordered_sections}
current_section = None
resume_data = {section: [] for section in ordered_sections}

with open(file_path, "r") as file:
    for line in file:
        line = line.strip()
        if line in list(begin_sections.keys()):
            current_section = begin_sections[line]
        if current_section is None:
            continue
        if line.startswith("\\") or line.startswith("{"):
            resume_data[current_section].append(line)

processed_resume_data = {section: [] for section in ordered_sections}


def handle_experience(data: list):
    item = {}
    to_skip = ["\\section", "\\resumeSubHeadingListStart"]
    i = 0
    while i < len(data):
        line = data[i]
        if any(line.startswith(skip) for skip in to_skip):
            i += 1
            continue
        if line.startswith("\\resumeSubHeadingListEnd"):
            if item:
                processed_resume_data["Experience"].append(item)
            break
        if line.startswith("\\resumeSubheading"):
            if item:
                processed_resume_data["Experience"].append(item)
            item = {}
            i += 1
            item["title"], item["duration"] = data[i].strip("{}").split("}{")
            i += 1
            item["company"], item["region"] = data[i].strip("{}").split("}{")
        elif line.startswith("\\resumeDescription"):
            item["description"] = line.replace("\\resumeDescription{", "").rstrip("}")
        elif line.startswith("\\resumeItemListStart"):
            item["items"] = []
            i += 1
            while not data[i].startswith("\\resumeItemListEnd"):
                item["items"].append(data[i].replace("\\resumeItem{", "").rstrip("}"))
                i += 1
        i += 1


def handle_education(data: list):
    item = {}
    to_skip = ["\\section", "\\resumeSubHeadingListStart"]
    i = 0
    while i < len(data):
        line = data[i]
        if any(line.startswith(skip) for skip in to_skip):
            i += 1
            continue
        if line.startswith("\\resumeSubHeadingListEnd"):
            if item:
                processed_resume_data["Education"].append(item)
            break
        if line.startswith("\\resumeSubheading"):
            if item:
                processed_resume_data["Education"].append(item)
            item = {}
            i += 1
            item["institution"], item["region"] = data[i].strip("{}").split("}{")
            i += 1
            item["title"] = data[i].strip("{}").split("}{")
        i += 1


def handle_projects(
    data: list,
):  # FIXME: not working for differently formatted projects
    item = {}
    to_skip = ["\\section", "\\resumeSubHeadingListStart"]
    i = 0
    while i < len(data):
        line = data[i]
        if any(line.startswith(skip) for skip in to_skip):
            i += 1
            continue
        if line.startswith("\\resumeSubHeadingListEnd"):
            if item:
                processed_resume_data["Projects / Extracurriculars"].append(item)
            break
        if line.startswith("\\resumeProjectHeading"):
            if item:
                processed_resume_data["Projects / Extracurriculars"].append(item)
            item = {}
            i += 1
            item["title"], item["duration"] = data[i].strip("{}").split("}{")
        elif line.startswith("\\resumeItemListStart"):
            item["items"] = []
            i += 1
            while not data[i].startswith("\\resumeItemListEnd"):
                item["items"].append(data[i].replace("\\resumeItem{", "").rstrip("}"))
                i += 1
        i += 1


def handle_awards(data: list):
    item = {}
    to_skip = ["\\section", "\\resumeSubHeadingListStart"]
    i = 0
    while i < len(data):
        line = data[i]
        if any(line.startswith(skip) for skip in to_skip):
            i += 1
            continue
        if line.startswith("\\resumeSubHeadingListEnd"):
            if item:
                processed_resume_data["Awards"].append(item)
            break
        if line.startswith("\\resumeProjectHeading"):
            if item:
                processed_resume_data["Awards"].append(item)
            item = {}
            item["awards"] = (
                line.replace("\\resumeProjectHeading{", "").rstrip("}").split(" $|$ ")
            )
        i += 1


def handle_technical_skills(data: list):
    skills = {}
    for line in data:
        if line.startswith("\\textbf"):
            print(line)
            category, items = (
                line.replace("\\textbf{", "").rstrip("\\\\").rstrip("} ").split("}{")
            )
            skills[category.rstrip(": ")] = items.split(", ")
    processed_resume_data["Technical Skills"].append(skills)


handle_experience(resume_data["Experience"])
handle_education(resume_data["Education"])
handle_projects(resume_data["Projects / Extracurriculars"])
handle_awards(resume_data["Awards"])
handle_technical_skills(resume_data["Technical Skills"])


print(processed_resume_data)
