package com.gnegdev.vivida.data.entity;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.gnegdev.vivida.data.*;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

@Getter
@Setter
@ToString
@Entity
@Table(name = "patient_clinical_profile")
public class PatientClinicalProfile {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id", nullable = false)
    private UUID id;

    @ManyToOne
    @JoinColumn(name = "user_id")
    @JsonBackReference
    private User user;

    @OneToOne(cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "patient_chemo_regimen_id")
    @JsonManagedReference
    @JsonProperty("patient_chemo_regimen")
    private PatientClinicalRegimen patientClinicalRegimen;

    @Column(name = "stage", nullable = false)
    private Integer stage;

    @Column(name = "age", nullable = false)
    private Integer age;

    @Column(name = "gender", nullable = false)
    private String gender;

    @Column(name = "family_history", nullable = false)
    @JsonProperty("family_history")
    private Boolean familyHistory = false;

    @Column(name = "previous_radiation", nullable = false)
    @JsonProperty("previous_radiation")
    private Boolean previousRadiation = false;

    @Column(name = "tumor_location", nullable = false)
    @JsonProperty("tumor_location")
    private String tumorLocation;

    @Enumerated(EnumType.STRING)
    @Column(name = "lateralization", nullable = false)
    private Lateralization lateralization;

    @Column(name = "mgmt_methylation", nullable = false)
    @JsonProperty("mgmt_methylation")
    private Boolean mgmtMethylation = false;

    @Column(name = "idh_mutation", nullable = false)
    @JsonProperty("idh_mutation")
    private Boolean idhMutation = false;

    @Column(name = "egfr_amplification", nullable = false)
    @JsonProperty("egfr_amplification")
    private Boolean egfrAmplification = false;

    @Column(name = "tert_mutation", nullable = false)
    @JsonProperty("tert_mutation")
    private Boolean tertMutation = false;

    @Column(name = "atrx_mutation", nullable = false)
    @JsonProperty("atrx_mutation")
    private Boolean atrxMutation = false;

    @Enumerated(EnumType.STRING)
    @Column(name = "molecular_subtype", nullable = false)
    @JsonProperty("molecular_subtype")
    private MolecularSubtype molecularSubtype;

    @Column(name = "kps", nullable = false)
    private Integer kps;

    @Column(name = "neurological_symptoms")
    @JsonProperty("neurological_symptoms")
    private String neurologicalSymptoms;

    @Column(name = "treatment", nullable = false)
    private String treatment;

    @Enumerated(EnumType.STRING)
    @Column(name = "resection_extent", nullable = false)
    @JsonProperty("resection_extent")
    private ResectionExtent resectionExtent;

    @Column(name = "tumor_size_before", nullable = false)
    @JsonProperty("tumor_size_before")
    private Double tumorSizeBefore;

    @Column(name = "edema_volume", nullable = false)
    @JsonProperty("edema_volume")
    private Double edemaVolume;

    @Enumerated(EnumType.STRING)
    @Column(name = "contrast_enhancement", nullable = false)
    @JsonProperty("contrast_enhancement")
    private ContrastEnhancement contrastEnhancement;

    @Column(name = "steroid_dose", nullable = false)
    @JsonProperty("steroid_dose")
    private Double steroidDose;

    @Column(name = "antiseizure_meds", nullable = false)
    @JsonProperty("antiseizure_meds")
    private Boolean antiseizureMeds = false;

    @Enumerated(EnumType.STRING)
    @Column(name = "functional_status", nullable = false)
    @JsonProperty("functional_status")
    private FunctionalStatus functionalStatus;

    @Embedded
    @JsonProperty("chemotherapy_treatment_profile")
    private ChemotherapyTreatmentProfile chemotherapyTreatmentProfile;

    @Embedded
    @JsonProperty("radiotherapy_treatment_profile")
    private RadiotherapyTreatmentProfile radiotherapyTreatmentProfile;
}