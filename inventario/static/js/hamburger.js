document.addEventListener("DOMContentLoaded", () => {
    // Seleccionar elementos
    const hamburgerIcon = document.getElementById("hamburger-icon")
    const navMenu = document.getElementById("nav-menu")
    const dropdownToggles = document.querySelectorAll(".dropdown-toggle")
  
    // Función para alternar el menú
    hamburgerIcon.addEventListener("click", () => {
      navMenu.classList.toggle("active")
      document.body.classList.toggle("menu-open")
    })
  
    // Cerrar el menú al hacer clic fuera de él
    document.addEventListener("click", (event) => {
      const isClickInsideMenu = navMenu.contains(event.target)
      const isClickOnHamburger = hamburgerIcon.contains(event.target)
  
      if (!isClickInsideMenu && !isClickOnHamburger && navMenu.classList.contains("active")) {
        navMenu.classList.remove("active")
        document.body.classList.remove("menu-open")
      }
    })
  
    // Manejar los submenús en dispositivos móviles
    if (window.innerWidth <= 768) {
      dropdownToggles.forEach((toggle) => {
        toggle.addEventListener("click", function (e) {
          e.preventDefault()
          const parent = this.parentElement
  
          // Cerrar todos los otros submenús abiertos
          document.querySelectorAll(".dropdown.active").forEach((item) => {
            if (item !== parent) {
              item.classList.remove("active")
            }
          })
  
          // Alternar el submenú actual
          parent.classList.toggle("active")
        })
      })
    }
  })

  function cargarNotificaciones() {
    fetch('/api/notificaciones/')
    .then(res => res.json())
    .then(data => {
        const contenedor = document.getElementById('notificaciones');
        contenedor.innerHTML = '';
        data.notificaciones.forEach(n => {
            const div = document.createElement('div');
            div.className = 'alerta-notificacion';
            div.innerHTML = `
                <span>${n.mensaje} (${n.fecha})</span>
                <button onclick="this.parentElement.remove()">✖</button>
            `;
            contenedor.appendChild(div);
        });
    });
}
setInterval(cargarNotificaciones, 10000); // cada 10 seg
  
  
 
  