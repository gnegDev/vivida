package com.gnegdev.vivida.util.mapper;

import com.gnegdev.vivida.data.dto.CreateUserRequest;
import com.gnegdev.vivida.data.entity.User;
import javax.annotation.processing.Generated;
import org.springframework.stereotype.Component;

@Generated(
    value = "org.mapstruct.ap.MappingProcessor",
    date = "2025-11-17T01:15:21+0300",
    comments = "version: 1.6.3, compiler: javac, environment: Java 24.0.2 (Oracle Corporation)"
)
@Component
public class UserMapperImpl implements UserMapper {

    @Override
    public User toEntity(CreateUserRequest userDto) {
        if ( userDto == null ) {
            return null;
        }

        User user = new User();

        user.setName( userDto.name() );
        user.setEmail( userDto.email() );
        user.setPassword( userDto.password() );

        return user;
    }
}
