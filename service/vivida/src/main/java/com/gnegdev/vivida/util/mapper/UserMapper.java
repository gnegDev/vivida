package com.gnegdev.vivida.util.mapper;

import com.gnegdev.vivida.data.dto.CreateUserRequest;
import com.gnegdev.vivida.data.entity.User;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface UserMapper {
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "patientClinicalProfiles",  ignore = true)
    User toEntity(CreateUserRequest userDto);

//    CreateUserRequest toDto(User user);
}