var tblProducts;
var tblSearchProducts;
var vents = {
    items: {
        cli: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: []
    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.products, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        var itbis = $('input[name="iva"]').val();
        var extra = 1.08;

        $.each(this.items.products, function (pos, dict) {
            dict.subtotal = dict.cant * parseFloat(dict.pvp);
            subtotal += dict.subtotal
        });
        this.items.subtotal = subtotal/extra;
        this.items.iva = this.items.subtotal * itbis;
        this.items.total = this.items.subtotal + this.items.iva;


        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (item) {
        this.items.products.push(item)
        this.list();
    },
    list: function () {
        this.calculate_invoice()
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data": "id"},
                {"data": "name"},
                {"data": "nexistencia"},
                {"data": "pvp"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color:white; "><i class="fas fa-trash-alt"></i></a>';

                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">'+data+'</span>'
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);

                    }
                },

                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text"  name="cant"  class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';

                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);

                    }
                },
            ],
            rowCallback(row, data) {
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: data.nexistencia,
                    step: 1,
                    buttondown_class: 'btn btn-secondary',
                    buttonup_class: 'btn btn-secondary',

                });
            },
            initComplete: function (settings, json) {

            }
        });
    }
}
function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }
    if (!Number.isInteger(repo.id )) {
        return repo.text;
    }
    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.name + '/'+ repo.cat.name + '<br>' +
        '<b>Existencia:</b> ' + repo.nexistencia + '<br>' +
        '<b>PVP:</b> <span class="badge badge-warning">$' + repo.pvp + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    $('#date_joined').datetimepicker({
        // format: 'DD/MM/DD',
        format: 'YYYY-MM-DD',
        // date: moment().format("DD/MM/YYYY"),
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });
    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '$',
        buttondown_class: 'btn btn-secondary',
        buttonup_class: 'btn btn-secondary',

    }).on('change ', function (event) {
        event.preventDefault();
        vents.calculate_invoice()
    }).val(0.08);
    //search clientes seleccion de cliente agregar cliente y ventana modal cliente
    $('select[name="cli"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_clients'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una letra nombre, apellido o rfc...',
        minimumInputLength: 1,
    });
    $('.btnAddClient').on('click', function () {
        //alert('x');
        //revisar;
        $('#myModalClient').modal('show');
    });
    $('#myModalClient').on('hidden.bs.modal', function (e) {
       $('#frmClient').trigger('reset'); 
    });
    $('#frmClient').on('submit', function (e) {
        e.preventDefault();
        // if (vents.items.products.length === 0) {
        //     message_error('Debe tener un producto para realizar el regitro');
        //     return false;
        // }
        // vents.items.date_joined = $('input[name="date_joined"]').val();
        // vents.items.cli = $('select[name="cli"]').val();
        var parameters = new FormData(this);
        parameters.append('action', 'create_client');
        //parameters.append('action', $('input[name="action"]').val())
        //parameters.append('vents', JSON.stringify(vents.items));
        submit_with_ajax(window.location.pathname, 'Notificación',
                        '¿Estas seguro de crear el siguiente cliente?', parameters, function (response) {
                            var newOption = new Option(response.full_name, response.id,false,true)
                            $('select[name="cli"]').append(newOption).trigger('change');
                            $('#myModalClient').modal('hide');
            // location.href = '/erp/sale/list';
        });
    });
    //comentar despues de usar
    // $('input[name="search"]').autocomplete({
    //     source: function (request, response) {
    //         $.ajax({
    //             url: window.location.pathname,
    //             type: 'POST',
    //             data: {
    //                 'action': 'search_products',
    //                 'term': request.term
    //             },
    //             dataType: 'json',
    //         }).done(function (data) {
    //             response(data);
    //         }).fail(function (jqXHR, textStatus, errorThrown) {
    //             //alert(textStatus + ': ' + errorThrown);
    //         }).always(function (data) {
    
    //         });
    //     },
    //     delay: 500,
    //     minLength: 1,
    //     select: function (event, ui) {
    //         event.preventDefault();
    //         console.clear();
    //         ui.item.cant = 1;
    //         ui.item.subtotal = 0.00;
    //         console.log(vents.items);
    //         vents.add(ui.item);
    //         $(this).val('');
    //     }
    // });
    $('.btnRemoveAll').on('click', function () {
        if (vents.items.products.length === 0) return false;
        alert_action('Notificacion', 'Estas seguro de elminar todo?', function () {
            vents.items.products = []
            vents.list()
        },function () {
            
        });
    });
    // event cant
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de elminar todo?', function () {
                vents.items.products.splice(tr.row, 1);
                vents.list();
            });
        })
        .on('change', 'input[name="cant"]', function () {

            console.clear();
            var cant = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td,li')).index();
            vents.items.products[tr.row].cant = cant;
            vents.calculate_invoice();
            $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2))
        });
    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus()
    })
    //nuevo venta modal de buscar articulos y agregar descontandolo de la lista modal
    $('.btnSearchProducts').on('click', function() {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'ids': JSON.stringify(vents.get_ids()),
                    'term': $('select[name="search"]').val()
                },
                dataSrc: ""
            },
            columns: [
                {"data": "name"},
                {"data": "nexistencia"},            
                {"data": "image"},
                {"data": "pvp"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">'+data+'</span>'
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$'+parseFloat(data).toFixed(2);
                    }
                },
                
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a rel="add" class="btn btn-success btn-xs btn-flat"><i class="fas fa-plus"></i></a> ';
                        
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {
    
            }
        });
        $('#MyModalSearchProducts').modal('show');
    });
    $('#tblSearchProducts tbody')
        .on('click', 'a[rel="add"]', function () {
            var tr = tblSearchProducts.cell($(this).closest('td,li')).index();
            var product = tblSearchProducts.row(tr.row).data();
            product.cant = 1;
            product.subtotal = 0.00;
            vents.add(product);
            //tblSearchProducts.row($(this).parents('tr')).remove().drawn();
            tblSearchProducts.row( $(this).parents('tr') ).remove().draw();
        });
    // Event Submit
    // vents.items.date_joined = $('input[name="date_joined"]').val();
    //        vents.items.cli = $('select[name="cli"]').val();
    //        var parameters = new FormData();
    //        parameters.append('action', $('input[name="action"]').val());
    //        parameters.append('vents', JSON.stringify(vents.items));
    $('#frmSale').on('submit', function (e) {
        e.preventDefault();
        
        if (vents.items.products.length === 0) {
            message_error('Debe tener un producto para realizar el regitro');
            return false;
        }
        vents.items.date_joined = $('input[name="date_joined"]').val();
        vents.items.cli = $('select[name="cli"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val())
        parameters.append('vents', JSON.stringify(vents.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                    alert_action('Alerta!','Quiere imprimir el Ticket de Venta?', function () {
                         window.open('/erp/sale/invoice/pdf/'+response.id+'/', '_blank');
                          location.href = '/erp/sale/list';
                    }, function () {
                        location.href = '/erp/sale/list';
                    });
            // location.href = '/erp/sale/list';
        });
    });
    

    //event list
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_autocomplete',
                    ids: JSON.stringify(vents.get_ids())
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        if(!Number.isInteger(data.id )){
            return false;
        }
        data.cant = 1;
        data.subtotal = 0.00;
        vents.add(data);
        $(this).val('').trigger('change.select2');
        ;
    });
    vents.list()
});
