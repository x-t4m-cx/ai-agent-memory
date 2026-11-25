package com.agentmemory.user_project_service.entity;

import com.agentmemory.user_project_service.entity.id.AgentProjectId;
import jakarta.persistence.*;

import java.time.Instant;

@Entity
@Table(name = "agent_projects")
public class AgentProject {

    @EmbeddedId
    private AgentProjectId id;

    @ManyToOne(fetch = FetchType.LAZY)
    @MapsId("agentId")
    @JoinColumn(name = "agent_id", nullable = false)
    private Agent agent;

    @ManyToOne(fetch = FetchType.LAZY)
    @MapsId("projectId")
    @JoinColumn(name = "project_id", nullable = false)
    private Project project;

    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    protected AgentProject() {
    }
    public AgentProject(Agent agent, Project project) {
        this.agent = agent;
        this.project = project;
    }

    @PrePersist
    protected void onCreate() {
        createdAt = Instant.now();
    }

    public AgentProjectId getId() {
        return id;
    }

    public Agent getAgent() {
        return agent;
    }

    public Project getProject() {
        return project;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }
}