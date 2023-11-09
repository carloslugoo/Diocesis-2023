function borrarResolucion(resolucionId) {
    Swal.fire({
        title: '¿Estás seguro que deseas borrar la resolucion?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, borrar',
        cancelButtonText: 'Cancelar',
        customClass: {
            confirmButton: 'confirm-button-green' // Agrega la clase personalizada
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario confirma, realiza la solicitud para borrar la resolucion
            fetch(`/borrar_resolucion/${resolucionId}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Resolucion borrada exitosamente") {
                    window.location.href = '/resoluciones';}
            })
            .catch(error => {
                Swal.fire('Error', 'Ocurrió un error al borrar la resolucion', 'error');
            });
        }
    });
}