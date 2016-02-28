$( "#searchForm" ).submit(addListings(event) {
  event.preventDefault();

  // Get values from elements on the page:
  var $form = $( this ),
    term = $form.find( "input[name='s']" ).val(),
    url = $form.attr( "action" );

  // Send the data using post
  var posting = $.post( url, { s: term } );

  // Put the results in a div
  posting.done(function( data ) {
    var content = $( data ).find( "#content" );
    $( "#result" ).append(
    '<div class="col-md-4"> Address: ' + listing.listing + '</div>' +

    '<div class="col-md-2"> Monthly Rent: ' + listing.Cost + '</div>' +

    '<div class="col-md-2"> Transit Time: ' + listing.travel_duration + '</div>' +

    '<div class="col-md-3"> Transit Details: You should travel by ' +  listing.best_travel_method + '. It will cost you ' + listing.cost_of_best_travel_method + '<br>' + listing.explanation + '</div>' + '<p> If you wanted to take Uber instead, it would cost you ' + listing.uber_premium_for_10_minutes + '</p>' + '</div>'

    '<div class="col-md-1"> Livability Index: ' + listing.Live + '</div>');
  });
});
