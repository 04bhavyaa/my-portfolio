# Vercel Deployment Guide for Django Portfolio

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **Environment Variables**: Prepare your environment variables

## Step 1: Prepare Your Project

### 1.1 Install Required Packages

```bash
pip install -r requirements.txt
```

### 1.2 Update Settings for Production

The `settings.py` file has been updated with:

- Environment variable support using `python-decouple`
- WhiteNoise for static file serving
- Production-ready configurations

### 1.3 Create Environment Variables

Create a `.env` file locally (don't commit this):

```env
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.vercel.app,localhost
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Step 2: Deploy to Vercel

### 2.1 Connect GitHub Repository

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Select the repository containing your Django portfolio

### 2.2 Configure Build Settings

Vercel will automatically detect the configuration from `vercel.json`, but verify:

- **Framework Preset**: Other
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py loaddata portfolio/fixtures/initial_data.json`
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt`

### 2.3 Set Environment Variables

In Vercel Dashboard → Project Settings → Environment Variables, add:

| Name                  | Value                     | Environment         |
| --------------------- | ------------------------- | ------------------- |
| `SECRET_KEY`          | Generate a new secret key | Production, Preview |
| `DEBUG`               | `False`                   | Production, Preview |
| `ALLOWED_HOSTS`       | `your-domain.vercel.app`  | Production, Preview |
| `EMAIL_HOST_USER`     | Your Gmail address        | Production, Preview |
| `EMAIL_HOST_PASSWORD` | Your Gmail app password   | Production, Preview |

### 2.4 Generate Secret Key

```python
# Run this in Python shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Step 3: Gmail Setup for Contact Form

### 3.1 Enable 2-Factor Authentication

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification

### 3.2 Generate App Password

1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select "Mail" and "Other (Custom name)"
3. Enter "Portfolio Contact Form"
4. Copy the generated 16-character password
5. Use this as `EMAIL_HOST_PASSWORD` in Vercel

## Step 4: Deploy and Test

### 4.1 Deploy

1. Click "Deploy" in Vercel
2. Wait for the build to complete
3. Your site will be available at `https://your-project-name.vercel.app`

### 4.2 Test Your Deployment

- [ ] Homepage loads correctly
- [ ] All sections display properly
- [ ] Contact form sends emails
- [ ] Static files (CSS/JS) load
- [ ] Images display correctly

## Step 5: Custom Domain (Optional)

### 5.1 Add Custom Domain

1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Update `ALLOWED_HOSTS` environment variable

## Troubleshooting

### Common Issues

#### Static Files Not Loading

- Ensure `STATIC_ROOT` is set in settings
- Run `python manage.py collectstatic` before deployment
- Check WhiteNoise configuration

#### Database Issues

- Vercel uses ephemeral file system
- SQLite database resets on each deployment
- Consider using PostgreSQL for persistent data

#### Email Not Working

- Verify Gmail app password is correct
- Check environment variables in Vercel
- Test with console backend first

#### Build Failures

- Check Python version compatibility
- Ensure all dependencies are in `requirements.txt`
- Review build logs in Vercel dashboard

### Debug Mode

For debugging, temporarily set:

```env
DEBUG=True
ALLOWED_HOSTS=*
```

## File Structure for Vercel

```
portfolio-project/
├── vercel.json          # Vercel configuration
├── requirements.txt     # Python dependencies
├── build.sh            # Build script
├── .env                 # Environment variables (local only)
├── .gitignore          # Git ignore rules
├── portfolio_site/     # Django project
├── portfolio/          # Django app
├── static/             # Static files
├── templates/          # HTML templates
└── media/              # Media files (if any)
```

## Performance Tips

1. **Optimize Images**: Compress images before uploading
2. **Minify CSS/JS**: Use tools to minify static files
3. **Enable Caching**: Configure appropriate cache headers
4. **CDN**: Vercel automatically provides CDN for static files

## Security Considerations

1. **Never commit `.env` file**
2. **Use strong SECRET_KEY**
3. **Set DEBUG=False in production**
4. **Configure ALLOWED_HOSTS properly**
5. **Use HTTPS only**

## Monitoring

- Check Vercel Analytics for traffic
- Monitor error logs in Vercel Dashboard
- Set up uptime monitoring
- Track contact form submissions

## Backup Strategy

- Keep your code in version control
- Export database data regularly
- Backup media files separately
- Document your deployment process

---

**Need Help?**

- [Vercel Documentation](https://vercel.com/docs)
- [Django Deployment Guide](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [WhiteNoise Documentation](https://whitenoise.readthedocs.io/)
