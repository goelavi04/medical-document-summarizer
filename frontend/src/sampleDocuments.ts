// Synthetic, non-identifiable example documents for demo purposes only — not real patient
// records. Useful for reviewers who want to try the tool without pasting their own text.
export const SAMPLE_DOCUMENTS: { label: string; text: string }[] = [
  {
    label: "Research abstract (synthetic)",
    text: `Background: Community-acquired pneumonia (CAP) remains a leading cause of hospitalization among adults over 65. This study evaluated outcomes of early versus delayed antibiotic administration in patients presenting with CAP.

Methods: We conducted a retrospective cohort study of 342 patients admitted with a diagnosis of community-acquired pneumonia between January 2021 and December 2022. Patients received either amoxicillin-clavulanate or ceftriaxone within 4 hours of presentation (early group, n=198) or after 4 hours (delayed group, n=144). The primary outcome was in-hospital mortality; secondary outcomes included length of stay and ICU transfer rate.

Results: In-hospital mortality was lower in the early antibiotic group (3.0%) compared to the delayed group (7.6%, p=0.04). Median length of stay was 5.2 days in the early group versus 7.1 days in the delayed group (p=0.01). ICU transfer occurred in 8.1% of the early group and 15.3% of the delayed group.

Conclusions: Early antibiotic administration in community-acquired pneumonia was associated with reduced mortality and shorter hospital stay. These findings support current guideline recommendations for prompt empiric antibiotic therapy in suspected CAP.`,
  },
  {
    label: "Discharge summary (synthetic)",
    text: `DISCHARGE SUMMARY

Admission Diagnosis: Acute exacerbation of congestive heart failure
Discharge Diagnosis: Congestive heart failure, NYHA Class III; Type 2 diabetes mellitus; Hypertension

Hospital Course: Patient is a 71-year-old with a history of type 2 diabetes and hypertension admitted with worsening dyspnea and bilateral lower extremity edema. Initial BNP was elevated at 1450 pg/mL. Chest X-ray showed pulmonary vascular congestion. Patient was started on IV furosemide 40mg twice daily with good diuretic response, transitioned to oral furosemide 40mg daily prior to discharge. Echocardiogram showed reduced ejection fraction of 35%. Lisinopril was initiated at 5mg daily and metoprolol succinate 25mg daily was started once euvolemic. Blood glucose was managed with metformin 500mg twice daily, continued from home regimen.

Discharge Medications: Furosemide 40mg daily, Lisinopril 5mg daily, Metoprolol succinate 25mg daily, Metformin 500mg twice daily, Aspirin 81mg daily

Discharge Instructions: Daily weights, low-sodium diet, follow up with cardiology in 1 week and primary care in 2 weeks. Return to ED for weight gain over 3 lbs in one day or worsening shortness of breath.`,
  },
];
