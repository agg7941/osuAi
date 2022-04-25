#!/bin/perl

use warnings;

$osud=$ARGV[0];
$osuf=$ARGV[1];
$ds=$ARGV[2];
$anno=$ARGV[3];

(split '/', `cd "$osud"; pwd`)[-1] =~ /(\d+)/;
$id=$1;
$dif=0;

$s='a';
$b=0; $e=0; $t=0;
$auf='0';

open $f, $osuf;
while(<$f>) {
	if($s eq 'a') {
		if(/AudioFilename:\ *([^\r]*)\r*/) { 
			$auf=$1; chomp $auf;
			@ls=split "\n", `cd "$osud"; ls -1`;
			foreach (@ls) {
				if(/(.*\Q$auf\E.*)/i) {
					$auf=$1; chomp $auf;
				}
			}
			$s='b';
		}
		next;
	} elsif($s eq 'b') {
		if(/BeatmapID:\ *(\d+)\r*/) {
			$dif=$1; chomp $dif;
			$s='t';
		}
		next;
	} elsif($s eq 't') {
		if(/\[TimingPoints\]/) {
			$s='f';
		}
		next;
	}

	print $_;
	if(m/^\ *\r*$/) { last }

	if($s eq 'f') {
		$t=(split ',', $_)[1];
		$s='s';
	} elsif($s eq 's') {
		$n=(split ',', $_)[1]; chomp $n;
		if($n > 0) {
			print "echo $t > \"$anno/$id-$dif-$b.bpm\"\n";
			system "echo $t > \"$anno/$id-$dif-$b.bpm\"";
			$t=$n;
		} else { next }
		$e=(split ',', $_)[0];
		print "ffmpeg -y -i \"$osud/$auf\" -ss ${b}ms -to ${e}ms -c:a copy \"$ds/$id-$dif-$b.mp3\"\n";
		system "ffmpeg -y -i \"$osud/$auf\" -ss ${b}ms -to ${e}ms -c:a copy \"$ds/$id-$dif-$b.mp3\"";
		$b=$e;
	}
}

print "echo $t > \"$anno/$id-$dif-$b.bpm\"\n";
system "echo $t > \"$anno/$id-$dif-$b.bpm\"";
print "ffmpeg -y -i \"$osud/$auf\" -ss ${b}ms -c:a copy \"$ds/$id-$dif-$b.mp3\"\n";
system "ffmpeg -y -i \"$osud/$auf\" -ss ${b}ms -c:a copy \"$ds/$id-$dif-$b.mp3\"";
