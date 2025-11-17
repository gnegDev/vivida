package com.gnegdev.vivida.controller;

import com.gnegdev.vivida.data.dto.CreateUserRequest;
import com.gnegdev.vivida.data.dto.LogInUserRequest;
import com.gnegdev.vivida.data.entity.User;
import com.gnegdev.vivida.service.auth.AuthService;
import com.gnegdev.vivida.service.data.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@RestController
@RequestMapping("/vivida/api/auth")
@RequiredArgsConstructor
public class AuthController {
    private final UserService userService;
    private final AuthService authService;

    @PostMapping("/signin")
    public ResponseEntity<User> createUser(@Valid @RequestBody CreateUserRequest createUserRequest) {
        User user = userService.createUser(createUserRequest);
        return new ResponseEntity<>(user, HttpStatus.CREATED);
    }

    @PostMapping("/login")
    public ResponseEntity<?> logInUser(@Valid @RequestBody LogInUserRequest logInUserRequest) {
        Optional<User> user = userService.getUserByEmail(logInUserRequest.email());

        if (user.isEmpty() || !authService.checkPassword(logInUserRequest.password(), user.get().getPassword())) {
            return new ResponseEntity<>("Incorrect login or password", HttpStatus.UNAUTHORIZED);
        } else {
            return new ResponseEntity<>(user, HttpStatus.OK);
        }
    }
}
