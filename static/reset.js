document.getElementById("miFormulario").addEventListener("submit", function(event) {
    // Evitar que el formulario se envíe normalmente
    event.preventDefault();
    
    // Resetear el formulario
    this.reset();
  });