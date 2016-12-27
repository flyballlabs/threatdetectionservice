$("#panel2").hide();
$("#panel3").hide();

$('#newaccount').click(function() {
  $("#panel1").hide();
  $("#panel2").show();
});

$('#demo').click(function() {
  $("#panel1").hide();
  $("#panel3").show();
});