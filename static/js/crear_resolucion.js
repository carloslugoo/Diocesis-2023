document.querySelector('form').addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            if (response.status === 400 || response.status === 415) {
                Swal.fire('Error', errorData.error, 'error');
            } else {
                Swal.fire('Error', 'Ocurrió un error en la carga del archivo', 'error');
            }
        } else {
            Swal.fire('Éxito', 'Archivo cargado exitosamente', 'success');
            // Aquí puedes realizar otras acciones si la carga fue exitosa
            window.location.href = "/resoluciones";
        }
    } catch (error) {
        console.error('Error:', error);
        Swal.fire('Error', 'Ocurrió un error inesperado', 'error');
    }
});