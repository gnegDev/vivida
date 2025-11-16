package com.gnegdev.vivida.data.entity;

import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.UUID;

@Getter
@Setter
@Entity
@Table(name = "patient_chemo_regimen")
public class PatientChemoRegimen {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", nullable = false)
    private UUID id;

    @OneToOne(mappedBy = "patientChemoRegimen", optional = false, orphanRemoval = true)
    @JsonBackReference
    private PatientClinicalProfile patientClinicalProfile;


}