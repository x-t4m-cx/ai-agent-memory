package com.agentmemory.user_project_service.repository;

import com.agentmemory.user_project_service.entity.AgentProject;
import com.agentmemory.user_project_service.entity.id.AgentProjectId;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface AgentProjectRepository
        extends JpaRepository<AgentProject, AgentProjectId> {

    List<AgentProject> findAllByAgent_Id(UUID agentId);

    List<AgentProject> findAllByProject_Id(UUID projectId);

    boolean existsByAgent_IdAndProject_Id(UUID agentId, UUID projectId);

    void deleteByAgent_IdAndProject_Id(UUID agentId, UUID projectId);
}