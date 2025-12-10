# AWS Deployment Guide - Revenue Leakage Detection System

## Overview
This guide provides step-by-step instructions for deploying the Revenue Leakage Detection System to AWS.

## Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   CloudFront    │─────▶│   S3 Bucket      │      │   EC2/ECS       │
│   (Frontend)    │      │   (Static Files) │      │   (Backend)     │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                                            │
                                                            ▼
                                                    ┌─────────────────┐
                                                    │   RDS/SQLite    │
                                                    │   (Database)    │
                                                    └─────────────────┘
```

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Domain name (optional but recommended)
- Admin access to the application

## Part 1: Backend Deployment (FastAPI on EC2)

### Step 1: Prepare Backend for Production

1. **Update CORS Settings** (`backend/core/config.py`):
```python
ALLOWED_ORIGINS = [
    "https://your-domain.com",
    "https://www.your-domain.com",
    "http://localhost:5173",  # Keep for local testing
]
```

2. **Create Environment Variables File** (`backend/.env.production`):
```env
DATABASE_URL=sqlite:///./revenue_advisor.db
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

3. **Update requirements.txt** to include production dependencies:
```txt
# Existing dependencies...
gunicorn==21.2.0
uvicorn[standard]==0.24.0
python-multipart==0.0.6
```

### Step 2: Launch EC2 Instance

1. **Instance Configuration:**
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t2.medium (recommended) or t2.small (minimum)
   - Storage: 20GB EBS
   - Security Group:
     - Port 22 (SSH) - Your IP only
     - Port 8000 (HTTP) - Anywhere (0.0.0.0/0)
     - Port 443 (HTTPS) - Anywhere (0.0.0.0/0)

2. **Create and download key pair** (e.g., `revenue-backend-key.pem`)

### Step 3: Connect and Setup EC2

```bash
# Connect to EC2
ssh -i revenue-backend-key.pem ubuntu@your-ec2-public-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Install nginx (optional - for reverse proxy)
sudo apt install nginx -y

# Create application directory
sudo mkdir -p /var/www/revenue-backend
sudo chown ubuntu:ubuntu /var/www/revenue-backend
cd /var/www/revenue-backend

# Clone or upload your code
# Option 1: Git clone
git clone https://github.com/jAtInn71/Revenue_scan.git .

# Option 2: Manual upload
# Use SCP to upload files
# scp -i revenue-backend-key.pem -r backend ubuntu@your-ec2-ip:/var/www/revenue-backend/

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Create production env file
nano .env
# Paste your production environment variables

# Initialize database
python -c "from database.database import init_db; init_db()"

# Create demo/admin user
python create_demo_user.py
```

### Step 4: Configure Systemd Service

Create service file: `/etc/systemd/system/revenue-backend.service`

```ini
[Unit]
Description=Revenue Detection Backend
After=network.target

[Service]
Type=notify
User=ubuntu
WorkingDirectory=/var/www/revenue-backend/backend
Environment="PATH=/var/www/revenue-backend/venv/bin"
ExecStart=/var/www/revenue-backend/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable revenue-backend
sudo systemctl start revenue-backend
sudo systemctl status revenue-backend
```

### Step 5: Configure Nginx (Optional but Recommended)

Create nginx config: `/etc/nginx/sites-available/revenue-backend`

```nginx
server {
    listen 80;
    server_name api.your-domain.com;  # Use your domain

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Increase body size for file uploads
    client_max_body_size 100M;
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/revenue-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d api.your-domain.com
```

## Part 2: Frontend Deployment (React on S3 + CloudFront)

### Step 1: Prepare Frontend Build

1. **Update API endpoint** (`frontend/src/services/api.js`):
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'https://api.your-domain.com/api';
```

2. **Create environment file** (`frontend/.env.production`):
```env
VITE_API_URL=https://api.your-domain.com/api
```

3. **Build the application:**
```bash
cd frontend
npm install
npm run build
```

This creates a `dist` folder with optimized static files.

### Step 2: Create S3 Bucket

1. Go to AWS S3 Console
2. Create bucket:
   - Name: `revenue-detection-frontend` (must be unique)
   - Region: Choose closest to your users
   - Uncheck "Block all public access"
   - Enable "Static website hosting"

3. Configure bucket policy (replace `YOUR-BUCKET-NAME`):
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
        }
    ]
}
```

### Step 3: Upload Build Files

```bash
# Using AWS CLI
aws s3 sync dist/ s3://revenue-detection-frontend/ --delete

# Or use AWS Console to upload the dist folder contents
```

### Step 4: Create CloudFront Distribution

1. Go to CloudFront Console
2. Create distribution:
   - Origin domain: Select your S3 bucket
   - Origin access: Public
   - Viewer protocol policy: Redirect HTTP to HTTPS
   - Default root object: `index.html`
   - Custom error response:
     - HTTP error code: 403
     - Response page path: `/index.html`
     - HTTP response code: 200
   - Alternate domain names (CNAMEs): `your-domain.com`, `www.your-domain.com`
   - SSL certificate: Request certificate from ACM

3. Wait for distribution to deploy (15-20 minutes)

### Step 5: Configure Route 53 (Optional - for custom domain)

1. Create hosted zone for your domain
2. Create A record:
   - Name: Leave blank (for root domain) or `www`
   - Type: A - IPv4 address
   - Alias: Yes
   - Route traffic to: CloudFront distribution
   - Select your distribution

## Part 3: Database Setup (Production)

### Option A: Continue with SQLite (Simple)
- Keep using SQLite on EC2
- Ensure regular backups to S3
- Use cron job for automated backups:

```bash
# Create backup script
cat > /var/www/revenue-backend/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d-%H%M%S)
aws s3 cp /var/www/revenue-backend/backend/revenue_advisor.db s3://revenue-backend-backups/db-backup-$DATE.db
EOF

chmod +x /var/www/revenue-backend/backup.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /var/www/revenue-backend/backup.sh") | crontab -
```

### Option B: Use Amazon RDS (Scalable)
1. Create RDS PostgreSQL instance
2. Update `DATABASE_URL` in backend:
```python
DATABASE_URL=postgresql://username:password@rds-endpoint:5432/revenue_db
```
3. Install psycopg2: `pip install psycopg2-binary`
4. Migrate SQLite data to PostgreSQL

## Part 4: Security Hardening

### Backend Security
1. **Enable firewall:**
```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

2. **Disable SSH password authentication:**
```bash
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
sudo systemctl restart sshd
```

3. **Set strong SECRET_KEY** in production env

### Frontend Security
1. Enable CloudFront WAF for DDoS protection
2. Configure security headers in CloudFront
3. Use HTTPS only

## Part 5: Monitoring & Maintenance

### CloudWatch Logs (Backend)
```bash
# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb

# Configure to send logs
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/etc/config.json
```

### Application Monitoring
- Use admin panel to monitor system metrics
- Set up alerts for high leakage amounts
- Monitor API response times

### Backup Strategy
1. Database: Daily automated backups to S3
2. Uploaded files: Sync `backend/uploads/` to S3
3. Reports: Sync `backend/reports/` to S3

```bash
# Automated file sync (add to cron)
0 3 * * * aws s3 sync /var/www/revenue-backend/backend/uploads/ s3://revenue-backend-data/uploads/
0 3 * * * aws s3 sync /var/www/revenue-backend/backend/reports/ s3://revenue-backend-data/reports/
```

## Cost Estimation (Monthly)

| Service | Configuration | Estimated Cost |
|---------|--------------|----------------|
| EC2 (t2.medium) | 24/7 | $33.87 |
| S3 (Frontend) | 5GB storage, 10GB transfer | $0.50 |
| CloudFront | 50GB data transfer | $4.25 |
| RDS (db.t3.micro) | Optional | $15.33 |
| Route 53 | 1 hosted zone | $0.50 |
| **Total** | Without RDS | **~$39** |
| **Total** | With RDS | **~$54** |

## Deployment Checklist

### Pre-Deployment
- [ ] Update CORS settings in backend
- [ ] Set production environment variables
- [ ] Update API URL in frontend
- [ ] Test build locally
- [ ] Create AWS account and configure CLI

### Backend Deployment
- [ ] Launch EC2 instance
- [ ] Configure security groups
- [ ] Install dependencies
- [ ] Upload code
- [ ] Configure systemd service
- [ ] Setup nginx
- [ ] Configure SSL certificate
- [ ] Test API endpoints

### Frontend Deployment
- [ ] Build production bundle
- [ ] Create S3 bucket
- [ ] Upload build files
- [ ] Create CloudFront distribution
- [ ] Configure custom domain (optional)
- [ ] Test website access

### Post-Deployment
- [ ] Verify admin panel shows metrics
- [ ] Test file upload functionality
- [ ] Test business analysis features
- [ ] Test AI chatbot
- [ ] Configure backups
- [ ] Set up monitoring
- [ ] Document credentials securely

## Rollback Plan

If deployment fails:
1. Keep old server running until new deployment is verified
2. CloudFront allows instant rollback by invalidating cache
3. Backend can be quickly restarted with previous version
4. Database backups available for restoration

## Support Resources

- AWS Documentation: https://docs.aws.amazon.com/
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- Vite Production Build: https://vitejs.dev/guide/build.html

---

**Last Updated:** December 8, 2024
**Prepared for:** Revenue Leakage Detection System v1.0
