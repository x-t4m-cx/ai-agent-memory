package com.agentmemory.user_project_service.repository;

import com.agentmemory.user_project_service.entity.ProjectMember;
import com.agentmemory.user_project_service.entity.id.ProjectMemberId;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.UUID;

public interface ProjectMemberRepository
        extends JpaRepository<ProjectMember, ProjectMemberId> {

    List<ProjectMember> findAllByProject_Id(UUID projectId);

    List<ProjectMember> findAllByUser_Id(UUID userId);

    boolean existsByProject_IdAndUser_Id(UUID projectId, UUID userId);

    void deleteByProject_IdAndUser_Id(UUID projectId, UUID userId);
}