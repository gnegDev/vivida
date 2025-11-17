package com.gnegdev.vivida.service.data.repository;

import com.gnegdev.vivida.data.entity.PatientClinicalProfile;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface PatientClinicalProfileRepository extends JpaRepository<PatientClinicalProfile, UUID> {
}