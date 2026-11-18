
-- Создание отдельных ролей для микросервисов.

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'user_project_app') THEN
        CREATE ROLE user_project_app WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'embedding_app') THEN
        CREATE ROLE embedding_app WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anonymization_app') THEN
        CREATE ROLE anonymization_app WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'conversation_memory_app') THEN
        CREATE ROLE conversation_memory_app WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'search_warmup_app') THEN
        CREATE ROLE search_warmup_app WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'platform_app') THEN
        CREATE ROLE platform_app WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
    END IF;
END
$$;

-- Пароли будут подставлены локально из .env перед выполнением.
ALTER ROLE user_project_app PASSWORD '__USER_PROJECT_DB_PASSWORD__';
ALTER ROLE embedding_app PASSWORD '__EMBEDDING_DB_PASSWORD__';
ALTER ROLE anonymization_app PASSWORD '__ANONYMIZATION_DB_PASSWORD__';
ALTER ROLE conversation_memory_app PASSWORD '__CONVERSATION_MEMORY_DB_PASSWORD__';
ALTER ROLE search_warmup_app PASSWORD '__SEARCH_WARMUP_DB_PASSWORD__';
ALTER ROLE platform_app PASSWORD '__PLATFORM_DB_PASSWORD__';

-- Назначение владельцев баз данных.
ALTER DATABASE user_project_db OWNER TO user_project_app;
ALTER DATABASE embedding_db OWNER TO embedding_app;
ALTER DATABASE anonymization_db OWNER TO anonymization_app;
ALTER DATABASE conversation_memory_db OWNER TO conversation_memory_app;
ALTER DATABASE search_warmup_db OWNER TO search_warmup_app;
ALTER DATABASE platform_db OWNER TO platform_app;

-- Запрещаем подключение и временные таблицы для PUBLIC.
REVOKE CONNECT, TEMP ON DATABASE user_project_db FROM PUBLIC;
REVOKE CONNECT, TEMP ON DATABASE embedding_db FROM PUBLIC;
REVOKE CONNECT, TEMP ON DATABASE anonymization_db FROM PUBLIC;
REVOKE CONNECT, TEMP ON DATABASE conversation_memory_db FROM PUBLIC;
REVOKE CONNECT, TEMP ON DATABASE search_warmup_db FROM PUBLIC;
REVOKE CONNECT, TEMP ON DATABASE platform_db FROM PUBLIC;

-- Разрешаем подключение только соответствующим сервисным пользователям.
GRANT CONNECT ON DATABASE user_project_db TO user_project_app;
GRANT CONNECT ON DATABASE embedding_db TO embedding_app;
GRANT CONNECT ON DATABASE anonymization_db TO anonymization_app;
GRANT CONNECT ON DATABASE conversation_memory_db TO conversation_memory_app;
GRANT CONNECT ON DATABASE search_warmup_db TO search_warmup_app;
GRANT CONNECT ON DATABASE platform_db TO platform_app;