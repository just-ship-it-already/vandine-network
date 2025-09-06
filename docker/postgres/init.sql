-- PostgreSQL initialization script
-- This runs when the PostgreSQL container is first created

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Create database for Django (if not exists)
SELECT 'CREATE DATABASE vandine_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'vandine_db')\gexec

-- Grant all privileges to the application user
GRANT ALL PRIVILEGES ON DATABASE vandine_db TO vandine_user;

-- Connect to the application database
\c vandine_db;

-- Create a schema for better organization
CREATE SCHEMA IF NOT EXISTS monitoring;

-- Set search path
ALTER DATABASE vandine_db SET search_path TO public, monitoring;

-- Create initial tables for performance
CREATE TABLE IF NOT EXISTS monitoring.health_checks (
    id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    response_time_ms INTEGER,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details JSONB
);

CREATE INDEX idx_health_checks_service_time ON monitoring.health_checks(service_name, checked_at DESC);

-- Create table for storing network scan results
CREATE TABLE IF NOT EXISTS monitoring.network_scans (
    id SERIAL PRIMARY KEY,
    device_ip INET NOT NULL,
    device_name VARCHAR(255),
    scan_type VARCHAR(50),
    scan_results JSONB,
    scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_network_scans_device_time ON monitoring.network_scans(device_ip, scanned_at DESC);

-- Performance tuning for monitoring workload
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET random_page_cost = 1.1;

-- Log slow queries for optimization
ALTER SYSTEM SET log_min_duration_statement = '1000';

-- Apply configuration changes
SELECT pg_reload_conf();