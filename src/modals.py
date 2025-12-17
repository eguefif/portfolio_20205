"""Modal generation functions."""

import markdown
import re

from src.images import find_section_image
from src.parsers import parse_markdown_sections


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


def generate_modal_html(modal_template, project_number, project_title, project_tech, markdown_content):
    """
    Generate a complete modal HTML from the modal template.
    """
    modal_body = generate_modal_body(project_number, markdown_content)

    # Replace placeholders in modal template
    modal_html = modal_template.replace('{{ modal_id }}', f'modal-{project_number}')
    modal_html = modal_html.replace('{{ project_title }}', project_title)
    modal_html = modal_html.replace('{{ project_tech }}', project_tech)
    modal_html = modal_html.replace('{{ modal_body }}', modal_body)

    return modal_html
