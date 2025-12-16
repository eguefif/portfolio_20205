#!/usr/bin/env python3
"""
Build script to generate index.html from template and markdown files.
"""

import argparse
import markdown

from src.parsers import parse_project_file
from src.images import generate_project_image_html
from src.modals import generate_modal_html
from src.html_utils import generate_youtube_link_html


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Build portfolio index.html')
    parser.add_argument('--resume', action='store_true',
                        help='Add resume download button to the page')
    args = parser.parse_args()

    # Read the template files
    with open('./templates/index.html', 'r', encoding='utf-8') as f:
        main_template = f.read()

    with open('./templates/modal.html', 'r', encoding='utf-8') as f:
        modal_template = f.read()

    with open('./templates/hero.html', 'r', encoding='utf-8') as f:
        hero_template = f.read()

    with open('./templates/projects.html', 'r', encoding='utf-8') as f:
        projects_template = f.read()

    # Read CSS files
    with open('./templates/css/base.css', 'r', encoding='utf-8') as f:
        base_css = f.read()

    with open('./templates/css/hero.css', 'r', encoding='utf-8') as f:
        hero_css = f.read()

    with open('./templates/css/projects.css', 'r', encoding='utf-8') as f:
        projects_css = f.read()

    with open('./templates/css/modal.css', 'r', encoding='utf-8') as f:
        modal_css = f.read()

    # Read JavaScript file
    with open('./templates/js/main.js', 'r', encoding='utf-8') as f:
        javascript = f.read()

    # Read the presentation markdown file
    with open('./presentation.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Convert presentation markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # Combine all CSS
    all_css = f"{base_css}\n\n{hero_css}\n\n{projects_css}\n\n{modal_css}"

    # Start with template replacements
    output = main_template.replace('{{ css }}', all_css)
    output = output.replace('{{ javascript }}', javascript)

    # Replace hero section with template
    hero_html = hero_template.replace('{{ presentation }}', html_content)

    # Add resume button if --resume flag is provided
    if args.resume:
        resume_button_html = '<a href="cv-guefif.pdf" class="resume-button" download aria-label="Download Resume">Download Resume</a>'
    else:
        resume_button_html = ''
    hero_html = hero_html.replace('{{ resume_button }}', resume_button_html)

    output = output.replace('{{ hero }}', hero_html)

    # Replace projects section with template (will be filled in later)
    output = output.replace('{{ projects }}', projects_template)

    # Generate modals HTML
    all_modals = []

    # Parse and replace project data
    for i in range(1, 5):
        project_data = parse_project_file(f'./projects/{i}.md')

        # Generate modal HTML
        modal_html = generate_modal_html(modal_template, i, project_data['title'], project_data['modal_content'])
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
