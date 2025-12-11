"""HTML generation utility functions."""


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
