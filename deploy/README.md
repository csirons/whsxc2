# WHSXC Django Application

A Django application for Widefield High School Cross Country, deployed on Fly.io.

## 🚀 Deployment

### Prerequisites

Install Fly.io CLI:
```bash
# macOS
brew install flyctl

# Linux/Windows
curl -L https://fly.io/install.sh | sh
```

Login to Fly.io:
```bash
fly auth login
```

### Initial Setup

For first-time deployment or creating new environments:
```bash
./deploy/deploy-fly.sh
```

### Deploy Updates

For day-to-day deployments (code changes, bug fixes, new features):
```bash
fly deploy --local-only
```

## 🌐 Access Your App

- **Website**: https://whsxc.fly.dev
- **Admin**: https://whsxc.fly.dev/admin/

## 🔧 Management

### Create Admin User
```bash
fly ssh console -C "python manage.py createsuperuser --settings=whsxc.settings_fly"
```

### View Logs
```bash
fly logs -f
```

### SSH Access
```bash
fly ssh console
```

### Deploy Updates
```bash
fly deploy --local-only
```

### Custom Domains (Optional)
```bash
fly certs create whsxc.com
fly certs create dev.whsxc.com
```

Then update your DNS records with the IP from:
```bash
fly ips list
```

## 💰 Costs

This app is configured to use Fly.io's free tier:
- Scales to zero when not in use
- 256MB RAM
- 1GB persistent storage

For small to medium traffic, this should cost $0/month.

## 📊 Monitoring

Check app status:
```bash
fly status
```

View dashboard:
```bash
fly dashboard
```

Scale instances:
```bash
fly scale count 2    # Scale up
fly scale count 0    # Scale to zero
```

## 📋 When to Use Each Command

### Use `./deploy/deploy-fly.sh` for:
- **Initial setup** - First time deploying the app
- **New environments** - Creating staging, testing, or production instances  
- **Different accounts** - Deploying to a teammate's Fly.io account
- **Starting over** - After destroying and recreating the app
- **Different regions** - Deploying to a new geographic region

### Use `fly deploy --local-only` for:
- **Code updates** - New features, bug fixes, improvements
- **Settings changes** - Updating Django configuration
- **Daily development** - Regular deployment workflow
- **Quick iterations** - Testing changes in production

**Rule of thumb**: Use the deploy script to "set up a new restaurant", use `fly deploy` to "cook new dishes in the existing restaurant".
