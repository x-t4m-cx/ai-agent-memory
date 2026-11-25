package com.agentmemory.user_project_service.repository;

import com.agentmemory.user_project_service.entity.Agent;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface AgentRepository extends JpaRepository<Agent, UUID> {

    Optional<Agent> findByApiKeyHash(String apiKeyHash);

    boolean existsByApiKeyHash(String apiKeyHash);
}