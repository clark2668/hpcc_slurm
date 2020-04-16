#!/usr/bin/perl

use strict;
use warnings;

my ($sec,$min,$hour,$day,$month,$year,$wday,$yday,$isdst) = localtime(time);

$month += 1;
$year += 1900;

mkdir("./$year\_$month\_$day");

my $cmd = "sacctmgr -n -p show association where account=deyoungbuyin";
my $cmd_rtn_raw = `$cmd`;
my @rtn_lines = split(/\n/, $cmd_rtn_raw);
foreach my $rtn_line (sort @rtn_lines) {
    my @line_items = split(/\|/, $rtn_line);
    my $user = $line_items[2];
    if($user ne '') {
	print "$user\n";
	my $cmd_out = `sacct -p -n -S 2020-04-09 -u $user --format="User,JobID,jobname,state,ElapsedRaw,ncpus,Reqgres,Start" | grep "gpu" | grep "COMPLETED" | grep "glidein" >> ./$year\_$month\_$day/log_$year\_$month\_$day\_$user.txt`;
    }
}
