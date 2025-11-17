package com.gnegdev.vivida.data.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;

public record PatientClinicalRegimentResponse(
        @JsonProperty("doctor_plan")
        JsonNode doctorPlan,

        @JsonProperty("global_optimal")
        JsonNode globalOptimal,

        @JsonProperty("local_optimal")
        JsonNode localOptimal,

        String recommendation
) {
}
