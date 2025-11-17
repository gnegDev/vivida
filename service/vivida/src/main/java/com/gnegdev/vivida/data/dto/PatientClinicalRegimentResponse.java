package com.gnegdev.vivida.data.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;
import jakarta.persistence.Column;

public record PatientClinicalRegimentResponse(
        @JsonProperty("doctor_plan")
        JsonNode doctorPlan,

        @Column(name = "global_optimal")
        @JsonProperty("global_optimal")
        JsonNode globalOptimal,

        @JsonProperty("local_optimal")
        JsonNode localOptimal,

        String recommendation
) {
}
