package com.gnegdev.vivida.util.mapper;

import com.gnegdev.vivida.data.dto.ChemotherapyTreatmentProfileDto;
import com.gnegdev.vivida.data.dto.CreatePatientClinicalProfileRequest;
import com.gnegdev.vivida.data.dto.PatientClinicalRegimentResponse;
import com.gnegdev.vivida.data.dto.RadiotherapyTreatmentProfileDto;
import com.gnegdev.vivida.data.entity.ChemotherapyTreatmentProfile;
import com.gnegdev.vivida.data.entity.PatientClinicalProfile;
import com.gnegdev.vivida.data.entity.PatientClinicalRegimen;
import com.gnegdev.vivida.data.entity.RadiotherapyTreatmentProfile;
import javax.annotation.processing.Generated;
import org.springframework.stereotype.Component;

@Generated(
    value = "org.mapstruct.ap.MappingProcessor",
    date = "2025-11-17T01:53:17+0300",
    comments = "version: 1.6.3, compiler: javac, environment: Java 24.0.2 (Oracle Corporation)"
)
@Component
public class PatientClinicalProfileMapperImpl implements PatientClinicalProfileMapper {

    @Override
    public PatientClinicalProfile toEntity(CreatePatientClinicalProfileRequest createPatientClinicalProfileRequest) {
        if ( createPatientClinicalProfileRequest == null ) {
            return null;
        }

        PatientClinicalProfile patientClinicalProfile = new PatientClinicalProfile();

        if ( createPatientClinicalProfileRequest.stage() != null ) {
            patientClinicalProfile.setStage( createPatientClinicalProfileRequest.stage() );
        }
        if ( createPatientClinicalProfileRequest.age() != null ) {
            patientClinicalProfile.setAge( createPatientClinicalProfileRequest.age() );
        }
        if ( createPatientClinicalProfileRequest.gender() != null ) {
            patientClinicalProfile.setGender( createPatientClinicalProfileRequest.gender() );
        }
        if ( createPatientClinicalProfileRequest.familyHistory() != null ) {
            patientClinicalProfile.setFamilyHistory( createPatientClinicalProfileRequest.familyHistory() );
        }
        if ( createPatientClinicalProfileRequest.previousRadiation() != null ) {
            patientClinicalProfile.setPreviousRadiation( createPatientClinicalProfileRequest.previousRadiation() );
        }
        if ( createPatientClinicalProfileRequest.tumorLocation() != null ) {
            patientClinicalProfile.setTumorLocation( createPatientClinicalProfileRequest.tumorLocation() );
        }
        if ( createPatientClinicalProfileRequest.lateralization() != null ) {
            patientClinicalProfile.setLateralization( createPatientClinicalProfileRequest.lateralization() );
        }
        if ( createPatientClinicalProfileRequest.mgmtMethylation() != null ) {
            patientClinicalProfile.setMgmtMethylation( createPatientClinicalProfileRequest.mgmtMethylation() );
        }
        if ( createPatientClinicalProfileRequest.idhMutation() != null ) {
            patientClinicalProfile.setIdhMutation( createPatientClinicalProfileRequest.idhMutation() );
        }
        if ( createPatientClinicalProfileRequest.egfrAmplification() != null ) {
            patientClinicalProfile.setEgfrAmplification( createPatientClinicalProfileRequest.egfrAmplification() );
        }
        if ( createPatientClinicalProfileRequest.tertMutation() != null ) {
            patientClinicalProfile.setTertMutation( createPatientClinicalProfileRequest.tertMutation() );
        }
        if ( createPatientClinicalProfileRequest.atrxMutation() != null ) {
            patientClinicalProfile.setAtrxMutation( createPatientClinicalProfileRequest.atrxMutation() );
        }
        if ( createPatientClinicalProfileRequest.molecularSubtype() != null ) {
            patientClinicalProfile.setMolecularSubtype( createPatientClinicalProfileRequest.molecularSubtype() );
        }
        if ( createPatientClinicalProfileRequest.kps() != null ) {
            patientClinicalProfile.setKps( createPatientClinicalProfileRequest.kps() );
        }
        if ( createPatientClinicalProfileRequest.neurologicalSymptoms() != null ) {
            patientClinicalProfile.setNeurologicalSymptoms( createPatientClinicalProfileRequest.neurologicalSymptoms() );
        }
        if ( createPatientClinicalProfileRequest.treatment() != null ) {
            patientClinicalProfile.setTreatment( createPatientClinicalProfileRequest.treatment() );
        }
        if ( createPatientClinicalProfileRequest.chemotherapyTreatmentProfile() != null ) {
            patientClinicalProfile.setChemotherapyTreatmentProfile( toEntity( createPatientClinicalProfileRequest.chemotherapyTreatmentProfile() ) );
        }
        if ( createPatientClinicalProfileRequest.radiotherapyTreatmentProfile() != null ) {
            patientClinicalProfile.setRadiotherapyTreatmentProfile( toEntity( createPatientClinicalProfileRequest.radiotherapyTreatmentProfile() ) );
        }
        if ( createPatientClinicalProfileRequest.resectionExtent() != null ) {
            patientClinicalProfile.setResectionExtent( createPatientClinicalProfileRequest.resectionExtent() );
        }
        if ( createPatientClinicalProfileRequest.tumorSizeBefore() != null ) {
            patientClinicalProfile.setTumorSizeBefore( createPatientClinicalProfileRequest.tumorSizeBefore() );
        }
        if ( createPatientClinicalProfileRequest.edemaVolume() != null ) {
            patientClinicalProfile.setEdemaVolume( createPatientClinicalProfileRequest.edemaVolume() );
        }
        if ( createPatientClinicalProfileRequest.contrastEnhancement() != null ) {
            patientClinicalProfile.setContrastEnhancement( createPatientClinicalProfileRequest.contrastEnhancement() );
        }
        if ( createPatientClinicalProfileRequest.steroidDose() != null ) {
            patientClinicalProfile.setSteroidDose( createPatientClinicalProfileRequest.steroidDose() );
        }
        if ( createPatientClinicalProfileRequest.antiseizureMeds() != null ) {
            patientClinicalProfile.setAntiseizureMeds( createPatientClinicalProfileRequest.antiseizureMeds() );
        }
        if ( createPatientClinicalProfileRequest.functionalStatus() != null ) {
            patientClinicalProfile.setFunctionalStatus( createPatientClinicalProfileRequest.functionalStatus() );
        }

        return patientClinicalProfile;
    }

    @Override
    public PatientClinicalRegimen toEntity(PatientClinicalRegimentResponse response) {
        if ( response == null ) {
            return null;
        }

        PatientClinicalRegimen patientClinicalRegimen = new PatientClinicalRegimen();

        if ( response.doctorPlan() != null ) {
            patientClinicalRegimen.setDoctorPlan( response.doctorPlan() );
        }
        if ( response.globalOptimal() != null ) {
            patientClinicalRegimen.setGlobalOptimal( response.globalOptimal() );
        }
        if ( response.localOptimal() != null ) {
            patientClinicalRegimen.setLocalOptimal( response.localOptimal() );
        }
        if ( response.recommendation() != null ) {
            patientClinicalRegimen.setRecommendation( response.recommendation() );
        }

        return patientClinicalRegimen;
    }

    @Override
    public ChemotherapyTreatmentProfile toEntity(ChemotherapyTreatmentProfileDto chemotherapyTreatmentProfile) {
        if ( chemotherapyTreatmentProfile == null ) {
            return null;
        }

        ChemotherapyTreatmentProfile chemotherapyTreatmentProfile1 = new ChemotherapyTreatmentProfile();

        if ( chemotherapyTreatmentProfile.drug() != null ) {
            chemotherapyTreatmentProfile1.setDrug( chemotherapyTreatmentProfile.drug() );
        }
        if ( chemotherapyTreatmentProfile.dose() != null ) {
            chemotherapyTreatmentProfile1.setDose( chemotherapyTreatmentProfile.dose() );
        }
        if ( chemotherapyTreatmentProfile.intervalDays() != null ) {
            chemotherapyTreatmentProfile1.setIntervalDays( chemotherapyTreatmentProfile.intervalDays() );
        }
        if ( chemotherapyTreatmentProfile.cycles() != null ) {
            chemotherapyTreatmentProfile1.setCycles( chemotherapyTreatmentProfile.cycles() );
        }

        return chemotherapyTreatmentProfile1;
    }

    @Override
    public RadiotherapyTreatmentProfile toEntity(RadiotherapyTreatmentProfileDto radiotherapyTreatmentProfileDto) {
        if ( radiotherapyTreatmentProfileDto == null ) {
            return null;
        }

        RadiotherapyTreatmentProfile radiotherapyTreatmentProfile = new RadiotherapyTreatmentProfile();

        if ( radiotherapyTreatmentProfileDto.totalDose() != null ) {
            radiotherapyTreatmentProfile.setTotalDose( radiotherapyTreatmentProfileDto.totalDose() );
        }
        if ( radiotherapyTreatmentProfileDto.fractionDose() != null ) {
            radiotherapyTreatmentProfile.setFractionDose( radiotherapyTreatmentProfileDto.fractionDose() );
        }
        if ( radiotherapyTreatmentProfileDto.fractions() != null ) {
            radiotherapyTreatmentProfile.setFractions( radiotherapyTreatmentProfileDto.fractions() );
        }

        return radiotherapyTreatmentProfile;
    }
}
