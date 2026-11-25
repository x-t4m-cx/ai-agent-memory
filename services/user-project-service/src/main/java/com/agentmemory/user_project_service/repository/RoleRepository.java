package com.agentmemory.user_project_service.repository;

import com.agentmemory.user_project_service.entity.Role;
import com.agentmemory.user_project_service.entity.enums.RoleName;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface RoleRepository extends JpaRepository<Role, UUID> {

    Optional<Role> findByName(RoleName name);
}