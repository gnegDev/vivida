package com.gnegdev.vivida.data.dto;

import com.gnegdev.vivida.data.*;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;
import java.util.UUID;

public record CreatePatientClinicalProfileRequest(
        UUID user_id,

        Integer stage,

        Integer age,

        String gender,

        @JsonProperty("family_history")
        Boolean familyHistory,

        @JsonProperty("previous_radiation")
        Boolean previousRadiation,

        @JsonProperty("tumor_location")
        String tumorLocation,

        Lateralization lateralization,

        @JsonProperty("mgmt_methylation")
        Boolean mgmtMethylation,

        @JsonProperty("idh_mutation")
        Boolean idhMutation,

        @JsonProperty("egfr_amplification")
        Boolean egfrAmplification,

        @JsonProperty("tert_mutation")
        Boolean tertMutation,

        @JsonProperty("atrx_mutation")
        Boolean atrxMutation,

        @JsonProperty("molecular_subtype")
        MolecularSubtype molecularSubtype,

        Integer kps,

        @JsonProperty("neurological_symptoms")
        List<String> neurologicalSymptoms,

        String treatment,

        @JsonProperty("resection_extent")
        ResectionExtent resectionExtent,

        @JsonProperty("tumor_size_before")
        Double tumorSizeBefore,

        @JsonProperty("edema_volume")
        Double edemaVolume,

        @JsonProperty("contrast_enhancement")
        ContrastEnhancement contrastEnhancement,

        @JsonProperty("steroid_dose")
        Double steroidDose,

        @JsonProperty("antiseizure_meds")
        Boolean antiseizureMeds,

        @JsonProperty("functional_status")
        FunctionalStatus functionalStatus,

        @JsonProperty("chemo_drug")
        String chemoDrug,

        @JsonProperty("chemo_dose_mg_per_m2")
        Float chemoDose,

        @JsonProperty("chemo_interval_days")
        Integer chemoIntervalDays,

        @JsonProperty("chemo_cycles")
        Integer chemoCycles,

        @JsonProperty("radiation_total_dose_Gy")
        Float radiationTotalDose,

        @JsonProperty("radiation_fraction_dose_Gy")
        Float radiationFractionDose,

        @JsonProperty("radiation_fractions")
        Integer radiationFractions
) {
}
