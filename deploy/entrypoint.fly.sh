#!/bin/bash

# Fly.io optimized Django entrypoint script
# This script runs at container startup on Fly.io

set -e

echo "🛩️ Starting Django application on Fly.io..."

# Function to run Django management commands
run_django_commands() {
    echo "📦 Collecting static files..."
    python manage.py collectstatic --noinput

    echo "🔍 Running Django system checks..."
    python manage.py check
    
    echo "✅ Django setup complete!"
}

# Function to handle database location for Fly.io persistent storage
setup_database() {
    # If we have a mounted volume, use it for the database
    if [ -d "/app/data" ] && [ -w "/app/data" ]; then
        echo "📁 Using persistent storage for database..."
        # Create symlink if database doesn't exist in mounted volume
        if [ ! -f "/app/data/running.db" ] && [ -f "/app/running.db" ]; then
            echo "🔄 Moving database to persistent storage..."
            cp /app/running.db /app/data/running.db
        fi
        # Always use the persistent database
        if [ ! -L "/app/running.db" ]; then
            rm -f /app/running.db
            ln -s /app/data/running.db /app/running.db
        fi
    else
        echo "⚠️  No persistent storage detected, using ephemeral database"
    fi
}

# Main execution
main() {
    setup_database
    run_django_commands
    
    echo "🚀 Starting Gunicorn server for Fly.io..."
    
    # Start Gunicorn with Fly.io optimized settings
    exec gunicorn \
        --bind 0.0.0.0:8000 \
        --workers 2 \
        --worker-class sync \
        --worker-connections 1000 \
        --max-requests 1000 \
        --max-requests-jitter 100 \
        --timeout 30 \
        --keep-alive 2 \
        --access-logfile - \
        --error-logfile - \
        --log-level info \
        whsxc.wsgi:application
}

# Run main function
main "$@"