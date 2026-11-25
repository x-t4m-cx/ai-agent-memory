package com.agentmemory.user_project_service.entity;

import jakarta.persistence.*;

import java.time.Instant;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

@Entity
@Table(name = "agents")
public class Agent {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "description")
    private String description;

    @Column(name = "api_key_hash", nullable = false, unique = true, length = 64)
    private String apiKeyHash;

    @Column(name = "api_key_prefix", nullable = false, length = 12)
    private String apiKeyPrefix;

    @Column(name = "api_key_created_at", nullable = false)
    private Instant apiKeyCreatedAt;

    @Column(name = "api_key_revoked_at")
    private Instant apiKeyRevokedAt;

    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @OneToMany(mappedBy = "agent", cascade = CascadeType.ALL, orphanRemoval = true)
    private Set<AgentProject> projects = new HashSet<>();

    protected Agent() {
    }

    public Agent(String name, String description,
                 String apiKeyHash, String apiKeyPrefix) {
        this.name = name;
        this.description = description;
        this.apiKeyHash = apiKeyHash;
        this.apiKeyPrefix = apiKeyPrefix;
    }

    @PrePersist
    protected void onCreate() {
        createdAt = Instant.now();
        apiKeyCreatedAt = Instant.now();
    }

    public boolean isApiKeyActive() {
        return apiKeyRevokedAt == null;
    }

    public void revokeApiKey() {
        apiKeyRevokedAt = Instant.now();
    }

    public void addProject(AgentProject agentProject) {
        projects.add(agentProject);
    }

    public UUID getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public String getApiKeyHash() {
        return apiKeyHash;
    }

    public String getApiKeyPrefix() {
        return apiKeyPrefix;
    }

    public Instant getApiKeyCreatedAt() {
        return apiKeyCreatedAt;
    }

    public Instant getApiKeyRevokedAt() {
        return apiKeyRevokedAt;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public Set<AgentProject> getProjects() {
        return projects;
    }
}