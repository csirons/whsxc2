#!/bin/bash

# Fly.io Deployment Script for Django Application
# This script automates the deployment of your Django app to Fly.io

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}[DEPLOY]${NC} $1"
}

# Configuration
FLY_APP_NAME="whsxc"
FLY_REGION="sjc"  # San Jose - change to your preferred region

echo "🛩️ Fly.io Django Deployment Script"
echo "===================================="
echo ""

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null && ! command -v fly &> /dev/null; then
    print_error "flyctl is not installed. Please install it first:"
    echo "  macOS: brew install flyctl"
    echo "  Linux: curl -L https://fly.io/install.sh | sh"
    echo "  Windows: powershell -Command \"iwr https://fly.io/install.ps1 -useb | iex\""
    echo ""
    echo "Then run: flyctl auth login"
    exit 1
fi

# Use 'fly' or 'flyctl' command
if command -v fly &> /dev/null; then
    FLY_CMD="fly"
else
    FLY_CMD="flyctl"
fi

print_status "Using command: $FLY_CMD"

# Check if user is logged in
if ! $FLY_CMD auth whoami &> /dev/null; then
    print_error "You are not logged in to Fly.io"
    print_status "Please run: $FLY_CMD auth login"
    exit 1
fi

print_success "Logged in to Fly.io as: $($FLY_CMD auth whoami)"

# Check if app exists
print_status "Checking if app '$FLY_APP_NAME' exists..."
if $FLY_CMD apps list | grep -q "^$FLY_APP_NAME "; then
    print_success "App '$FLY_APP_NAME' already exists"
    APP_EXISTS=true
else
    print_warning "App '$FLY_APP_NAME' does not exist"
    APP_EXISTS=false
fi

# Create app if it doesn't exist
if [ "$APP_EXISTS" = false ]; then
    print_status "Creating new Fly.io app '$FLY_APP_NAME'..."
    
    # Ask user to confirm app name
    read -p "App name '$FLY_APP_NAME' will be created in region '$FLY_REGION'. Continue? (y/N): " confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        print_error "Deployment cancelled by user"
        exit 1
    fi
    
    $FLY_CMD apps create $FLY_APP_NAME
    print_success "App '$FLY_APP_NAME' created successfully"
fi

# Generate a secure secret key if needed
print_status "Generating secure Django secret key..."
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Set environment variables/secrets
print_status "Setting up environment variables..."

# Essential secrets
$FLY_CMD secrets set SECRET_KEY="$SECRET_KEY" --app $FLY_APP_NAME
$FLY_CMD secrets set DEBUG=False --app $FLY_APP_NAME
$FLY_CMD secrets set DJANGO_SETTINGS_MODULE=whsxc.settings_fly --app $FLY_APP_NAME
$FLY_CMD secrets set FLY_APP_NAME=$FLY_APP_NAME --app $FLY_APP_NAME
$FLY_CMD secrets set DJANGO_LOG_LEVEL=INFO --app $FLY_APP_NAME

print_success "Environment variables set successfully"

# Create persistent volume for database
print_status "Setting up persistent storage..."
if ! $FLY_CMD volumes list --app $FLY_APP_NAME | grep -q "whsxc_data"; then
    print_status "Creating persistent volume for database..."
    $FLY_CMD volumes create whsxc_data --region $FLY_REGION --size 1 --app $FLY_APP_NAME
    print_success "Persistent volume 'whsxc_data' created"
else
    print_success "Persistent volume 'whsxc_data' already exists"
fi

# Update fly.toml with correct app name
print_status "Updating fly.toml configuration..."
sed -i.bak "s/app = \"whsxc\"/app = \"$FLY_APP_NAME\"/" fly.toml
sed -i.bak "s/primary_region = \"sjc\"/primary_region = \"$FLY_REGION\"/" fly.toml

# Deploy the application
print_header "Deploying application to Fly.io..."
$FLY_CMD deploy --app $FLY_APP_NAME

# Wait for deployment to complete
print_status "Waiting for deployment to complete..."
sleep 10

# Run database migrations
print_status "Running database migrations..."
$FLY_CMD ssh console --app $FLY_APP_NAME -C "python manage.py migrate --settings=whsxc.settings_fly"

# Create superuser (optional)
print_status "Setting up Django admin user..."
read -p "Create Django superuser? (y/N): " create_user
if [[ $create_user =~ ^[Yy]$ ]]; then
    read -p "Enter admin username (default: admin): " admin_user
    admin_user=${admin_user:-admin}
    
    read -p "Enter admin email: " admin_email
    if [ -z "$admin_email" ]; then
        admin_email="admin@${FLY_APP_NAME}.fly.dev"
    fi
    
    # Generate a temporary password
    temp_password=$(openssl rand -base64 12)
    
    print_status "Creating superuser '$admin_user'..."
    $FLY_CMD ssh console --app $FLY_APP_NAME -C "python manage.py shell --settings=whsxc.settings_fly -c \"
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$admin_user').exists():
    User.objects.create_superuser('$admin_user', '$admin_email', '$temp_password')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
\""
    
    print_success "Superuser '$admin_user' created with temporary password: $temp_password"
    print_warning "IMPORTANT: Change this password immediately after logging in!"
fi

# Set up custom domains (optional)
print_status "Setting up custom domains..."
read -p "Set up custom domains (whsxc.com, dev.whsxc.com)? (y/N): " setup_domains
if [[ $setup_domains =~ ^[Yy]$ ]]; then
    print_status "Adding custom domains..."
    
    # Add primary domain
    $FLY_CMD certs create whsxc.com --app $FLY_APP_NAME || true
    
    # Add dev domain  
    $FLY_CMD certs create dev.whsxc.com --app $FLY_APP_NAME || true
    
    print_success "Custom domains added. Update your DNS records:"
    echo ""
    echo "Add these DNS records to your domain:"
    echo "  whsxc.com        A     $(fly ips list --app $FLY_APP_NAME | grep -E "v4" | awk '{print $3}' | head -1)"
    echo "  dev.whsxc.com    A     $(fly ips list --app $FLY_APP_NAME | grep -E "v4" | awk '{print $3}' | head -1)"
    echo "  www.whsxc.com    CNAME whsxc.com"
    echo ""
    print_status "SSL certificates will be automatically generated once DNS propagates"
fi

# Display deployment information
echo ""
echo "=========================================="
print_success "🎉 Deployment Complete!"
echo "=========================================="
echo ""
print_status "Your Django application is now live:"
echo "  🌐 Default URL: https://${FLY_APP_NAME}.fly.dev"
echo "  🔧 Admin URL: https://${FLY_APP_NAME}.fly.dev/admin/"
echo ""

if [[ $setup_domains =~ ^[Yy]$ ]]; then
    echo "  🌐 Production: https://whsxc.com (after DNS setup)"
    echo "  🌐 Development: https://dev.whsxc.com (after DNS setup)"
    echo "  🔧 Admin: https://whsxc.com/admin/"
    echo ""
fi

if [[ $create_user =~ ^[Yy]$ ]]; then
    echo "  👤 Admin Username: $admin_user"
    echo "  🔐 Temporary Password: $temp_password"
    echo ""
    print_warning "Change the admin password immediately!"
fi

print_status "Useful commands:"
echo "  📊 View logs: $FLY_CMD logs --app $FLY_APP_NAME"
echo "  🔄 Redeploy: $FLY_CMD deploy --app $FLY_APP_NAME"
echo "  🖥️  SSH access: $FLY_CMD ssh console --app $FLY_APP_NAME"
echo "  📈 Monitoring: $FLY_CMD status --app $FLY_APP_NAME"
echo "  🔧 Django shell: $FLY_CMD ssh console --app $FLY_APP_NAME -C 'python manage.py shell --settings=whsxc.settings_fly'"
echo ""

print_status "App scaling:"
echo "  💪 Scale up: $FLY_CMD scale count 2 --app $FLY_APP_NAME"
echo "  💰 Scale down: $FLY_CMD scale count 1 --app $FLY_APP_NAME"
echo ""

print_success "Happy coding! 🚀"

# Clean up backup files
rm -f fly.toml.bak 2>/dev/null || true