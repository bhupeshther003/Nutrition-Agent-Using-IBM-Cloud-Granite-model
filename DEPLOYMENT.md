# 🚀 Deployment Guide for NutriBot

This guide provides detailed instructions for deploying the NutriBot application to various platforms.

## Table of Contents
- [Local Development](#local-development)
- [IBM Cloud Deployment](#ibm-cloud-deployment)
- [Heroku Deployment](#heroku-deployment)
- [AWS Deployment](#aws-deployment)
- [Docker Deployment](#docker-deployment)
- [Production Checklist](#production-checklist)

---

## 🏠 Local Development

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment tool

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nutribot-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   
   Windows:
   ```bash
   .venv\Scripts\activate
   ```
   
   Linux/Mac:
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment**
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   ```
   
   Edit `.env` with your credentials:
   ```env
   IBM_CLOUD_API_KEY=your_api_key
   IBM_WATSONX_PROJECT_ID=your_project_id
   IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
   FLASK_SECRET_KEY=generate_a_secure_random_key
   FLASK_ENV=development
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   
   Open browser: `http://localhost:5000`

---

## ☁️ IBM Cloud Deployment

### Prerequisites
- IBM Cloud account
- IBM Cloud CLI installed
- Cloud Foundry CLI

### Deployment Steps

1. **Install IBM Cloud CLI**
   ```bash
   # Download from: https://cloud.ibm.com/docs/cli
   ```

2. **Login to IBM Cloud**
   ```bash
   ibmcloud login
   ibmcloud target --cf
   ```

3. **Create manifest.yml**
   ```yaml
   applications:
   - name: nutribot-app
     memory: 256M
     instances: 1
     buildpack: python_buildpack
     command: gunicorn app:app
     env:
       FLASK_ENV: production
   ```

4. **Create Procfile**
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT
   ```

5. **Set environment variables**
   ```bash
   ibmcloud cf set-env nutribot-app IBM_CLOUD_API_KEY "your_api_key"
   ibmcloud cf set-env nutribot-app IBM_WATSONX_PROJECT_ID "your_project_id"
   ibmcloud cf set-env nutribot-app FLASK_SECRET_KEY "your_secret_key"
   ```

6. **Deploy**
   ```bash
   ibmcloud cf push
   ```

7. **Access your app**
   ```bash
   ibmcloud cf apps
   # Note the URL provided
   ```

---

## 🟣 Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed
- Git installed

### Deployment Steps

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create nutribot-app
   ```

4. **Create Procfile** (if not exists)
   ```
   web: gunicorn app:app
   ```

5. **Set environment variables**
   ```bash
   heroku config:set IBM_CLOUD_API_KEY="your_api_key"
   heroku config:set IBM_WATSONX_PROJECT_ID="your_project_id"
   heroku config:set IBM_WATSONX_URL="https://us-south.ml.cloud.ibm.com"
   heroku config:set FLASK_SECRET_KEY="your_secret_key"
   heroku config:set FLASK_ENV="production"
   ```

6. **Initialize Git (if needed)**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

7. **Deploy to Heroku**
   ```bash
   git push heroku main
   ```

8. **Open the app**
   ```bash
   heroku open
   ```

9. **View logs**
   ```bash
   heroku logs --tail
   ```

---

## 🟠 AWS Deployment (Elastic Beanstalk)

### Prerequisites
- AWS account
- AWS CLI installed
- EB CLI installed

### Deployment Steps

1. **Install AWS EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB application**
   ```bash
   eb init -p python-3.9 nutribot-app
   ```

3. **Create environment**
   ```bash
   eb create nutribot-env
   ```

4. **Set environment variables**
   ```bash
   eb setenv IBM_CLOUD_API_KEY="your_api_key" \
            IBM_WATSONX_PROJECT_ID="your_project_id" \
            IBM_WATSONX_URL="https://us-south.ml.cloud.ibm.com" \
            FLASK_SECRET_KEY="your_secret_key" \
            FLASK_ENV="production"
   ```

5. **Deploy**
   ```bash
   eb deploy
   ```

6. **Open the app**
   ```bash
   eb open
   ```

7. **Monitor status**
   ```bash
   eb status
   eb logs
   ```

---

## 🐳 Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - IBM_CLOUD_API_KEY=${IBM_CLOUD_API_KEY}
      - IBM_WATSONX_PROJECT_ID=${IBM_WATSONX_PROJECT_ID}
      - IBM_WATSONX_URL=${IBM_WATSONX_URL}
      - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
      - FLASK_ENV=production
    restart: unless-stopped
```

### Deployment Steps

1. **Build the image**
   ```bash
   docker build -t nutribot-app .
   ```

2. **Run with docker-compose**
   ```bash
   docker-compose up -d
   ```

3. **Or run directly**
   ```bash
   docker run -d -p 5000:5000 \
     -e IBM_CLOUD_API_KEY="your_api_key" \
     -e IBM_WATSONX_PROJECT_ID="your_project_id" \
     -e IBM_WATSONX_URL="https://us-south.ml.cloud.ibm.com" \
     -e FLASK_SECRET_KEY="your_secret_key" \
     nutribot-app
   ```

4. **View logs**
   ```bash
   docker logs -f <container_id>
   ```

5. **Stop the container**
   ```bash
   docker-compose down
   ```

---

## ✅ Production Checklist

### Security
- [ ] Change `FLASK_SECRET_KEY` to a strong random value
- [ ] Never commit `.env` file to version control
- [ ] Use HTTPS in production
- [ ] Enable CORS only for trusted domains
- [ ] Implement rate limiting
- [ ] Add input validation and sanitization
- [ ] Keep dependencies updated

### Performance
- [ ] Use production WSGI server (gunicorn)
- [ ] Enable gzip compression
- [ ] Implement caching where appropriate
- [ ] Optimize static file delivery
- [ ] Monitor application performance
- [ ] Set up logging and monitoring

### Configuration
- [ ] Set `FLASK_ENV=production`
- [ ] Configure proper error handling
- [ ] Set up database (if needed)
- [ ] Configure session management
- [ ] Set appropriate timeout values

### Monitoring
- [ ] Set up application monitoring
- [ ] Configure error tracking (e.g., Sentry)
- [ ] Set up uptime monitoring
- [ ] Configure log aggregation
- [ ] Set up alerts for critical issues

### Backup
- [ ] Regular database backups (if applicable)
- [ ] Backup environment configurations
- [ ] Document recovery procedures

---

## 🔧 Environment Variables

Required environment variables for production:

```env
# IBM Watsonx.ai Configuration
IBM_CLOUD_API_KEY=your_ibm_cloud_api_key
IBM_WATSONX_PROJECT_ID=your_project_id
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Flask Configuration
FLASK_SECRET_KEY=generate_secure_random_key_here
FLASK_ENV=production
```

### Generating Secure Secret Key

Python method:
```python
import secrets
print(secrets.token_hex(32))
```

Command line:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue: Application won't start**
- Check all environment variables are set
- Verify Python version compatibility
- Check logs for specific errors

**Issue: IBM Watsonx.ai connection fails**
- Verify API key is correct
- Check Project ID is valid
- Ensure Watsonx.ai service is active
- Check network connectivity

**Issue: Static files not loading**
- Verify static folder structure
- Check file permissions
- Ensure correct URL paths

**Issue: High memory usage**
- Reduce number of workers
- Implement caching
- Optimize model parameters

---

## 📊 Monitoring and Logs

### View Application Logs

**Heroku:**
```bash
heroku logs --tail
```

**AWS:**
```bash
eb logs
```

**Docker:**
```bash
docker logs -f <container_name>
```

**IBM Cloud:**
```bash
ibmcloud cf logs nutribot-app --recent
```

---

## 🔄 Updates and Maintenance

### Updating the Application

1. **Pull latest changes**
   ```bash
   git pull origin main
   ```

2. **Update dependencies**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Test locally**
   ```bash
   python app.py
   ```

4. **Deploy updates**
   ```bash
   # Heroku
   git push heroku main
   
   # AWS
   eb deploy
   
   # IBM Cloud
   ibmcloud cf push
   ```

---

## 📞 Support

For deployment issues:
1. Check application logs
2. Review platform-specific documentation
3. Verify all environment variables
4. Check IBM Watsonx.ai service status

---

**Happy Deploying! 🚀**