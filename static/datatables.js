$(document).ready(function () {
    $('#ventas').DataTable({
        "language": {
            "lengtMenu": "Mostrar _MENU_ registro",
            "zeroRecords": "No se encontraron resultados",
            "info": "Mostrando registros del _START_ al _END_ de un total _TOTAL_ registros",
            "infoEmpty": "Mostrando registros del 0 al 0 de un total registros",
            "sSearch": "Buscar:",
            "oPaginate": {
                "sFirst": "Primero",
                "sLast": "Ultimo",
                "sNext": "Siguiente",
                "sPrevius": "Anterior"
            },
            "sProcessing": "Procesado..."
        }
    });
});