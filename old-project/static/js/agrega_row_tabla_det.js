function nuevo_lin(id, id_tabla){
    let inten = $('#' + id_tabla).find('tr').length - 2;

    if (inten - 1 >= id) {
        id = inten;
    }

    let id_lin_men = 'addr_' + (id - 1) + '_' + id_tabla;
    let id_lin = 'addr_' + id + '_' + id_tabla;
    let id_lin_mas = 'addr_' + (id + 1) + '_' + id_tabla;

    $("#" + id_lin).html($("#" + id_lin_men).html()).find('td:first-child').html(id + 1);
    $('#' + id_tabla).append('<tr id="' + id_lin_mas + '" ></tr>');
}


function delete_lin(but, f) {
    let a = $(but).closest('tr');
    let row = document.getElementById(a[0].id)
    let tabla = $(but).closest('table');
    let trs = $(tabla).find('tr');
    let cantidad = trs.length - 2;
    const cantidadbtn = document.getElementById(tabla[0].id).querySelectorAll("a[id=delete_row").length;
    
    if (cantidadbtn > 2) {
        a.html('');
        row.remove();
        let trs = $(tabla).find('tr')

        for (var i = 1; i <= cantidad; i++) {
            $(trs[i]).find('td:first-child').html(i)
            trs[i].setAttribute('id', 'addr_' + (i-1) + "_" + f)
        }
    }
};