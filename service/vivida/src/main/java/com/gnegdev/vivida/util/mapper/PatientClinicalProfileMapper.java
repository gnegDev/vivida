package com.gnegdev.vivida.util.mapper;

import com.gnegdev.vivida.data.dto.CreatePatientClinicalProfileRequest;
import com.gnegdev.vivida.data.entity.PatientClinicalProfile;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.NullValueCheckStrategy;

@Mapper(componentModel = "spring", nullValueCheckStrategy = NullValueCheckStrategy.ALWAYS)
public interface PatientClinicalProfileMapper {

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "user", ignore = true)
    @Mapping(target = "patientChemoRegimen", ignore = true)
    PatientClinicalProfile toEntity(CreatePatientClinicalProfileRequest createPatientClinicalProfileRequest);

}
