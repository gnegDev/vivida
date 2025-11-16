package com.gnegdev.vivida.controller;

import com.gnegdev.vivida.data.dto.CreatePatientClinicalProfileRequest;
import com.gnegdev.vivida.data.entity.PatientClinicalProfile;
import com.gnegdev.vivida.service.data.PatientClinicalProfileService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/vivida/api/patient")
@RequiredArgsConstructor
public class PatientClinicalProfileController {
    private final PatientClinicalProfileService patientClinicalProfileService;

    @PostMapping("/create")
    public ResponseEntity<PatientClinicalProfile> createPatientClinicalProfile(@RequestBody CreatePatientClinicalProfileRequest request) {

        PatientClinicalProfile patientClinicalProfile = patientClinicalProfileService.createPatientClinicalProfile(request);

        return new ResponseEntity<>(patientClinicalProfile, HttpStatus.CREATED);
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> getPatientClinicalProfileById(@PathVariable UUID id) {
        Optional<PatientClinicalProfile> patientClinicalProfile = patientClinicalProfileService.getPatientClinicalProfileById(id);

        if (patientClinicalProfile.isPresent()) {
            return new ResponseEntity<>(patientClinicalProfile.get(), HttpStatus.OK);
        }
        return new ResponseEntity<>("Patient not found with id: " + id, HttpStatus.NOT_FOUND);
    }}
