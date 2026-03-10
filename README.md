# Resume Hosting on Cloudflare Pages

Tired of reuploading your most updated resume to Google Drive every time you apply to a new internship? Then this is the project for you! In just 10 minutes, you can create a Single Source of Truth for your resume and portfolio website.

Or, perhaps you just want the template - copy it here on oveleaf! - https://www.overleaf.com/read/qjvqdqcznjxj#d12f4f

## Features

- Based off [Jake's Resume Template](https://www.overleaf.com/latex/templates/jakes-resume/syzfjbzwjncs), with way too many edits
  - goal? maximize content density on a single page + align with typical SG portfolio content
- Automatically convert `.tex` file into JSON, perfect for keeping your portfolio site's information up to date - just fetch from `https://your.domain.here/resume.json`
- Generates beautiful PDFs during CI/CD - no need to commit PDFs anymore!
- Free, instant edge hosting natively supported via Cloudflare Pages and Terraform.

## Getting Started

1. **Fork** this repository.

2. **Update your Content:**
   - Update the `resume.tex` file with YOUR own details.

3. **Configure your Variables:**
   - Go to your GitHub repository **Settings -> Secrets and variables -> Actions -> Variables**.
   - Add a `DOMAIN_NAME` variable (e.g. `resume.yourdomain.com`).
   - Add a `PROJECT_NAME` variable (e.g. `resume-hosting`).

4. **Add CI/CD Secrets:**
   - Go to your GitHub repository **Settings -> Secrets and variables -> Actions -> Secrets**.
   - Add your `CLOUDFLARE_API_TOKEN` (Create one with 'Pages' and 'DNS' edit permissions from your Cloudflare dashboard).
   - Add your `CLOUDFLARE_ACCOUNT_ID`.
   - Add your `CLOUDFLARE_ZONE_ID`.

5. **Deploy:**
   - Push your changes to the `main` branch! GitHub Actions will compile your PDF, extract the JSON, setup the Cloudflare architecture using Terraform, and deploy the site instantly.

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

## License

This project is open source and available under the MIT License.
