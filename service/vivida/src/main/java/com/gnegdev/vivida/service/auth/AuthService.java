package com.gnegdev.vivida.service.auth;

import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthService {
//    private final UserService userService;
    private final PasswordEncoder passwordEncoder;

//    public Optional<User> logInUser(String email, String password) {
//        Optional<User> user = userService.getUserByEmail(email);
//        if (user.isEmpty()) {
//            return user;
//        } else if (checkPassword(password, user.get().getPassword())) {
//            return user;
//        } else
//
//    }

    public boolean checkPassword(String plainPassword, String hashedPassword) {
        return passwordEncoder.matches(plainPassword, hashedPassword);
    }

}
