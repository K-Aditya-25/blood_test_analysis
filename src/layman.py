"""Plain-English (layman) wording for test results and section summaries.

Wording is grounded in patient-facing sources (American Heart Association,
Cleveland Clinic, American Liver/Kidney/Thyroid foundations) - no patient
data is used here. Each test maps to the body system it reflects and a short
phrase describing an out-of-range result in everyday language.
"""

# test key -> (health area in plain words, what a high/low result hints at)
TOPICS = {
    "creatinine": ("kidney waste filtering", "kidneys may be clearing waste a little slower"),
    "gfr": ("kidney filtering rate", "kidney filtering may be reduced"),
    "urea": ("kidney waste (urea)", "can point to dehydration or kidney strain"),
    "uric_acid": ("joint/crystal waste", "high levels can lead to gout or kidney stones"),
    "ast": ("liver enzymes", "possible irritation of the liver"),
    "alt": ("liver enzymes", "possible irritation of the liver"),
    "ast_alt_ratio": ("liver enzyme balance", "on its own this ratio rarely means trouble when both enzymes are normal"),
    "ggtp": ("liver bile flow", "may hint at bile-flow or alcohol-related stress"),
    "alp": ("liver/bone enzyme", "may point to liver or bone activity"),
    "bili_total": ("waste from broken-down red cells", "can hint at a bile-flow or red-cell issue"),
    "bili_direct": ("processed bile pigment", "may point to a bile-flow concern"),
    "protein_total": ("overall blood protein", "often just dehydration; sometimes liver/kidney loss"),
    "albumin": ("main blood protein (liver-made)", "may suggest low intake, or liver/kidney loss"),
    "globulin": ("immune & transport proteins", "may reflect immune activity"),
    "ag_ratio": ("protein balance", "a mild imbalance - worth reviewing with the proteins"),
    "amylase": ("pancreas & salivary enzyme", "a mild rise alone (under 3x the limit) rarely means pancreatitis"),
    "calcium": ("bone & nerve mineral", "may relate to parathyroid or vitamin D"),
    "phosphorus": ("bone & cell mineral", "with good kidney filtering, a mild rise is usually diet or harmless"),
    "sodium": ("body water & salt balance", "often simply hydration-related"),
    "potassium": ("heart & muscle cell salt", "can affect heart rhythm if very off"),
    "chloide": ("acid/salt balance", "usually tracks sodium shifts"),
    "chol_total": ("overall blood fat", "slightly above the ideal range"),
    "triglycerides": ("blood fat from calories", "high - often from sugars, alcohol or diet"),
    "hdl": ("'good' cholesterol (clears arteries)", "on the lower side - exercise and healthy fats help raise it"),
    "ldl": ("'bad' cholesterol (furs up arteries)", "above the ideal - a heart-risk marker worth a chat with your doctor"),
    "vldl": ("triglyceride-carrying fat", "tracks with triglycerides"),
    "non_hdl": ("all 'bad' cholesterol combined", "above the ideal - reflects overall heart risk"),
    "hba1c": ("3-month average blood sugar", "in the healthy, non-diabetic range"),
    "eag": ("estimated average blood sugar", "for context only"),
    "glucose_f": ("fasting blood sugar", "at the higher or lower end - worth rechecking"),
    "hscrp": ("low-grade inflammation / heart risk", "rises move heart risk from low toward average/high"),
    "apo_a1": ("protective 'good' cholesterol particles", "lower protection for the heart"),
    "apo_b": ("'bad' plaque-forming particles", "higher plaque risk"),
    "apo_ratio": ("plaque-risk balance", "above ideal raises heart-disease risk"),
    "hemoglobin": ("oxygen-carrying pigment", "low means anaemia (tiredness); check iron/B12"),
    "pcv": ("share of blood that is red cells", "low can mean anaemia or bleeding"),
    "rbc": ("number of red blood cells", "slightly low - may point to early iron lack"),
    "mcv": ("average red-cell size", "small hints at iron lack; large hints at B12/folate"),
    "mch": ("haemoglobin per cell", "pale cells can hint at iron lack"),
    "mchc": ("haemoglobin concentration", "low colour often points to iron lack"),
    "rdw": ("variation in red-cell size", "mixed sizes often mean iron lack"),
    "tlc": ("total white blood cells", "reflects immune activity"),
    "neutrophils": ("bacterial-fighting white cells", "off - may reflect infection/inflammation"),
    "lymphocytes": ("viral-fighting white cells", "slightly raised - often a recent mild virus, usually harmless"),
    "monocytes": ("clean-up white cells", "slightly raised - often recovery/inflammation, usually temporary"),
    "eosinophils": ("allergy/parasite white cells", "raised - may mean allergy or parasite activity"),
    "basophils": ("allergy-signal white cells", "raised - allergic/inflammatory activity"),
    "platelets": ("clot-forming cells", "off - affects clotting tendency"),
    "mpv": ("average platelet size", "larger new platelets"),
    "esr": ("general inflammation marker", "some inflammation present"),
    "vit_b12": ("nerve & blood-cell vitamin", "low can affect nerves and blood cells"),
    "vit_d": ("bone & immunity vitamin", "low means weaker bones and immunity - common and fixable"),
    "iron": ("circulating iron", "low iron stores"),
    "tibc": ("iron-carrying capacity", "high often means the body is short of iron"),
    "transf_sat": ("how full iron transport is", "below 20% means low usable iron - early iron shortage"),
    "t3_free": ("active thyroid hormone", "off can mean an over/underactive thyroid"),
    "t4_free": ("main thyroid hormone", "off can mean an over/underactive thyroid"),
    "tsh": ("thyroid 'thermostat' signal", "off can mean an over/underactive thyroid"),
    "ur_sp_grav": ("urine concentration", "reflects hydration"),
    "ur_ph": ("urine acidity", "within the normal range"),
    "ur_protein": ("protein in urine", "present - worth a kidney check"),
    "ur_glucose": ("sugar in urine", "sugar spilling - check blood sugar"),
    "ur_ketones": ("fat-burn byproducts", "present - fasting or possible diabetes"),
    "ur_bili": ("bile pigment in urine", "present - liver/bile check"),
    "ur_blood": ("blood in urine", "trace - urinary tract check"),
    "ur_le": ("white-cell enzyme in urine", "present - possible urine infection"),
    "ur_nitrite": ("bacteria marker in urine", "present - possible urine infection"),
    "ur_uro": ("bilirubin breakdown in urine", "raised - liver/red-cell check"),
}


def topic(key: str) -> str:
    return TOPICS.get(key, ("this test", "slightly outside the usual range"))[0]


def hint(key: str) -> str:
    return TOPICS.get(key, ("this test", "slightly outside the usual range"))[1]
