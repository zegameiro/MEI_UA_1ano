DO
$$
BEGIN
   -- Check if the user exists before creating it
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = 'taskflow_admin_user'
   ) THEN
      CREATE USER taskflow_admin_user WITH SUPERUSER PASSWORD 'taskflow_admin_password';
   END IF;
END
$$;

DO
$$
BEGIN
   -- Check if the database exists before creating it
   IF NOT EXISTS (
      SELECT FROM pg_database
      WHERE datname = 'taskflow_db'
   ) THEN
      CREATE DATABASE taskflow_db;
   END IF;
END
$$;
