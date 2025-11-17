package com.gnegdev.vivida.service.data;

import com.gnegdev.vivida.data.dto.CreateUserRequest;
import com.gnegdev.vivida.data.entity.User;
import com.gnegdev.vivida.service.data.repository.UserRepository;
import com.gnegdev.vivida.util.mapper.UserMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final UserMapper userMapper;
    private final PasswordEncoder passwordEncoder;

    public User createUser(CreateUserRequest createUserRequest) {
        User user = userMapper.toEntity(createUserRequest);
        user.setPassword(passwordEncoder.encode(createUserRequest.password()));

        return userRepository.save(user);
    }

    public Optional<User> getUserByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    public Optional<User> getUserById(UUID id) {
        return userRepository.findById(id);
    }

    public User getUserReferenceById(UUID id) {
        return userRepository.getReferenceById(id);
    }
}
