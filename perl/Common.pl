use strict;

sub existInList {
	# desc: a element exists in a list or not 
	# usage: if(existInList("A",@aList))
	# return: 1 or 0
	
	my ($element, @list) = @_;
	foreach my $ele (@list) {
		if($ele eq $element) { 
			return 1;
		}
	}
	return 0;
}

sub indexOfList {
	# desc: a element exists in a list or not 
	# usage: indexOfList("A", @aList)
	# return: -1 : not existing, >= 0 : in the list
	
	use List::MoreUtils qw(firstidx);
	my ($element, @list) = @_;
	return (firstidx { $_ eq $element } @list);
}

