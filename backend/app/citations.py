import re
from html import escape

from app.models import Source

REF_PATTERN = re.compile(r"<ref>(.*?)</ref>")


def link_citations(content: str, sources: list[Source]) -> str:
    """Replace each <ref>id</ref> with a numbered link to its source.

    Sources are numbered in the order they're first cited. A ref whose id
    doesn't match any source is removed.
    """
    sources_by_id = {source.id: source for source in sources}

    number = 0
    for source_id in REF_PATTERN.findall(content):
        source = sources_by_id.get(source_id)
        if source is not None and source.number is None:
            number += 1
            source.number = number

    def to_link(match: re.Match) -> str:
        source = sources_by_id.get(match.group(1))
        if source is None:
            return ""
        url = escape(source.source)
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">[{source.number}]</a>'

    return REF_PATTERN.sub(to_link, content)