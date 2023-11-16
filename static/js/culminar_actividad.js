document.getElementById('archivo').addEventListener('change', function() {
    var archivos = this.files;
    var maxSize = 10 * 1024 * 1024; 
    if (archivos.length > 4) {
        // Muestra la alerta con SweetAlert
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Solo se permiten hasta 4 imágenes.',
        });

        // Eliminar archivos adicionales si el usuario selecciona más de 4
        this.value = '';
    }
    for (var i = 0; i < archivos.length; i++) {
        // Verifica el tamaño de cada archivo
        if (archivos[i].size > maxSize) {
            // Muestra la alerta con SweetAlert
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'El tamaño de los archivos no debe superar los 25 MB.',
            });
        }
    }   
});