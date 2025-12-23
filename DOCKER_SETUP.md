# Running GCM with Docker on WSL

Complete guide for running the General Circulation Model using Docker on Windows WSL.

## Prerequisites

1. **Windows WSL2** installed
2. **Docker Desktop** for Windows with WSL2 backend
3. **Git** (to clone the repository)

### Install Docker on WSL

If you haven't installed Docker yet:

```bash
# Update package index
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker
```

**OR** use Docker Desktop for Windows with WSL2 integration (recommended).

---

## Quick Start

### Option 1: Run Demo Scenarios (Generate Plots)

```bash
# Build and run demo scenarios
docker-compose --profile demo up --build

# Plots will be saved to ./output/ directory
```

### Option 2: Run Web Application

```bash
# Build and run web interface
docker-compose --profile web up --build

# Open browser to: http://localhost:5000
```

### Option 3: Interactive Python Shell

```bash
# Start interactive shell
docker-compose --profile shell run gcm-shell

# Inside container, you can run:
python demo_scenarios.py
# or
python -c "from gcm import GCM; model = GCM(); print('GCM loaded!')"
```

---

## Detailed Usage

### 1. Build the Docker Image

```bash
# Build the image
docker build -t gcm:latest .

# Or with docker-compose
docker-compose build
```

### 2. Run Demo Scenarios

**Using Docker Compose (Recommended):**
```bash
docker-compose --profile demo up
```

**Using Docker directly:**
```bash
docker run -v $(pwd)/output:/app/output gcm:latest python demo_scenarios.py
```

**Output:**
- Plots saved to `./output/` directory
- View with any image viewer or browser

### 3. Run Web Application

**Using Docker Compose:**
```bash
docker-compose --profile web up
```

**Using Docker directly:**
```bash
docker run -p 5000:5000 -v $(pwd)/output:/app/output gcm:latest python app.py
```

**Access:**
- Open browser: http://localhost:5000
- Configure and run simulations interactively
- Download plots directly from web interface

### 4. Run Custom Python Scripts

```bash
# Start shell
docker-compose --profile shell run gcm-shell

# Inside container:
python
>>> from gcm import GCM
>>> model = GCM(nlon=32, nlat=16, nlev=10)
>>> model.initialize(profile='tropical')
>>> model.run(duration_days=1)
```

---

## Output Files

All generated plots are saved to `./output/` directory:

```
output/
├── gcm_scenarios_comprehensive.png    # Complete overview
├── gcm_detail_tropical.png            # Tropical scenario
├── gcm_detail_midlatitude.png         # Midlatitude scenario
└── gcm_detail_polar.png               # Polar scenario
```

---

## Common Commands

### View Running Containers

```bash
docker ps
```

### Stop Containers

```bash
# Stop all
docker-compose down

# Stop specific profile
docker-compose --profile web down
```

### Remove Containers and Images

```bash
# Remove containers
docker-compose down

# Remove image
docker rmi gcm:latest

# Clean everything (containers, images, volumes)
docker system prune -a
```

### View Logs

```bash
# Follow logs
docker-compose --profile demo logs -f

# View specific container
docker logs gcm-demo
```

### Rebuild After Code Changes

```bash
# Rebuild and run
docker-compose --profile demo up --build

# Force rebuild
docker-compose build --no-cache
```

---

## Development Workflow

### Edit Code Locally, Run in Docker

1. **Edit files** in your favorite editor (VS Code, etc.)
2. **Code is mounted** via volumes - changes reflect immediately
3. **Restart container** to pick up changes:
   ```bash
   docker-compose --profile web restart
   ```

### Live Development

For web app with auto-reload:

```bash
# Edit docker-compose.yml, change FLASK_ENV to development
# Then run:
docker-compose --profile web up

# Flask will auto-reload on code changes
```

---

## Troubleshooting

### Issue: "Cannot connect to Docker daemon"

**Solution:**
```bash
# Start Docker service
sudo service docker start

# Or use Docker Desktop (Windows)
```

### Issue: "Permission denied" on WSL

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Issue: "Port 5000 already in use"

**Solution:**
```bash
# Find process using port
sudo lsof -i :5000

# Kill it or change port in docker-compose.yml:
ports:
  - "8080:5000"  # Use port 8080 instead
```

### Issue: Slow performance on WSL

**Solution:**
- Use Docker Desktop with WSL2 integration
- Store code in WSL filesystem (not /mnt/c/)
- Increase Docker memory limit in Docker Desktop settings

### Issue: Plots not appearing in output/

**Solution:**
```bash
# Create output directory
mkdir -p output

# Check volume mount
docker-compose --profile demo config

# Verify permissions
chmod 777 output
```

---

## Performance Tips

### 1. Use WSL2 Filesystem

Store project in WSL home directory for better performance:

```bash
# Good (fast)
/home/username/gcm/

# Bad (slow)
/mnt/c/Users/username/gcm/
```

### 2. Allocate More Resources

In Docker Desktop:
- Settings → Resources
- Increase CPUs to 4+
- Increase Memory to 8GB+

### 3. Use BuildKit

Enable faster builds:

```bash
export DOCKER_BUILDKIT=1
docker-compose build
```

---

## Advanced Usage

### Custom Resolution

Create custom script:

```python
# custom_run.py
from gcm import GCM

model = GCM(nlon=64, nlat=32, nlev=20, dt=600)
model.initialize(profile='tropical')
model.run(duration_days=10, output_interval_hours=6)
```

Run in Docker:

```bash
docker run -v $(pwd):/app -v $(pwd)/output:/app/output \
  gcm:latest python custom_run.py
```

### Run Specific Scenario

```bash
docker run -v $(pwd)/output:/app/output gcm:latest \
  python -c "
from gcm import GCM
import matplotlib.pyplot as plt
model = GCM(nlon=24, nlat=12, nlev=8)
model.initialize(profile='polar')
model.run(duration_days=5)
plt.figure()
plt.contourf(model.state.T[0])
plt.savefig('/app/output/my_plot.png')
"
```

### Batch Processing

Create `batch_run.sh`:

```bash
#!/bin/bash
for profile in tropical midlatitude polar; do
  docker run -v $(pwd)/output:/app/output gcm:latest \
    python run_single_scenario.py --profile $profile
done
```

---

## Complete Example Session

```bash
# 1. Clone repository (if needed)
git clone https://github.com/monksealseal/heroku.git
cd heroku

# 2. Create output directory
mkdir -p output

# 3. Build Docker image
docker-compose build

# 4. Run demo scenarios
docker-compose --profile demo up

# 5. View plots
ls -lh output/
# Open plots in your default image viewer
xdg-open output/gcm_scenarios_comprehensive.png

# 6. Run web interface
docker-compose --profile web up

# 7. Open browser
# Visit: http://localhost:5000

# 8. Stop everything
docker-compose down
```

---

## Docker Files Reference

### Dockerfile
- Base image: Python 3.11 slim
- System deps: gcc, gfortran, HDF5, NetCDF
- Python deps: numpy, scipy, matplotlib, flask
- Working dir: `/app`
- Exposed port: 5000

### docker-compose.yml

**Services:**
1. **gcm-demo**: Run scenarios, generate plots
2. **gcm-web**: Web interface on port 5000
3. **gcm-shell**: Interactive Python shell

**Profiles:**
- `demo`: Run demo scenarios
- `web`: Run web application
- `shell`: Interactive development

---

## Next Steps

1. **Run demos**: `docker-compose --profile demo up --build`
2. **View plots**: Check `./output/` directory
3. **Try web app**: `docker-compose --profile web up`
4. **Customize**: Edit code, rebuild, run again

---

## Resources

- **Docker Docs**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **WSL2**: https://docs.microsoft.com/en-us/windows/wsl/
- **GCM Documentation**: See `docs/` folder

---

## Summary

```bash
# Quick reference card
docker-compose --profile demo up    # Run scenarios
docker-compose --profile web up     # Web interface
docker-compose --profile shell run gcm-shell  # Interactive
docker-compose down                 # Stop all
docker-compose build --no-cache     # Rebuild clean
```

Enjoy running your General Circulation Model! 🌍🌡️
