var tblProd;
var tblCardex;

function format(d) {
    console.log(d)
    var html = '<table class="table table-sm" >';
    html += ' <thead class="thead-dark">';
    html += ' <tr> <th  scope="col">Producto</th>';
    html += '  <th scope="col">Tipo Mov</th>';
    html += '  <th scope="col">Folio</th>';
    html += '  <th scope="col">Fecha</th>';
    html += '  <th scope="col">Cantidad</th>';
    html += '  <th scope="col">Costo</th></tr>';
    html += ' </thead>';
    html += ' <tbody>';
    // $.each(d.det, function (key, value) {
    //     html+='<tr>'
    //     html+='<td>'+value.prod.name+'</td>'
    //     html+='<td>'+value.prod.cat.name+'</td>'
    //     html+='<td>'+value.price+'</td>'
    //     html+='<td>'+value.cant+'</td>'
    //     html+='<td>'+value.subtotal+'</td>'
    //     html+='</tr>';
    // });
    html += ' </tbody>';
    return html
}


$(function () {
    tblProd = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            // {
            //     "className": 'dt-control',
            //     "orderable": false,
            //     "data": null,
            //     "defaultContent": ''
            // },
            {"data": "id"},
            {"data": "cat.name"},
            {"data": "name"},            
            {"data": "image"},
            {"data": "pvp"},
            {"data": "exist"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$'+parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if(row.nexistencia > 0){
                        return '<span class="badge badge-success">'+data+'</span>'
                    }else if(row.nexistencia < 0){
                        return '<span class="badge badge-danger">'+data+'</span>'
                    }
                    return '<span class="badge badge-warning">'+data+'</span>'
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/product/update/' + row.id + '/" class="btn btn-success btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/erp/product/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    buttons += '<a rel="info_prod" class="btn btn-primary btn-xs btn-flat" style="color: white"><i class="fas fa-search"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
    // $('<div class="loading">Loading</div>').appendTo('body');

    $('#data tbody')
    .on('click', 'a[rel="info_prod"]', function () {
        var tr = tblProd.cell($(this).closest('td, li')).index();
        var data = tblProd.row(tr.row).data();
        console.log(data);

        //$("#nProd").remove();
        $("#nProd").append( $("<h5 class='text-primary'><i class='fas fa-hashtag'></i> Codigo: "+data.id+"</h5>") );

        $("#nProd").append( $("<h5 class='text-primary'><i class='fas fa-print'></i> Producto: "+data.name+"</h5>") );
        
        $("#nProd").append( $("<h5 class='text-primary'><i class='fas fa-chevron-circle-up'></i> Existencia: "+data.nexistencia+"</h5>") );

        // $('.close').on('click', function () {
        //     //alert('aqui');
        //     $("#nProd").remove();
        // });
        $('#myModelDetCardex').on('hidden.bs.modal', function (e) {
           // $('#frmClient').trigger('reset');
           $("#nProd").empty();
          // $(this).removeData('bs.modal',null);
           
        });
        tblCardex = $('#tblDetCard').DataTable({
            // dom: 'Bfrtip',       
            // buttons:[ 
            //     {
            //         extend:    'excelHtml5',
            //         text:      '<i class="fas fa-file-excel"></i> ',
            //         titleAttr: 'Exportar a Excel',
            //         className: 'btn btn-success'
            //     },
            //     {
            //         extend:    'pdfHtml5',
            //         text:      '<i class="fas fa-file-pdf"></i> ',
            //         titleAttr: 'Exportar a PDF',
            //         className: 'btn btn-danger'
            //     },
            //     {
            //         extend:    'print',
            //         text:      '<i class="fa fa-print"></i> ',
            //         titleAttr: 'Imprimir',
            //         className: 'btn btn-info'
            //     },
            // ],   
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            //data: data.det,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_cardex',
                    'id': data.id
                },
                dataSrc: ""
            },
            columns: [
                {"data": "prod_tipo"},
                {"data": "prod_estado"},
                {"data": "prod_sale"},
                {"data": "prod_fecha"},
                {"data": "mov_ent"},
                {"data": "mov_sal"},
                {"data": "prod_costo"},
                {"data": "monto_ent"},
                {"data": "monto_sal"},
                {"data": "monto_imp"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if(row.prod_tipo === 'V'){
                            var importe = row.prod_cant*row.prod_costo;
                            importe *= -1;
                            return '<p class="text-success font-weight-bold">'+'$' + parseFloat(importe).toFixed(2)+'</p>';
                        }else if(row.prod_tipo === 'C'){
                            var importe = row.prod_cant*row.prod_costo;
                            //importe *= -1;
                            return '<p class="text-primary font-weight-bold">'+'$' + parseFloat(importe).toFixed(2)+'</p>';
                        }
                        //return '$' + parseFloat(0).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        // if(row.prod_tipo === 'V'){
                        //     var importe = row.prod_cant*row.prod_costo;
                        //     return '<p class="text-success font-weight-bold">'+'$'+ parseFloat(importe).toFixed(2) +'</p>' ;
                        // }
                        // return '<p class="text-secondary font-weight-bold">'+'$'+ parseFloat(0).toFixed(2) +'</p>';
                        return '<p class="text-success font-weight-bold">'+'$'+ parseFloat(data).toFixed(2) +'</p>' ;
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        // if(row.prod_tipo === 'C'){
                            
                        //     var importe = row.prod_cant*row.prod_costo;
                        //     return '<p class="text-primary font-weight-bold">'+'$' + parseFloat(importe).toFixed(2)+'</p>';
                        // }
                        // return '<p class="text-secondary font-weight-bold">'+'$'+ parseFloat(0).toFixed(2) +'</p>';
                        return '<p class="text-primary font-weight-bold">'+'$' + parseFloat(data).toFixed(2)+'</p>';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<p class="text-dark font-weight-bold">'+'$' + parseFloat(data).toFixed(2)+'</p>';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if(row.prod_tipo === 'V'){
                            return '<p class="text-success font-weight-bold">'+data+'</p>'
                        }
                        return '<p class="text-secondary font-weight-bold">'+0+'</p>'
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        if(row.prod_tipo === 'C'){
                            return '<p class="text-primary font-weight-bold">'+data+'</p>'
                        }
                        return '<p class="text-secondary font-weight-bold">'+0+'</p>'
                    }
                },
                {
                    targets: [-8],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<p class="font-weight-bold">'+data+'</p>';
                    }
                },
                {
                    targets: [-9],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<p class="font-weight-bold">'+data+'</p>';
                    }
                },
                {
                    targets: [-10],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<p class="font-weight-bold">'+data+'</p>';
                    }
                },
            ],
            initComplete: function (settings, json) {

            },
            "drawCallback":function(){
                //alert("cargando...");
                var api = this.api();
                $(api.column(4).footer()).html(
                    'Ent= '+parseFloat(api.column(4, {page:'current'}).data().sum()).toFixed(2)
                ),
                $(api.column(5).footer()).html(
                    'Sal= '+parseFloat(api.column(5, {page:'current'}).data().sum()).toFixed(2)
                ),
                $(api.column(7).footer()).html(
                    'T-Ent: $'+parseFloat(api.column(7, {page:'current'}).data().sum()).toFixed(2)
                ),
                $(api.column(8).footer()).html(
                    'T-Sal: $'+parseFloat(api.column(8, {page:'current'}).data().sum()).toFixed(2)
                ),
                $(api.column(9).footer()).html(
                    'Total: $'+parseFloat(api.column(9, {page:'current'}).data().sum()).toFixed(2)
                )
            }


        });

        $('#myModelDetCardex').modal('show');

    })
    .on('click', 'td.dt-control', function () {
        var tr = $(this).closest('tr');
        var row = tblProd.row(tr);
        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });

});
