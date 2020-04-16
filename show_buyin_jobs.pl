#!/usr/bin/perl

use strict;
use warnings;

if(!defined($ARGV[0])) {
    print "Usage: show_buyin_users.pl <buyin_name>\n";
    exit;
}

my $buyin = $ARGV[0];

my $cmd = "sacctmgr -n -p show association where account=$buyin";

my $cmd_rtn_raw = `$cmd`;

my @rtn_lines = split(/\n/, $cmd_rtn_raw);

foreach my $rtn_line (sort @rtn_lines) {

    my @line_items = split(/\|/, $rtn_line);

    my $user = $line_items[2];

    if($user ne '') {
	print "$user\n";

	print "Jobs:\n";

	my $cmd_out = `squeue -h -u $user --format="%u %A %N %T %P %b %p %Q"`;

	my @cmd_out_lines = split(/\n/, $cmd_out);

	my $count = 1;
	foreach my $line (@cmd_out_lines) {
	    print "$count: $line\n";
	    $count++;
	}
	print "\n";
    }
}
