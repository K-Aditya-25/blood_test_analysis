"""Narrative sections: each groups related tests into a health 'story'."""

from .models import Section

SECTIONS = [
    Section("kidneys_liver", "Liver & Kidney Function", "organ",
        "These organs clear waste and detoxify your blood. When both liver enzymes "
        "and kidney filters sit inside their healthy bands, your body's filtration "
        "system is working well.", "bullet", 1),
    Section("electrolytes", "Minerals & Electrolytes", "salt",
        "These minerals power your nerves, muscles and bones. Small shifts are common "
        "and often reflect a recent meal or hydration rather than illness when kidney "
        "function is good.", "bullet", 2),
    Section("heart_meta", "Heart & Sugar Control", "heart",
        "This is your long-term metabolic risk picture: cholesterol, blood sugar and "
        "inflammation together signal how hard your heart is working.", "bullet", 3),
    Section("blood_cells", "Blood Cell Health", "cell",
        "Red cells carry oxygen, white cells defend you, platelets clot. Counts inside "
        "their bands mean healthy blood and immune balance.", "bullet", 4),
    Section("vitamins_iron", "Vitamins & Iron Stores", "vitamin",
        "Nutrients that fuel bones, immunity and blood-building. Gaps here are common "
        "and easy to correct once spotted.", "bullet", 5),
    Section("thyroid", "Thyroid Balance", "thyroid",
        "Your metabolic thermostat. Balanced TSH, T3 and T4 mean a well-regulated "
        "metabolism and energy level.", "bullet", 6),
    Section("urine", "Urine Health", "urine",
        "A quick screen of the urinary tract - all 'negative' results are good news, "
        "meaning no signs of infection, blood or sugar spilling.", "status", 7),
]

THEME = {
    "kidneys_liver": "liver and kidney filtering",
    "electrolytes": "minerals and salts",
    "heart_meta": "heart health and blood sugar",
    "blood_cells": "blood cell counts",
    "vitamins_iron": "vitamins and iron",
    "thyroid": "thyroid (metabolism)",
    "urine": "urine",
}
