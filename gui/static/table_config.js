//Editable Table With Ajax 
    $('#demo2').html( '<table class="ui table segment" id="example3"></table>' );
    $('#example3').dataTable( {
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": false,
        "bInfo": false,
        "aaData": [
            /* Reduced data set */
            [ "John", "Approved", "None" ],
            [ "Jamie", "Approved", "None" ],
            [ "Jill", "Denied", "Requests Call" ]
        ],
        "aoColumns": [
            { "sTitle": "Name" },
            { "sTitle": "Status" },
            { "sTitle": "Notes" }
        ]
    });

    var oTable2 = $('#example3').dataTable({
        "bRetrieve": true,
        "bPaginate": false,
        "bLengthChange": false,
        "bFilter": false,
        "bInfo": false
    });
     
    // Apply the jEditable handlers to the table 
    oTable2.$('td').editable( '', {
        "callback": function( sValue, y ) {
            var aPos = oTable2.fnGetPosition( this );
            oTable2.fnUpdate( sValue, aPos[0], aPos[1] );
        },
        "submitdata": function ( value, settings ) {
            return {
                "row_id": this.parentNode.getAttribute('id'),
                "column": oTable2.fnGetPosition( this )[2]
            };
        }
    });
  
    $('<tfoot><tr><th colspan="3" width="100%">Click on the the table cels to edit them. Click on the Column Header to sort.</th></tr></tfoot>').appendTo("#example3");
    
    $('<i class="sort icon"></i>').appendTo("#example3 thead th");
    