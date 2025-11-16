package com.gnegdev.vivida.service.analysis;

import com.gnegdev.vivida.data.dto.PatientChemoRegimentResponse;
import com.gnegdev.vivida.data.entity.PatientClinicalProfile;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

@Service
public class AnalysisClient {
    @Value("${analysis.endpoint}")
    private String endpoint;

    private final RestClient restClient = RestClient.create();

    public PatientChemoRegimentResponse analyzePatientClinicalProfile(PatientClinicalProfile patientClinicalProfile) {
        ResponseEntity<PatientChemoRegimentResponse> response = restClient.post()
                .uri(endpoint + "/analyze")
                .contentType(MediaType.APPLICATION_JSON)
                .body(patientClinicalProfile)
                .retrieve()
                .toEntity(PatientChemoRegimentResponse.class);

        return response.getBody();
    }
}
