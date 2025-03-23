# Resume Hosting on AWS S3

Tired of reuploading your most updated resume to Google Drive every time you apply to a new internship? Then this is the project for you! In just 10 minutes, you can create a SSOT for your resume and portfolio website.

## Features

- Based off [Jake's Resume Template](https://www.overleaf.com/latex/templates/jakes-resume/syzfjbzwjncs), with way too many edits
- Automatically convert .tex file into JSON, perfect for keeping your portfolio site's information up to date - just fetch from https://your.domain.here/export.json

## Getting Started

1. Clone this repository:

```bash
git clone https://github.com/duckyfuz/resumes.git
cd resumes
```

2. Replace existing info:

   - Delete the current `kennethgao_resume.pdf` file
   - Update the `kennethgao_resume.tex` file with YOUR own details

3. Fix file paths:

   - Update all files within the `terraform/` folder with your updated file paths
   - Update `.github/workflows/actions.yaml` file with your updated file paths

4. Deploy:

   - Add your AWS secrets to github actions
   - If using github, push your changes to the main branch to trigger the github actions
   - If not using github, you're on your own

## Recommended Tools

### LaTeX Workshop Extension

For the best experience when working in this project, I recommend installing the [LaTeX Workshop extension](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop) for Visual Studio Code. This extension provides:

- Real-time PDF preview
- Automatic compilation on save
- Intelligent code completion
- Error detection and reporting
- SyncTeX support for easy navigation between source and PDF
- Built-in snippets for faster LaTeX writing
- Support for bibliography management

To install:

1. Open VS Code
2. Install [LaTeX Workshop extension](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)
3. Install your LaTeX distribution (I used [TeX Live](https://www.tug.org/texlive/))
4. Add directory of TeX Live binaries to your PATH environment (I added `export PATH=$PATH:/usr/local/texlive/2025/bin/universal-darwin` to my `~/.zshrc` file, your mileage may vary)

## Contributing

Feel free to fork this repository and customize it for your own use. If you make improvements that could benefit others, please submit a pull request.

Honestly, if someone helped me clean up all the spaghetti and move all variables to a single file I would be VERY VERY VERY grateful...

## License

This project is open source and available under the MIT License.
