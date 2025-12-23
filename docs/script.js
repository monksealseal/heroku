// General Circulation Model - GitHub Pages JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all animatable elements
    document.querySelectorAll('.feature-card, .doc-card, .use-case, .step').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });

    // Update "Launch Web App" links with actual Heroku URL
    // (Replace 'your-app' with actual app name after deployment)
    const appUrl = 'https://your-app.herokuapp.com';
    document.querySelectorAll('a[href="https://your-app.herokuapp.com"]').forEach(link => {
        // Keep as placeholder for now - user will update after Heroku deployment
        link.addEventListener('click', (e) => {
            if (link.href === 'https://your-app.herokuapp.com/') {
                e.preventDefault();
                alert('Deploy the app to Heroku first, then update this link with your app URL!');
            }
        });
    });

    // GitHub repo link
    const githubLinks = document.querySelectorAll('a[href="https://github.com/monksealseal/heroku"]');
    githubLinks.forEach(link => {
        // Update with actual GitHub repo URL
        link.href = 'https://github.com/YOUR_USERNAME/YOUR_REPO';
    });

    console.log('🌍 GCM GitHub Pages loaded successfully!');
});
