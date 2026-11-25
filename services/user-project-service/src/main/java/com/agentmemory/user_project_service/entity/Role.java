package com.agentmemory.user_project_service.entity;

import com.agentmemory.user_project_service.entity.enums.RoleName;
import jakarta.persistence.*;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

@Entity
@Table(name = "roles")
public class Role {

    @Id
    private UUID id;

    @Enumerated(EnumType.STRING)
    @Column(name = "name", nullable = false, unique = true, length = 32)
    private RoleName name;

    @ManyToMany(mappedBy = "roles")
    private Set<User> users = new HashSet<>();

    protected Role() {
    }

    public UUID getId() {
        return id;
    }

    public RoleName getName() {
        return name;
    }

    public Set<User> getUsers() {
        return users;
    }
}