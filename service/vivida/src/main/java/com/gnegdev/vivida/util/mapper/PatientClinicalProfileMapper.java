package com.gnegdev.vivida.util.mapper;

import com.gnegdev.vivida.data.dto.CreatePatientClinicalProfileRequest;
import com.gnegdev.vivida.data.dto.PatientClinicalRegimentResponse;
import com.gnegdev.vivida.data.entity.PatientClinicalProfile;
import com.gnegdev.vivida.data.entity.PatientClinicalRegimen;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.NullValueCheckStrategy;

@Mapper(componentModel = "spring", nullValueCheckStrategy = NullValueCheckStrategy.ALWAYS)
public interface PatientClinicalProfileMapper {

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "user", ignore = true)
    @Mapping(target = "patientClinicalRegimen", ignore = true)
    PatientClinicalProfile toEntity(CreatePatientClinicalProfileRequest request);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "patientClinicalProfile", ignore = true)
    PatientClinicalRegimen toEntity(PatientClinicalRegimentResponse response);

}
