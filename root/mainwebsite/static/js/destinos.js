
$(document).ready(function() {


    // Inicializar DataTables
    $('#miTabla').DataTable({
        paging: true, // Habilitar paginación
        pageLength: 20, // Número de filas por página
        searching: true, // Habilitar la función de búsqueda
        dom: 'Bfrtip', // Habilitar los botones de exportación
        buttons: [
        {
            extend: 'excel',
            text: '<i class="bi bi-file-excel"></i> Exportar a Excel',
            className: 'btn btn-success',
            exportOptions: {
                columns: [1, 2, 3, 4] // Especifica las columnas a exportar (excluye la columna de opciones)
            },
            
        },

        {
            extend: 'csv',
            text: '<i class="bi bi-file-earmark-spreadsheet"></i> Exportar a CSV',
            className: 'btn btn-info',
            exportOptions: {
                columns: [1, 2, 3, 4] // Especifica las columnas a exportar (excluye la columna de opciones)
            }
        },

        ],
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json',// Cargar traducción al español
        },
        
    });


    // Abrir el modal de confirmación de eliminación
    $(".eliminar").click(function() {
        var elementoId = $(this).data("id");
        $("#confirmar-eliminar").attr("data-id", elementoId); // Guardar el ID en el botón de confirmación
        $("#confirmarEliminarModal").modal("show");
    });

    // Cuando se confirma la eliminación desde el modal
    $("#confirmar-eliminar").click(function() {
        var elementoId = $(this).data("id");
        $.ajax({
            url: "/workspace/destino/eliminar/" + elementoId,
            type: "POST",
            data: {
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            dataType: "json",
            success: function(response) {
                // Actualizar la tabla después de eliminar
                location.reload();
            },
            error: function(error) {
                console.log(error);
            }
        });
        $("#confirmarEliminarModal").modal("hide"); // Ocultar el modal de confirmación
    });


});