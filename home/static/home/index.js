function toggleMenu(id) {
                    const el = document.getElementById(id);
                    if(el) el.classList.toggle('hidden');
                }




const link = document.createElement('link');
  link.rel = 'icon';
  link.type = 'image/x-icon';
  link.href = "{% static 'home/images/3.ico' %}"; // Django static path

  // Remove any old favicons
  const oldLinks = document.querySelectorAll("link[rel~='icon']");
  oldLinks.forEach(l => l.parentNode.removeChild(l));

  // Add the new one
  document.head.appendChild(link);