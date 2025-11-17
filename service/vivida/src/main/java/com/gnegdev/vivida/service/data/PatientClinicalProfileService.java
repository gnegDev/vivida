package com.gnegdev.vivida.service.data;

import com.gnegdev.vivida.data.dto.CreatePatientClinicalProfileRequest;
import com.gnegdev.vivida.data.entity.PatientClinicalProfile;
import com.gnegdev.vivida.data.entity.User;
import com.gnegdev.vivida.service.data.repository.PatientClinicalProfileRepository;
import com.gnegdev.vivida.util.mapper.PatientClinicalProfileMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Slf4j
@Repository
@RequiredArgsConstructor
public class PatientClinicalProfileService {
    private final PatientClinicalProfileRepository patientClinicalProfileRepository;
    private final PatientClinicalProfileMapper patientClinicalProfileMapper;
    private final UserService userService;

    public PatientClinicalProfile createPatientClinicalProfile(CreatePatientClinicalProfileRequest request) {
        PatientClinicalProfile patientClinicalProfile = patientClinicalProfileMapper.toEntity(request);
        User user = userService.getUserReferenceById(request.user_id());

        patientClinicalProfile.setUser(user);

        log.info("Converted DTO:\n{}\nto entity:\n{}", request, patientClinicalProfile);

        return patientClinicalProfileRepository.save(patientClinicalProfile);
    }

    public Optional<PatientClinicalProfile> getPatientClinicalProfileById(UUID id) {
        return patientClinicalProfileRepository.findById(id);
    }
}
