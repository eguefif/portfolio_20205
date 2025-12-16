# Portfolio Builder

A static site generator that builds a portfolio website from markdown files and templates.

## How It Works

The builder (`main.py`) reads markdown files from the `projects/` folder and templates from the `template/` folder, then generates a single `index.html` file with your portfolio.

**Setup Command:**
```bash
uv sync
```

**Build command:**
```bash
uv run main.py
```

**Build with resume download button:**
```bash
uv run main.py --resume
```

This adds a "Download Resume" button in the hero section that links to `cv-guefif.pdf`.

**Publish to personal website:**
```bash
uv run main.py --publish
```

This will:
- Copy `index.html` to your personal website directory
- Copy the `images/` directory
- Copy `cv-guefif.pdf` (if it exists)
- Commit the changes with a timestamp message

Note: Git push is currently disabled. You'll need to manually push changes to deploy.

## Project Structure


## Editing Projects

Each project is a markdown file in `projects/` numbered `1.md`, `2.md`, etc.

## Adding Images

Images follow the naming pattern: `{project_number}-{image_number}.{ext}`
