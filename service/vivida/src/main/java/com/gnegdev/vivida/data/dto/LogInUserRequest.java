package com.gnegdev.vivida.data.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

public record LogInUserRequest(
    @NotBlank
    String email,
    @NotBlank
    String password
) {
}
