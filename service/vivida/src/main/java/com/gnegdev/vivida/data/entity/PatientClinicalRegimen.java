package com.gnegdev.vivida.data.entity;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.JsonNode;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.util.UUID;

@Getter
@Setter
@ToString
@Entity
@Table(name = "patient_chemo_regimen")
public class PatientClinicalRegimen {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", nullable = false)
    private UUID id;

    @OneToOne(mappedBy = "patientClinicalRegimen", optional = false, orphanRemoval = true)
    @JsonBackReference
    private PatientClinicalProfile patientClinicalProfile;

    @Column(name = "doctor_plan")
    @JdbcTypeCode(SqlTypes.JSON)
    @JsonProperty("doctor_plan")
    private JsonNode doctorPlan;

    @Column(name = "global_optimal")
    @JdbcTypeCode(SqlTypes.JSON)
    @JsonProperty("global_optimal")
    private JsonNode globalOptimal;

    @Column(name = "local_optimal")
    @JdbcTypeCode(SqlTypes.JSON)
    @JsonProperty("local_optimal")
    private JsonNode localOptimal;

    @Column(name = "recommendation")
    private String recommendation;

}