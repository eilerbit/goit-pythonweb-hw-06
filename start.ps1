$containerName = "hw6-postgres"
$password = "1234test"

if (docker ps -a --format "{{.Names}}" | Select-String -Pattern "^$containerName$") {
    Write-Host "Container already exists. Starting it..."
    docker start $containerName
} else {
    Write-Host "Creating and running new PostgreSQL container..."
    docker run --name $containerName -p 5432:5432 -e POSTGRES_PASSWORD=$password -d postgres
}

# Initialize Alembic only if migrations directory does not exist
if (!(Test-Path "./migrations")) {
    Write-Host "Initializing Alembic migrations..."
    alembic init migrations
}

# Generate and apply migrations explicitly
Write-Host "Generating migrations and upgrading database..."
alembic revision --autogenerate -m "Auto migration"
alembic upgrade head

# Seed the database with fake data
python seed.py
