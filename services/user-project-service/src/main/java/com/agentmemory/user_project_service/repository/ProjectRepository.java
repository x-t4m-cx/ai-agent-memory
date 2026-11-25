package com.agentmemory.user_project_service.repository;

import com.agentmemory.user_project_service.entity.Project;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface ProjectRepository extends JpaRepository<Project, UUID> {
}