package com.gnegdev.vivida.data.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record RadiotherapyTreatmentProfileDto(
        @JsonProperty("total_dose_Gy")
        Float totalDose,

        @JsonProperty("fraction_dose_Gy")
        Float fractionDose,

        Integer fractions
) {
}
