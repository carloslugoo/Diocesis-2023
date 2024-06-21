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
function confirmarActividad(actividadId) {
    Swal.fire({
        title: '¿Estás seguro que deseas participar en la actividad?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, participar',
        cancelButtonText: 'Cancelar',
        customClass: {
            confirmButton: 'confirm-button-green' // Agrega la clase personalizada
        }
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario confirma, realiza la solicitud para borrar la actividad
            fetch(`/participar_actividad/${actividadId}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "Exito") {
                    window.location.href = `/ver_actividad/${actividadId}`;}
            })
            .catch(error => {
                Swal.fire('Error', 'Ocurrió un error al borrar la actividad', 'error');
            });
        }
    });
}