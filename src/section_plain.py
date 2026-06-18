"""Plain-language templates for each narrative section.

Each section has: a one-line 'what this area covers', and templates for the
'all clear', 'watch a few', and 'needs attention' situations. Placeholders:
  {n}        = number of flagged tests in the section
  {list}     = comma-joined plain topics of the flagged tests
  {readings} = "reading" / "readings"
  {verb}     = "is" / "are"
"""

SECTION_PLAIN = {
    "kidneys_liver": {
        "area": "How well your liver and kidneys clean and detoxify your blood.",
        "all_clear": "Your liver enzymes and kidney filters all sit safely inside their healthy range - your body's cleaning system is working well.",
        "watch": "Mostly healthy, with {n} {readings} to keep an eye on: {list}. None are alarming on their own, but worth mentioning to your doctor.",
        "attention": "{n} {readings} here {verb} outside the healthy range ({list}). Worth a closer look with your doctor to rule out liver or kidney concerns.",
    },
    "electrolytes": {
        "area": "The salts and minerals that power your nerves, muscles and bones.",
        "all_clear": "All your minerals and salts are balanced - your nerves, muscles and bones are well supplied.",
        "watch": "{n} mineral {readings} {verb} just outside the ideal range ({list}). With healthy kidneys this is usually down to a recent meal or hydration, not illness.",
        "attention": "{n} mineral {readings} {verb} off ({list}). Usually diet or hydration related, but worth confirming with your doctor.",
    },
    "heart_meta": {
        "area": "Your long-term heart and sugar picture: cholesterol, blood sugar and inflammation.",
        "all_clear": "Your cholesterol, blood sugar and inflammation markers are all in the healthy zone - your heart and metabolism look good.",
        "watch": "Mostly good, but {n} heart-related {readings} {verb} above the ideal ({list}). These are the ones most worth a lifestyle chat with your doctor.",
        "attention": "{n} heart/sugar {readings} need attention ({list}). These are the key numbers for your heart and diabetes risk - please discuss with your doctor.",
    },
    "blood_cells": {
        "area": "Your blood cells: red cells carry oxygen, white cells fight infection, platelets help clotting.",
        "all_clear": "Your red cells, white cells and platelets are all in healthy numbers - good oxygen, immunity and clotting.",
        "watch": "Blood counts are mostly healthy, with {n} {readings} just nudging the edge ({list}). Often a recent mild virus; usually nothing to worry about.",
        "attention": "{n} blood-cell {readings} {verb} outside range ({list}). Worth checking with your doctor, especially if you feel tired or run down.",
    },
    "vitamins_iron": {
        "area": "Nutrients that fuel your bones, immunity and blood-building.",
        "all_clear": "Your vitamins and iron stores are all at healthy levels - good nutritional backup for bones, immunity and blood.",
        "watch": "{n} nutrient {readings} {verb} below ideal ({list}). Gaps here are common and usually easy to fix with diet or supplements - ask your doctor.",
        "attention": "{n} nutrient {readings} {verb} low ({list}). These can affect energy, bones and immunity, so worth correcting with your doctor's guidance.",
    },
    "thyroid": {
        "area": "Your thyroid - the gland that sets your body's energy 'speed'.",
        "all_clear": "Your thyroid hormones are balanced - your metabolism is running at a healthy pace.",
        "watch": "Thyroid {readings} {verb} close to the edge ({list}). Usually nothing urgent, but your doctor may want to recheck.",
        "attention": "{n} thyroid {readings} {verb} off ({list}). This can affect energy and weight - worth discussing with your doctor.",
    },
    "urine": {
        "area": "A quick screen of your urinary tract.",
        "all_clear": "All urine checks came back clear - no signs of infection, blood, sugar or protein leaking into the urine.",
        "watch": "Mostly clear, with {n} item(s) to note: {list}. Usually minor, but worth mentioning if you have any symptoms.",
        "attention": "{n} urine finding(s) need a check ({list}). See your doctor if you have burning, frequency or pain.",
    },
}


def template(section_key: str, situation: str) -> str:
    return SECTION_PLAIN.get(section_key, {}).get(situation, "")
