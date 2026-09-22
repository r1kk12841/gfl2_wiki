"""Fortification previews must attach only to the correct skill."""
import json
import sys
from pathlib import Path

builder = sys.modules['gfl2_site_builder']


def test_alva_levels_keep_their_source_tiers():
    doll = json.loads((Path('data/characters/alva.json')).read_text(encoding='utf-8'))
    builder.enrich_doll_fortifications(doll)
    skills = {s['name']: s for s in doll['skills']}
    assert [(u['level'], u['tier']) for u in skills['Frosted Echo']['level_upgrades']] == [(2, 1), (3, 5)]
    assert skills['Laceration']['level_upgrades'] == []
    assert [(u['level'], u['tier']) for u in skills['Nix Requiem']['level_upgrades']] == [(2, 2)]


def test_similar_names_do_not_receive_unrelated_upgrades():
    doll = {'skills': [{'name': 'Echo'}, {'name': 'Echo Strike'}],
            'fortification': [{'skill': 'Echo Strike', 'level': 2, 'tier': 1, 'effect': 'Upgrade'}]}
    builder.enrich_doll_fortifications(doll)
    assert doll['skills'][0]['level_upgrades'] == []
    assert len(doll['skills'][1]['level_upgrades']) == 1


def test_preview_renders_source_effect_and_tier_link(built_site):
    html = (built_site / 'characters/alva.html').read_text(encoding='utf-8')
    assert 'class="skill-level-preview"' in html
    assert 'href="#fortification-5"' in html
    assert 'data-upgrade-tier="5"' in html
    assert 'id="fortification-5"' in html
