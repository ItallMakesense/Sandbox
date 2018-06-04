import requests
from itertools import combinations
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz


def _calc_pattern_weight(tags):
    tags_patterns = []
    weight = 1
    for tag in tags:
        children = tag.findChildren(recursive=False)
        if not children:
            weight = 0
            break
        tags_patterns.append(''.join(t.name for t in children))
    if weight:
        tags_patterns.sort()
        for one, other in combinations(tags_patterns, 2):
            weight *= fuzz.ratio(one, other)
    return weight


def get_rich_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_tags = []
    for tag in soup.find_all():
        children = tag.findChildren(recursive=False)
        children_weight = len(children)
        text_weight = len(tag.text)
        pattern_weight = _calc_pattern_weight(children) if children else 0
        overal_weight = children_weight * text_weight * pattern_weight
        all_tags.append([overal_weight, children_weight, text_weight, tag])
    sorted_tags = sorted(all_tags, key=lambda l: l[0])
    return sorted_tags[-1]


if __name__ == '__main__':
    url = 'https://investors.atlassian.com/corporate-governance/management/default.aspx#'
    response = requests.get(url)
    rich_content = get_rich_content(response.text))
