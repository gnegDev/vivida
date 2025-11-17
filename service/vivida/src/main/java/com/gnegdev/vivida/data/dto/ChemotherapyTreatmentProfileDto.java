package com.gnegdev.vivida.data.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record ChemotherapyTreatmentProfileDto(
        String drug,

        @JsonProperty("dose_mg_per_m2")
        Float dose,

        @JsonProperty("interval_days")
        Integer intervalDays,

        Integer cycles
) {
}