#!/usr/bin/env python3
"""
Build script to generate index.html from template and markdown files.
"""

import markdown
import os
import glob
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
    title = ""
    description = ""
    modal_content = []

    # First line is always GitHub link
    if lines:
        github = lines[0].strip()
        if github.startswith('gh:'):
            github = github[3:].strip()

    # Look for optional YouTube link and title
    i = 1
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
        'title': title,
        'description': description,
        'modal_content': modal_content_html
    }


def generate_youtube_link_html(youtube_url):
    """
    Generate HTML for YouTube link if URL exists, otherwise return empty string.
    """
    if youtube_url:
        return f'''<a href="{youtube_url}" target="_blank" class="youtube-link" onclick="event.stopPropagation()">
                        <img src="images/yt_icon_red_digital.png" alt="YouTube">
                    </a>
                    '''
    return ''


def find_project_image(project_number):
    """
    Find the first image for a project in the projects folder.
    Looks for files matching pattern: {project_number}-1.* (png, jpg, jpeg, webp, gif)

    Returns the image path if found, otherwise returns empty string.
    """
    image_extensions = ['png', 'jpg', 'jpeg', 'webp', 'gif']

    for ext in image_extensions:
        # Look for pattern like "1-1.png", "2-1.jpg", etc.
        pattern = f'./projects/{project_number}-1.{ext}'
        matches = glob.glob(pattern)
        if matches:
            return matches[0]

    return ''


def generate_project_image_html(project_number, project_title):
    """
    Generate HTML for project image if it exists, otherwise return empty string.
    """
    image_path = find_project_image(project_number)

    if image_path:
        return f'<img src="{image_path}" alt="{project_title}" class="project-image">'

    return ''


def find_section_image(project_number, section_number):
    """
    Find an image for a specific section of a project.
    Looks for files matching pattern: {project_number}-{section_number}.* (png, jpg, jpeg, webp, gif)

    Returns the image path if found, otherwise returns empty string.
    """
    image_extensions = ['png', 'jpg', 'jpeg', 'webp', 'gif']

    for ext in image_extensions:
        pattern = f'./projects/{project_number}-{section_number}.{ext}'
        matches = glob.glob(pattern)
        if matches:
            return matches[0]

    return ''


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


def generate_modal_body(project_number, markdown_content):
    """
    Generate modal body HTML with sections and alternating images.
    H1 title is removed from content (it appears in modal header instead).
    Images alternate between left and right for each section.
    """
    sections = parse_markdown_sections(markdown_content)
    html_parts = []
    image_counter = 1

    for idx, (heading, content) in enumerate(sections):
        # Check if this is the first section (intro) and remove H1 title
        if idx == 0 and not heading:
            # Remove H1 from content (it's already in the modal header)
            content = re.sub(r'^# .+$\n?', '', content, count=1, flags=re.MULTILINE).strip()

        # Skip empty sections
        if not content.strip() and not heading:
            continue

        section_html = '<div class="modal-section">'

        # Find image for this section
        image_path = find_section_image(project_number, image_counter)

        if image_path:
            # Alternate image position: odd sections = left, even sections = right
            image_class = 'modal-section-image-left' if idx % 2 == 0 else 'modal-section-image-right'
            section_html += f'<img src="{image_path}" alt="{heading}" class="{image_class}">'
            image_counter += 1

        # Add heading if it exists (H2 sections)
        if heading:
            section_html += f'<h2>{heading}</h2>'

        # Convert markdown content to HTML
        if content.strip():
            content_html = markdown.markdown(content)
            section_html += content_html

        section_html += '</div>'
        html_parts.append(section_html)

    return '\n'.join(html_parts)


def generate_modal_html(modal_template, project_number, project_title, markdown_content):
    """
    Generate a complete modal HTML from the modal template.
    """
    modal_body = generate_modal_body(project_number, markdown_content)

    # Replace placeholders in modal template
    modal_html = modal_template.replace('{{ modal_id }}', f'modal-{project_number}')
    modal_html = modal_html.replace('{{ project_title }}', project_title)
    modal_html = modal_html.replace('{{ modal_body }}', modal_body)

    return modal_html


def main():
    # Read the template files
    with open('./template/index.html', 'r', encoding='utf-8') as f:
        template_content = f.read()

    with open('./template/modal.html', 'r', encoding='utf-8') as f:
        modal_template = f.read()

    with open('./template/hero.html', 'r', encoding='utf-8') as f:
        hero_template = f.read()

    with open('./template/projects.html', 'r', encoding='utf-8') as f:
        projects_template = f.read()

    # Read CSS files
    with open('./template/css/base.css', 'r', encoding='utf-8') as f:
        base_css = f.read()

    with open('./template/css/hero.css', 'r', encoding='utf-8') as f:
        hero_css = f.read()

    with open('./template/css/projects.css', 'r', encoding='utf-8') as f:
        projects_css = f.read()

    with open('./template/css/modal.css', 'r', encoding='utf-8') as f:
        modal_css = f.read()

    # Read JavaScript file
    with open('./template/js/main.js', 'r', encoding='utf-8') as f:
        javascript = f.read()

    # Read the presentation markdown file
    with open('./presentation.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Convert presentation markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # Combine all CSS
    all_css = f"{base_css}\n\n{hero_css}\n\n{projects_css}\n\n{modal_css}"

    # Start with template replacements
    output = template_content.replace('{{ css }}', all_css)
    output = output.replace('{{ javascript }}', javascript)

    # Replace hero section with template
    hero_html = hero_template.replace('{{ presentation }}', html_content)
    output = output.replace('{{ hero }}', hero_html)

    # Replace projects section with template (will be filled in later)
    output = output.replace('{{ projects }}', projects_template)

    # Generate modals HTML
    all_modals = []

    # Parse and replace project data
    for i in range(1, 5):
        project_data = parse_project_file(f'./projects/{i}.md')

        # Read the full markdown content for modal generation
        with open(f'./projects/{i}.md', 'r', encoding='utf-8') as f:
            full_markdown = f.read()
            # Extract content after the title line for modal
            lines = full_markdown.split('\n')
            # Skip GitHub link, optional YouTube link, and title
            modal_markdown = '\n'.join(lines[1:])  # Start from line after GitHub link

        # Generate modal HTML
        modal_html = generate_modal_html(modal_template, i, project_data['title'], modal_markdown)
        all_modals.append(modal_html)

        # Replace GitHub link
        output = output.replace(f'{{{{ project_{i}_github }}}}', project_data['github'])

        # Replace title and description
        output = output.replace(f'{{{{ project_{i}_title }}}}', project_data['title'])
        output = output.replace(f'{{{{ project_{i}_description }}}}', project_data['description'])

        # Replace YouTube link placeholder with generated HTML
        youtube_html = generate_youtube_link_html(project_data['youtube'])
        output = output.replace(f'{{{{ project_{i}_youtube_link }}}}', youtube_html)

        # Replace image placeholder with generated HTML
        image_html = generate_project_image_html(i, project_data['title'])
        output = output.replace(f'{{{{ project_{i}_image }}}}', image_html)

    # Replace modals placeholder with all generated modals
    output = output.replace('{{ modals }}', '\n'.join(all_modals))

    # Write the output to index.html in the root folder
    with open('./index.html', 'w', encoding='utf-8') as f:
        f.write(output)

    print("Successfully generated index.html")


if __name__ == '__main__':
    main()
