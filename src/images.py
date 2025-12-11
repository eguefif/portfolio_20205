"""Image-related utility functions."""

import glob


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
