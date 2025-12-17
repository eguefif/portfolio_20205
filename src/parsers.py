"""Parsing functions for markdown files."""

import markdown
import re


def parse_project_file(filepath):
    """
    Parse a project markdown file to extract metadata and content.

    Expected format:
    - First line: GitHub link (may have 'gh:' prefix)
    - Optional: YouTube link (with 'yt:' prefix)
    - # Title
    - First paragraph (description)
    - Full content for modal

    Returns a dict with: github, youtube, title, description, full_content_html
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    github = ""
    youtube = ""
    tech = ""
    title = ""
    description = ""
    modal_content = []

    # First line is always GitHub link
    if lines:
        github = lines[0].strip()
        if github.startswith('gh:'):
            github = github[3:].strip()

    # Look for optional tech line, YouTube link and title
    i = 1
    if i < len(lines) and lines[i].strip().startswith('tech:'):
        tech = lines[i].strip()[5:].strip()
        i += 1
    title_line_index = -1
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('yt:'):
            youtube = line[3:].strip()
            i += 1
        elif line.startswith('#') and not line.startswith('##'):
            # Found the title
            title = line.lstrip('#').strip()
            title_line_index = i
            i += 1
            break
        else:
            i += 1

    # Extract the first paragraph (skip empty lines after title)
    first_para_index = -1
    while i < len(lines):
        line = lines[i].strip()
        if line and not line.startswith('#'):
            description = line
            first_para_index = i
            break
        i += 1

    # Extract everything after the title for the modal (excluding the first line which is the link)
    if title_line_index >= 0:
        modal_lines = lines[title_line_index + 1:]
        modal_markdown = '\n'.join(modal_lines)
        modal_content_html = markdown.markdown(modal_markdown)
    else:
        modal_content_html = ""

    return {
        'github': github,
        'youtube': youtube,
        'tech': tech,
        'title': title,
        'description': description,
        'modal_content': modal_content_html
    }


def parse_markdown_sections(markdown_text):
    """
    Parse markdown text and split it into sections based on H2 headings (##).
    Returns a list of tuples: (heading, content)
    First item is the intro content before any H2 heading.
    """
    sections = []

    # Split by H2 headings
    parts = re.split(r'^## (.+)$', markdown_text, flags=re.MULTILINE)

    # First part is the intro (before any H2)
    if parts[0].strip():
        sections.append(('', parts[0].strip()))

    # Process remaining parts in pairs (heading, content)
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            heading = parts[i].strip()
            content = parts[i + 1].strip()
            sections.append((heading, content))

    return sections
