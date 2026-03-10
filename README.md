# Resume Hosting on Cloudflare Pages

Tired of reuploading your most updated resume to Google Drive every time you apply to a new internship? Then this is the project for you! In just 10 minutes, you can create a Single Source of Truth for your resume and portfolio website.

Or, perhaps you just want the template - copy it here on oveleaf! - https://www.overleaf.com/read/qjvqdqcznjxj#d12f4f

## Features

- **LaTeX Source of Truth**: Based off [Jake's Resume Template](https://www.overleaf.com/latex/templates/jakes-resume/syzfjbzwjncs), optimized for content density.
- **Automated Data Extraction**: Automatically converts `.tex` into clean `resume.json`, perfect for a headless portfolio site API (fetch from `https://your.domain.com/resume.json`).
- **PDF Generation**: High-quality PDF compiled during CI/CD—no need to commit binaries.
- **PR Preview Environments**: Every Pull Request automatically provisions a unique Cloudflare Pages project and domain (e.g., `resume-4.kenf.dev`) for instant review.
- **Automatic Cleanup**: PR infrastructure is automatically destroyed when the PR is closed or merged.
- **Cloud Infrastructure**: Fully managed via Terraform and HCP Terraform (Terraform Cloud) for state isolation.

## Getting Started

1. **Fork** this repository.

2. **Setup HCP Terraform (Terraform Cloud):**
   - Create an account at [app.terraform.io](https://app.terraform.io).
   - Create an organization (e.g., `your-org-name`).
   - Create a workspace named `resume-hosting` using the **CLI-driven workflow**.
   - In Workspace Settings -> General, set **Execution Mode** to **Local**.
   - Add the tag `resume-hosting` to the workspace.

3. **Update your Content:**
   - Update the `resume.tex` file with YOUR own details.

4. **Configure GitHub Variables:**
   - Go to **Settings -> Secrets and variables -> Actions -> Variables**.
   - `DOMAIN_NAME`: Your resume domain (e.g., `resume.kenf.dev`).
   - `PROJECT_NAME`: Your Cloudflare Pages project prefix (e.g., `resume-hosting`).

5. **Configure GitHub Secrets:**
   - Go to **Settings -> Secrets and variables -> Actions -> Secrets**.
   - `CLOUDFLARE_API_TOKEN`: Token with 'Pages' and 'DNS' edit permissions.
   - `CLOUDFLARE_ACCOUNT_ID`: Your Cloudflare Account ID.
   - `CLOUDFLARE_ZONE_ID`: The Zone ID for your domain.
   - `TF_API_TOKEN`: An API token from HCP Terraform (User Settings -> Tokens).

6. **Deploy:**
   - Push to `main` to deploy your production resume.
   - Create a **Pull Request** to see a preview environment at `resume-[PR_NUMBER].[yourdomain.com]`.

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
