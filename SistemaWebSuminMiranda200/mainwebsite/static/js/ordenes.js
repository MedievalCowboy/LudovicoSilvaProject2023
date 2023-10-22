
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
            className: 'custom-option-btn',
            exportOptions: {
                columns: [1, 2, 3, 4] // Especifica las columnas a exportar (excluye la columna de opciones)
            },
            
        },
        {
            extend: 'pdf',
            text: '<i class="bi bi-file-pdf"></i> Exportar a PDF',
            className: 'btn btn-danger',
            exportOptions: {
                columns: [1, 2, 3, 4] // Especifica las columnas a exportar (excluye la columna de opciones)
            },
            title: 'PROVEEDORES',
            customize: function(doc) {
                // Obtén la fecha actual en formato 'dd/mm/yyyy'
                var currentDate = new Date().toLocaleDateString('es-ES');
                
                // Agrega la fecha como subtítulo
                doc.content.push({
                    text: 'Fecha: ' + currentDate, // Texto del subtítulo
                    fontSize: 10, // Tamaño de fuente del subtítulo
                    alignment: 'center', // Alineación del subtítulo
                    margin: [0, 5, 0, 10] // Márgenes del subtítulo (arriba, derecha, abajo, izquierda)
                });
 
                // Centrar la información en la hoja
                var rowCount = doc.content[1].table.body.length;
                for (var i = 0; i < rowCount; i++) {
                    doc.content[1].table.body[i].forEach(function(cell, j) {
                        cell.alignment = 'center';
                    });
                }
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
        {
            extend: 'print',
            text: '<i class="bi bi-printer"></i> Imprimir',
            className: 'btn btn-primary',
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
            url: "/workspace/orden/eliminar/" + elementoId,
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



    // Manejar el botón "Seleccionar Todo"
    $("#seleccionar-todo").click(function() {
        var isChecked = $(this).prop("checked");
        $(".seleccionar-elemento").prop("checked", isChecked);
    });



});