$('#searchForm').submit(addListings);

$(function addListings(){
	var $listings = $('#listings');

	$.ajax({
		type: 'POST',
		url:
		success: function(listings) {
			$.each(listings, function(i, listing) {
				$listings.append('<li> Address: ' + listing.street + '<br>' + listing.city + ', ' + list.state + ', ' + listing.zip + '<br>' + 'Monthly Rent: ' + listing.cost + '<br>' + 'Bedrooms: ' + listing.bed + '<br>' + 'Baths: ' + listing.bath + '<br>' + 'Livability Index: ' + listing.live + '</li>');
			});
		}
	});
});
