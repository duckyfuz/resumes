# Resume Hosting on Cloudflare Pages

Maintain a professional resume in LaTeX and automatically serve it as a high-quality PDF and a structured JSON API for your portfolio website.

## Features

- **Single Source of Truth**: Edit `resume.tex`, and the system handles the rest.
- **Dynamic Previews**: Every Pull Request creates a unique preview URL (e.g., `resume-4.kenf.dev`).
- **Headless API**: Access your resume data at `your-domain.com/resume.json`.
- **Hands-off Infrastructure**: Automatic deployment and cleanup via GitHub Actions and Terraform.

## Quick Start (10 Minutes)

### 1. External Setup
- **HCP Terraform**: [Create an account](https://app.terraform.io/public/signup/account) and an **Organization**. Generate a [User API Token](https://app.terraform.io/app/settings/tokens).
- **Cloudflare**: Get your **Account ID**, **Zone ID** for your domain, and an **API Token** (with 'Pages' and 'DNS' edit permissions).

### 2. Fork & Configure
Fork this repo and add the following to **Settings -> Secrets and variables -> Actions**:

**Secrets:**
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_ZONE_ID`
- `TF_API_TOKEN` (Your HCP Terraform Token)

**Variables:**
- `DOMAIN_NAME`: e.g., `resume.kenf.dev`
- `PROJECT_NAME`: e.g., `resume-hosting`

### 3. Deploy
- **Production**: Push to `main`. The system will automatically create your HCP Terraform workspace and deploy to your domain.
- **Previews**: Create a Pull Request. A unique environment will be provisioned automatically and destroyed when the PR is closed.

---

## Technical Details

### JSON Extraction
The Python pipeline in `extraction/` parses the LaTeX source using specific comment markers:
- `% SECTION STARTS HERE`
- `% END OF SECTION`

### Local Development
If you want to compile locally, we recommend the [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop) extension for VS Code.

