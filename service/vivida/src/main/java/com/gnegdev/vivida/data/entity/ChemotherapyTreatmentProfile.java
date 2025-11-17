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
public class ChemotherapyTreatmentProfile {
    @Column(name = "drug")
    private String drug;

    @Column(name = "dose")
    @JsonProperty("dose_mg_per_m2")
    private Float dose;

    @Column(name = "interval_days")
    @JsonProperty("interval_days")
    private Integer intervalDays;

    @Column(name = "cycles")
    private Integer cycles;

}