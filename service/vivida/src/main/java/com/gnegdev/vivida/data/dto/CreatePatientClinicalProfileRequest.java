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
        String neurologicalSymptoms,

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

        @JsonProperty("chemotherapy")
        ChemotherapyTreatmentProfileDto chemotherapyTreatmentProfile,

        @JsonProperty("radiotherapy")
        RadiotherapyTreatmentProfileDto radiotherapyTreatmentProfile
) {
}
