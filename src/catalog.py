"""Catalog of tests to extract, grouped by narrative section.

Each entry: (key, section, display_name, search_name, kind)
  search_name = exact leading text of the test line in the PDF
  kind        = "num" (numeric value) or "qual" (text value)
"""

N = "num"
Q = "qual"

KL = "kidneys_liver"
EL = "electrolytes"
HM = "heart_meta"
BC = "blood_cells"
VI = "vitamins_iron"
TH = "thyroid"
UR = "urine"

TESTS = [
    ("creatinine", KL, "Creatinine", "Creatinine", N),
    ("gfr", KL, "GFR Estimated", "GFR Estimated", N),
    ("urea", KL, "Urea", "Urea", N),
    ("uric_acid", KL, "Uric Acid", "Uric Acid", N),
    ("ast", KL, "AST (SGOT)", "AST (SGOT)", N),
    ("alt", KL, "ALT (SGPT)", "ALT (SGPT)", N),
    ("ast_alt_ratio", KL, "AST:ALT Ratio", "AST:ALT Ratio", N),
    ("ggtp", KL, "GGTP", "GGTP", N),
    ("alp", KL, "Alkaline Phosphatase", "Alkaline Phosphatase (ALP)", N),
    ("bili_total", KL, "Bilirubin Total", "Bilirubin Total", N),
    ("bili_direct", KL, "Bilirubin Direct", "Bilirubin Direct", N),
    ("protein_total", KL, "Total Protein", "Total Protein", N),
    ("albumin", KL, "Albumin", "Albumin", N),
    ("globulin", KL, "Globulin", "Globulin(Calculated)", N),
    ("ag_ratio", KL, "A:G Ratio", "A : G Ratio", N),
    ("amylase", KL, "Amylase", "Amylase", N),
    ("calcium", EL, "Calcium", "Calcium, Total", N),
    ("phosphorus", EL, "Phosphorus", "Phosphorus", N),
    ("sodium", EL, "Sodium", "Sodium", N),
    ("potassium", EL, "Potassium", "Potassium", N),
    ("chloide", EL, "Chloride", "Chloride", N),
    ("chol_total", HM, "Total Cholesterol", "Cholesterol Total", N),
    ("triglycerides", HM, "Triglycerides", "Triglycerides", N),
    ("hdl", HM, "HDL Cholesterol", "HDL Cholesterol", N),
    ("ldl", HM, "LDL Cholesterol", "LDL Cholesterol,Direct", N),
    ("vldl", HM, "VLDL Cholesterol", "VLDL Cholesterol", N),
    ("non_hdl", HM, "Non-HDL Cholesterol", "Non-HDL Cholesterol", N),
    ("hba1c", HM, "HbA1c", "HbA1c", N),
    ("eag", HM, "Avg. Glucose (eAG)", "Estimated average glucose (eAG)", N),
    ("glucose_f", HM, "Fasting Glucose", "GLUCOSE FASTING (F), PLASMA", N),
    ("hscrp", HM, "hs-CRP", "C-REACTIVE PROTEIN HIGH SENSITIVITY (HsCRP), SERUM", N),
    ("apo_a1", HM, "Apolipoprotein A1", "Apolipoprotein (Apo A1)", N),
    ("apo_b", HM, "Apolipoprotein B", "Apolipoprotein (Apo B)", N),
    ("apo_ratio", HM, "Apo B / A1 Ratio", "Apo B / Apo A1 Ratio", N),
    ("hemoglobin", BC, "Hemoglobin", "Hemoglobin", N),
    ("pcv", BC, "Packed Cell Volume", "Packed Cell Volume (PCV)", N),
    ("rbc", BC, "RBC Count", "RBC Count", N),
    ("mcv", BC, "MCV", "MCV", N),
    ("mch", BC, "MCH", "MCH", N),
    ("mchc", BC, "MCHC", "MCHC", N),
    ("rdw", BC, "RDW", "Red Cell Distribution Width (RDW)", N),
    ("tlc", BC, "Total WBC", "Total Leukocyte Count (TLC)", N),
    ("neutrophils", BC, "Neutrophils", "Segmented Neutrophils", N),
    ("lymphocytes", BC, "Lymphocytes", "Lymphocytes", N),
    ("monocytes", BC, "Monocytes", "Monocytes", N),
    ("eosinophils", BC, "Eosinophils", "Eosinophils", N),
    ("basophils", BC, "Basophils", "Basophils", N),
    ("platelets", BC, "Platelets", "Platelet Count", N),
    ("mpv", BC, "Mean Platelet Vol.", "Mean Platelet Volume", N),
    ("esr", BC, "ESR", "E.S.R.", N),
    ("vit_b12", VI, "Vitamin B12", "Vitamin B12; Cyanocobalamin", N),
    ("vit_d", VI, "Vitamin D (25-OH)", "Vitamin D, 25 Hydroxy", N),
    ("iron", VI, "Iron", "Iron", N),
    ("tibc", VI, "TIBC", "Total Iron Binding Capacity (TIBC)", N),
    ("transf_sat", VI, "Transferrin Saturation", "Transferrin Saturation", N),
    ("t3_free", TH, "Free T3", "Free Triiodothyronine (T3, Free)", N),
    ("t4_free", TH, "Free T4", "Free Thyroxine (T4, Free)", N),
    ("tsh", TH, "TSH", "TSH, Ultrasensitive", N),
    ("ur_sp_grav", UR, "Specific Gravity", "Specific gravity", N),
    ("ur_ph", UR, "pH", "Ph", N),
    ("ur_protein", UR, "Proteins", "Proteins", Q),
    ("ur_glucose", UR, "Glucose", "Glucose", Q),
    ("ur_ketones", UR, "Ketones", "Ketones", Q),
    ("ur_bili", UR, "Bilirubin", "Bilirubin", Q),
    ("ur_blood", UR, "Blood", "Blood", Q),
    ("ur_le", UR, "Leukocyte Esterase", "Leukocyte esterase", Q),
    ("ur_nitrite", UR, "Nitrite", "Nitrite", Q),
    ("ur_uro", UR, "Urobilinogen", "Urobilinogen", Q),
]
