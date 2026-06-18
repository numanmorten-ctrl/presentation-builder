"""Rule-based Story JSON generator; designed as the future OpenAI integration seam."""

from __future__ import annotations

from .content_salary import DEFAULT_DECK_STYLE, DEFAULT_SLIDE_COUNT, is_morten_salary_prompt
from .schemas import DeckStory


def _style_lens(style: str) -> str:
    return {
        "Executive / McKinsey-style": "kort, ledelsesrettet og beslutningsorienteret",
        "Technical": "med ekstra vægt på BIM, data, software, automation og AI",
        "Sales / customer-facing": "med vægt på kundeværdi, troværdighed og forretningsresultater",
        "Internal management": "med vægt på rolleafklaring, mandat, governance og fastholdelse",
    }.get(style, "ledelsesrettet")


def build_story(description: str, deck_style: str = DEFAULT_DECK_STYLE, slide_count: int = DEFAULT_SLIDE_COUNT, include_notes: bool = True) -> DeckStory:
    """Convert user input to Story JSON before any PowerPoint rendering happens."""
    if is_morten_salary_prompt(description):
        story = build_morten_salary_story(description, deck_style, include_notes)
    else:
        story = build_generic_executive_story(description, deck_style, include_notes)
    story["slides"] = story["slides"][: max(1, min(slide_count, len(story["slides"]))) ]
    return story


def build_morten_salary_story(description: str, deck_style: str = DEFAULT_DECK_STYLE, include_notes: bool = True) -> DeckStory:
    notes = include_notes
    return {
        "meta": {
            "title": "Rolleudvikling og løndialog",
            "subtitle": "Morten Numan | Ledelsesdialog",
            "audience": "Nærmeste leder og relevante beslutningstagere",
            "style": f"{deck_style} — {_style_lens(deck_style)}",
            "language": "da",
            "include_speaker_notes": include_notes,
        },
        "slides": [
            {"type": "cover", "title": "Rolleudvikling og løndialog", "subtitle": "Morten Numan | Executive discussion document", "speaker_notes": "Positionér mødet som en konstruktiv udviklingsdialog – ikke som et ensidigt lønkrav." if notes else ""},
            {"type": "executive_summary", "title": "Executive summary", "cards": [{"headline": "Rollen er vokset", "body": "Ansvar og kompleksitet ligger i dag over det oprindelige 2024-udgangspunkt."}, {"headline": "Værdien er tværfaglig", "body": "Morten forbinder byggefaglighed med BIM, data, systemer og automation."}, {"headline": "Beslutningen er tydelig", "body": "Rolle, titel og løn bør afstemmes med den faktiske contribution i dag."}], "speaker_notes": "Giv lederen hele argumentet på ét minut: scope, værdi og konkret ask." if notes else ""},
            {"type": "timeline", "title": "Professionel udvikling over tid", "items": [{"label": "2024", "detail": "Oprindeligt rollegrundlag og forventet leverance."}, {"label": "H1 2025", "detail": "Mere koordinering, ejerskab og tværgående samarbejde."}, {"label": "H2 2025", "detail": "BIM, data og systemarbejde fylder mere i værdiskabelsen."}, {"label": "I dag", "detail": "Automation, software og AI udvider mandatet yderligere."}], "speaker_notes": "Brug tidslinjen til at vise udviklingen som et faktuelt mønster." if notes else ""},
            {"type": "comparison", "title": "Rolle 2024 vs. rolle i dag", "left_title": "2024 baseline", "right_title": "I dag", "left_items": ["Defineret opgaveudførsel", "Primært funktionelt scope", "Relativt enkel benchmark"], "right_items": ["End-to-end ejerskab", "Tværgående digitalt mandat", "Hybrid profil, svær at benchmarke"], "speaker_notes": "Fremhæv forskellen mellem formel rollebeskrivelse og faktisk bidrag." if notes else ""},
            {"type": "value_cards", "title": "Værdiskabelse for Knauf", "cards": [{"headline": "Produktivitet", "body": "Automatiserer og forenkler gentagende arbejde."}, {"headline": "Kvalitet", "body": "Styrker struktur, datadisciplin og konsistens."}, {"headline": "Hastighed", "body": "Omsætter uklarhed til brugbare systemer og beslutninger."}, {"headline": "Leverage", "body": "Får tekniske og kommercielle teams til at arbejde bedre sammen."}], "speaker_notes": "Oversæt kompetencer til forretningsresultater: mindre friktion, bedre beslutninger, hurtigere leverance." if notes else ""},
            {"type": "house_model", "title": "Tværfaglig profil — svær at benchmarke", "foundation": "Byggefaglig baggrund og praktisk erfaring", "core": "BIM + data + systemer", "upper": "Automation | Software | AI", "roof": "Digitale produkter og forretningsværdi", "side_note": "Markedet priser ofte lagene hver for sig — rollen kombinerer dem.", "speaker_notes": "Forklar at rollen ikke bør vurderes som én smal funktion." if notes else ""},
            {"type": "case_list", "title": "Dokumenterede resultater", "cases": [{"headline": "Bredere scope", "body": "Flere opgaver og interessenter håndteres med højere selvstændighed."}, {"headline": "Større ejerskab", "body": "Mere ansvar for struktur, proces og digital fremdrift."}, {"headline": "Bedre alignment", "body": "Støtter fælles sprog mellem faglighed, data og forretning."}], "speaker_notes": "Erstat gerne eksemplerne med konkrete projekter, feedback og leverancer før mødet." if notes else ""},
            {"type": "hub_and_spokes", "title": "Fremtidigt potentiale", "center": "Tydeligt mandat", "items": ["Anerkend nuværende scope", "Definér fremtidig rolle", "Skalér digitale produkter", "Afstem titel og løn"], "speaker_notes": "Positionér anerkendelse som en business enabler for fastholdelse og mere værdi." if notes else ""},
            {"type": "conclusion", "title": "Konklusion / dialog om rolle, titel og løn", "statements": ["Bidraget har ændret sig væsentligt.", "Rolleframeworket bør indhente virkeligheden.", "Næste skridt bør være konkret og tidsfastsat."], "final_message": "Lad os afstemme rolle, titel og løn med den værdi, der skabes i dag.", "speaker_notes": "Afslut med at aftale næste skridt, timing og beslutningsejere." if notes else ""},
        ],
    }


def build_generic_executive_story(description: str, deck_style: str = DEFAULT_DECK_STYLE, include_notes: bool = True) -> DeckStory:
    topic = description.strip().splitlines()[0][:80] if description.strip() else "Executive presentation"
    return {
        "meta": {"title": topic, "subtitle": "Executive storyline", "audience": "Executive audience", "style": deck_style, "language": "da", "include_speaker_notes": include_notes},
        "slides": [
            {"type": "cover", "title": topic, "subtitle": "Executive storyline", "speaker_notes": "Åbn med formål og ønsket beslutning." if include_notes else ""},
            {"type": "executive_summary", "title": "Executive summary", "cards": [{"headline": "Kontekst", "body": "Hvorfor emnet er vigtigt nu."}, {"headline": "Indsigt", "body": "Hvad analysen peger på."}, {"headline": "Anbefaling", "body": "Hvad vi bør beslutte og gøre."}], "speaker_notes": "Hold budskabet kort og beslutningsorienteret." if include_notes else ""},
            {"type": "conclusion", "title": "Næste skridt", "statements": ["Afklar beslutning.", "Fordel ansvar.", "Fastlæg timing."], "final_message": "Fra fælles retning til konkret handling.", "speaker_notes": "Luk med klare next steps." if include_notes else ""},
        ],
    }
