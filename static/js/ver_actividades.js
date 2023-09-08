function confirmDelete(actividadId) {
    Swal.fire({
        title: '¿Estás seguro que deseas borrar la actividad?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, borrar',
        cancelButtonText: 'Cancelar',
        customClass: {
            confirmButton: 'confirm-button-green' // Agrega la clase personalizada
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario confirma, realiza la solicitud para borrar la actividad
            fetch(`/borrar_actividad/${actividadId}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Actividad borrada exitosamente") {
                    window.location.href = '/actividades';}
            })
            .catch(error => {
                Swal.fire('Error', 'Ocurrió un error al borrar la actividad', 'error');
            });
        }
    });
}