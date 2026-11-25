package com.agentmemory.user_project_service.entity.id;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;

import java.io.Serializable;
import java.util.Objects;
import java.util.UUID;

@Embeddable
public class AgentProjectId implements Serializable {

    @Column(name = "agent_id")
    private UUID agentId;

    @Column(name = "project_id")
    private UUID projectId;

    protected AgentProjectId() {
    }

    public AgentProjectId(UUID agentId, UUID projectId) {
        this.agentId = agentId;
        this.projectId = projectId;
    }

    public UUID getAgentId() {
        return agentId;
    }

    public UUID getProjectId() {
        return projectId;
    }

    @Override
    public boolean equals(Object object) {
        if (this == object) return true;
        if (!(object instanceof AgentProjectId that)) return false;
        return Objects.equals(agentId, that.agentId)
                && Objects.equals(projectId, that.projectId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(agentId, projectId);
    }
}