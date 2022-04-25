#!/bin/perl

use warnings;
use strict;

my $BEATMAPS="../beatmaps";
my $WD=`pwd`; chomp $WD;
my $DS="$WD/$ARGV[0]";
my $ANNO="$WD/$ARGV[1]";
my $c='/home/poi/proj/osuAi/directionalCNN/parseBeatmap.pl';

chdir $BEATMAPS;
my $d=`ls -d1 */`; chomp $d;
my @lst = split '\n', $d;

foreach (@lst) {
	print "$_\n";
	chdir "$WD/$BEATMAPS/$_";
	my $osuf=`ls -1 | grep osu`; chomp $osuf;
	print "perl $c . $osuf $DS $ANNO\n";
	system('perl', $c, '.', "$osuf", "$DS", "$ANNO");
}
