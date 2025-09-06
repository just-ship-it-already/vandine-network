# Git Workflow & CI/CD Pipeline

## Branch Strategy

### Branch Structure
- **main** (production) - Protected, production-ready code
- **staging** - Pre-production testing environment
- **dev** - Active development branch
- **feature/** - Feature branches (created from dev)
- **hotfix/** - Emergency fixes (created from main)

## Deployment Environments

| Environment | Branch | URL | Auto-Deploy |
|------------|--------|-----|-------------|
| Development | dev | dev.rafael.vandine.us | Yes |
| Staging | staging | staging.rafael.vandine.us | Yes |
| Production | main | rafael.vandine.us | Yes (with approval) |

## GitHub Actions Workflows

### 1. Deploy Pipeline
Automatically deploys code when branches are updated

### 2. Monitoring
Hourly health checks of infrastructure

### 3. Auto Updates
Weekly dependency updates with PR creation

## Quick Start Commands

### Start developing a new feature:
git checkout dev
git pull origin dev
git checkout -b feature/my-feature
# Make changes
git add .
git commit -m "feat: description"
git push origin feature/my-feature

### Deploy to staging:
git checkout staging
git merge dev
git push origin staging

### Deploy to production:
git checkout main
git merge staging
git push origin main

## Best Practices
1. Never commit directly to main
2. Test in staging before production
3. Use semantic commit messages
4. Monitor deployments
