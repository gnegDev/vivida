package com.gnegdev.vivida.service.analysis;

import com.gnegdev.vivida.data.dto.PatientClinicalRegimentResponse;
import com.gnegdev.vivida.data.entity.PatientClinicalProfile;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Slf4j
@Service
public class AnalysisClient {
    @Value("${analysis.endpoint}")
    private String endpoint;

    private final RestClient restClient = RestClient.create();

    public PatientClinicalRegimentResponse analyzePatientClinicalProfile(PatientClinicalProfile patientClinicalProfile) {
        log.info("Optimizing clinical regiment: {}", patientClinicalProfile.toString());

        ResponseEntity<PatientClinicalRegimentResponse> response = restClient.post()
                .uri(endpoint + "/optimize/summary")
                .contentType(MediaType.APPLICATION_JSON)
                .body(patientClinicalProfile)
                .retrieve()
                .toEntity(PatientClinicalRegimentResponse.class);

        return response.getBody();
    }
}
