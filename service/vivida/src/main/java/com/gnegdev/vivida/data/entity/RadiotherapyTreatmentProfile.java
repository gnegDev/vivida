package com.gnegdev.vivida.data.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
@Embeddable
public class RadiotherapyTreatmentProfile {
    @Column(name = "total_dose")
    @JsonProperty("total_dose_Gy")
    private Float totalDose;

    @Column(name = "fraction_dose")
    @JsonProperty("fraction_dose_Gy")
    private Float fractionDose;

    @Column(name = "fractions")
    private Integer fractions;
}