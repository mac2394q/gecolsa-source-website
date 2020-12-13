/*jshint strict:true, browser:true, jquery:true */
$(function () {
    'use strict';

    $.Redactor.opts.langs.es = {
        html: 'HTML',
        video: 'Video',
        image: 'Imagen',
        table: 'Tabla',
        link: 'Enlace',
        link_insert: 'Insertar enlace ...',
        link_edit: 'Edit link',
        unlink: 'Desenlazar',
        formatting: 'Estilos',
        paragraph: 'Párrafo',
        quote: 'Comillas',
        code: 'Código',
        header1: 'Título H1',
        header2: 'Título H2',
        header3: 'Título H3',
        header4: 'Título H4',
        header5: 'Título H5',
        bold:  'Negrita',
        italic: 'Itálica',
        fontcolor: 'Color fuente',
        backcolor: 'Color fondo',
        unorderedlist: 'Lista sin orden',
        orderedlist: 'Lista ordenada',
        outdent: 'Disminuir sangrado',
        indent: 'Sangrar',
        cancel: 'Cancelar',
        insert: 'Añadir',
        save: 'Guardar',
        _delete: 'Borrar',
        insert_table: 'Añadir tabla',
        insert_row_above: 'Añadir fila arriba',
        insert_row_below: 'Añadir fila debajo',
        insert_column_left: 'Añadir columna a la izquierda',
        insert_column_right: 'Añadir column a la derecha',
        delete_column: 'Borrar columna',
        delete_row: 'Borrar fila',
        delete_table: 'Borrar tabla',
        rows: 'Filas',
        columns: 'Columnas',
        add_head: 'Añadir cabecera',
        delete_head: 'Borrar cabecera',
        title: 'Título',
        image_position: 'Posición',
        none: 'Ninguna',
        left: 'Izquierda',
        right: 'Derecha',
        center: 'Centro',
        image_web_link: 'Enlace de imagen web',
        text: 'Texto',
        mailto: 'Email',
        web: 'URL',
        video_html_code: 'Código embebido del video',
        file: 'Fichero',
        upload: 'Cargar',
        download: 'Descargar',
        choose: 'Seleccionar',
        or_choose: 'O seleccionar',
        drop_file_here: 'Soltar el fichero aquí',
        align_left: 'Alinear a la izquierda',
        align_center: 'Alinear al centro',
        align_right: 'Alinear a la derecha',
        align_justify: 'Justificar',
        horizontalrule: 'Trazo horizontal',
        deleted: 'Borrado',
        anchor: 'Anclaje',
        link_new_tab: 'Open link in new tab',
        underline: 'Subrayado',
        alignment: 'Alineación',
        filename: 'Nombre (opcional)',
        edit: 'Editar'
    };

    // Enable redactor
    /*ignore jslint start*/
    $('textarea').redactor({
        minHeight: 300,
        toolbarFixedTopOffset: 63,
        lang: 'es',
        plugins: ['table'],
        formattingAdd: [
            {
                tag: 'span',
                title: 'Fecha',
                class: 'year-box'
            },
            {
                tag: 'blockquote',
                title: 'Cita'
            },
            {
                tag: 'p',
                title: 'Cabecera de tabla',
                class: 'table-header'
            }
        ],
        imageUpload: '/admin/redactor/upload/image/'
    });
    /*ignore jslint end*/
});
