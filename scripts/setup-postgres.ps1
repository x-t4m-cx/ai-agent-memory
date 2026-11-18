
$ErrorActionPreference = "Stop"

# Корневая директория проекта.
$projectRoot = Split-Path -Parent $PSScriptRoot

$envFile = Join-Path $projectRoot ".env"
$sqlFile = Join-Path $projectRoot "infrastructure/postgres/scripts/02-create-service-roles.sql"

# Проверяем наличие файлов.
if (-not (Test-Path $envFile)) {
    throw "Файл .env не найден: $envFile"
}

if (-not (Test-Path $sqlFile)) {
    throw "SQL-файл не найден: $sqlFile"
}

# Читаем переменные окружения.
$envValues = @{}

Get-Content $envFile | ForEach-Object {
    if ($_ -match '^([^#=]+)=(.*)$') {
        $envValues[$matches[1]] = $matches[2]
    }
}

# Проверяем необходимые пароли.
$passwordKeys = @(
    "USER_PROJECT_DB_PASSWORD",
    "EMBEDDING_DB_PASSWORD",
    "ANONYMIZATION_DB_PASSWORD",
    "CONVERSATION_MEMORY_DB_PASSWORD",
    "SEARCH_WARMUP_DB_PASSWORD",
    "PLATFORM_DB_PASSWORD"
)

foreach ($key in $passwordKeys) {
    if (-not $envValues.ContainsKey($key)) {
        throw "В .env отсутствует переменная $key"
    }

    if ($envValues[$key] -notmatch '^[a-f0-9]{48}$') {
        throw "Переменная $key имеет неверный формат."
    }
}

# Загружаем SQL и подставляем пароли.
$sql = Get-Content $sqlFile -Raw

foreach ($key in $passwordKeys) {
    $placeholder = "__${key}__"
    $sql = $sql.Replace($placeholder, $envValues[$key])
}

if ($sql -match '__[A-Z0-9_]+__') {
    throw "В SQL остались незаменённые шаблоны."
}

# Проверяем доступность контейнера.
docker inspect ai-memory-postgres --format '{{.State.Running}}' | Out-Null

if ($LASTEXITCODE -ne 0) {
    throw "Не удалось проверить контейнер PostgreSQL."
}

# Выполняем SQL.
Write-Host "Настройка PostgreSQL..." -ForegroundColor Cyan

$sql | docker exec -i ai-memory-postgres `
    psql -U memory_admin -d postgres -v ON_ERROR_STOP=1

if ($LASTEXITCODE -ne 0) {
    throw "Ошибка настройки PostgreSQL."
}

Write-Host "PostgreSQL успешно настроен." -ForegroundColor Green
