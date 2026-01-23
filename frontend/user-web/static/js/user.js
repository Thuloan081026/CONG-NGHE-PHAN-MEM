// public.js

document.addEventListener("DOMContentLoaded", function() {
    console.log("SMD Public Portal Loaded");
    
    // Có thể thêm hiệu ứng scroll mượt ở đây nếu muốn
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});