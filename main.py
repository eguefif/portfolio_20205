#!/usr/bin/env python3
"""
Build script to generate index.html from template and markdown files.
"""

import markdown


def parse_project_file(filepath):
    """
    Parse a project markdown file to extract metadata and content.

    Expected format:
    - First line: GitHub link (may have 'gh:' prefix)
    - Optional: YouTube link (with 'yt:' prefix)
    - # Title
    - First paragraph (description)

    Returns a dict with: github, youtube, title, description
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    github = ""
    youtube = ""
    title = ""
    description = ""

    # First line is always GitHub link
    if lines:
        github = lines[0].strip()
        if github.startswith('gh:'):
            github = github[3:].strip()

    # Look for optional YouTube link and title
    i = 1
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('yt:'):
            youtube = line[3:].strip()
            i += 1
        elif line.startswith('#'):
            # Found the title
            title = line.lstrip('#').strip()
            i += 1
            break
        else:
            i += 1

    # Extract the first paragraph (skip empty lines after title)
    while i < len(lines):
        line = lines[i].strip()
        if line and not line.startswith('#'):
            description = line
            break
        i += 1

    return {
        'github': github,
        'youtube': youtube,
        'title': title,
        'description': description
    }


def generate_youtube_link_html(youtube_url):
    """
    Generate HTML for YouTube link if URL exists, otherwise return empty string.
    """
    if youtube_url:
        return f'''<a href="{youtube_url}" target="_blank" class="youtube-link">
                        <img src="images/yt_icon_red_digital.png" alt="YouTube">
                    </a>
                    '''
    return ''


def main():
    # Read the template file
    with open('./template/index.html', 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Read the presentation markdown file
    with open('./presentation.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Convert presentation markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # Start with the presentation replacement
    output = template_content.replace('{{ presentation }}', html_content)

    # Parse and replace project data
    for i in range(1, 5):
        project_data = parse_project_file(f'./projects/{i}.md')

        # Replace GitHub link
        output = output.replace(f'{{{{ project_{i}_github }}}}', project_data['github'])

        # Replace title and description
        output = output.replace(f'{{{{ project_{i}_title }}}}', project_data['title'])
        output = output.replace(f'{{{{ project_{i}_description }}}}', project_data['description'])

        # Replace YouTube link placeholder with generated HTML
        youtube_html = generate_youtube_link_html(project_data['youtube'])
        output = output.replace(f'{{{{ project_{i}_youtube_link }}}}', youtube_html)

    # Write the output to index.html in the root folder
    with open('./index.html', 'w', encoding='utf-8') as f:
        f.write(output)

    print("Successfully generated index.html")


if __name__ == '__main__':
    main()
