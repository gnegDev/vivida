package com.gnegdev.vivida.service.data.repository;

import com.gnegdev.vivida.data.entity.PatientChemoRegimen;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface PatientChemoRegimenRepository extends JpaRepository<PatientChemoRegimen, UUID> {
}