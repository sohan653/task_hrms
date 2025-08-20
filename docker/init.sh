#!/bin/bash
export PATH="${NVM_DIR}/versions/node/v${NODE_VERSION_DEVELOP}/bin/:${PATH}"
cd frappe-bench

wait_for_mariadb() {
    echo "Waiting for MariaDB to be ready..."
    max_attempts=30
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if mysql -h mariadb -u root -p123 -e "SELECT 1" > /dev/null 2>&1; then
            echo "MariaDB is ready!"
            return 0
        fi
        
        echo "Attempt $attempt/$max_attempts: MariaDB not ready yet, waiting 5 seconds..."
        sleep 5
        ((attempt++))
    done
    
    echo "ERROR: MariaDB failed to become ready after $max_attempts attempts"
    exit 1
}

wait_for_redis() {
    echo "Waiting for Redis to be ready..."
    max_attempts=30
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        # Check if we can establish a basic TCP connection
        if timeout 5 bash -c "</dev/tcp/redis/6379" 2>/dev/null; then
            echo "Redis is ready!"
            return 0
        fi
        
        echo "Attempt $attempt/$max_attempts: Redis not ready yet, waiting 2 seconds..."
        sleep 2
        ((attempt++))
    done
    
    echo "ERROR: Redis failed to become ready after $max_attempts attempts"
    exit 1
}

wait_for_mariadb
wait_for_redis

bench set-mariadb-host mariadb
bench set-redis-cache-host redis://redis:6379
bench set-redis-queue-host redis://redis:6379
bench set-redis-socketio-host redis://redis:6379

# Check if site exists
if [ -d "sites/hrms.localhost" ]; then
    echo "Site hrms.localhost already exists. Skipping site creation."
else
    echo "Site hrms.localhost does not exist. Creating site..."
    
    create_site_with_retry() {
        local max_attempts=3
        local attempt=1
        
        while [ $attempt -le $max_attempts ]; do
            echo "Creating site (attempt $attempt/$max_attempts)..."
            
            if bench new-site hrms.localhost \
                --force \
                --mariadb-root-password 123 \
                --admin-password admin \
                --no-mariadb-socket; then
                echo "Site created successfully!"
                return 0
            fi
            
            echo "Site creation failed, waiting 10 seconds before retry..."
            sleep 10
            ((attempt++))
        done
        
        echo "ERROR: Failed to create site after $max_attempts attempts"
        exit 1
    }
    
    create_site_with_retry
    
    echo "Installing ERPNext..."
    bench --site hrms.localhost install-app erpnext
    
    echo "Installing task_hrms..."
    bench --site hrms.localhost install-app task_hrms
fi

# Always set these configurations (in case they changed)
bench --site hrms.localhost set-config developer_mode 1
bench --site hrms.localhost clear-cache
bench use hrms.localhost

# Create Procfile if it doesn't exist
if [ ! -f "Procfile" ]; then
    echo "Creating Procfile..."
    cat > Procfile << EOF
web: bench serve --port 8000
worker: bench worker --queue default,long,short
schedule: bench schedule
EOF
else
    echo "Procfile already exists. Skipping creation."
fi

echo "Starting Frappe/ERPNext server..."
# Start the web server directly without Procfile
exec bench serve --port 8000