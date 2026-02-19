#!/usr/bin/perl

# Compute fractional of time in unprotonation state S_i^{unprot}
# = N_i^u/N_i^u + N_i^p
# tautomer information contained in the file
# 0 for single titration site; 2 for HSP, 4 for ASP/GLU
# Usage: CptSX.pl [file] [start] [end] [pH]

sub usage {
   printf STDERR "Usage: CptSX.pl [file] [start] [end] [pH]\n";
   exit 1;
}
		    

if(!$ARGV[0]){
   &usage()
}

while ($#ARGV>=0) {
    if ($ARGV[0] eq "-help" || $ARGV[0] eq "-h") {
    &usage();
    }
    $file = shift @ARGV;
    $start = shift @ARGV;
    $end = shift @ARGV;
    $pH = shift @ARGV;
    }

open (INFILE,"$file");
open (OUTFILE,">$file-$start-$end.sx");

$lam_p = 0.2;
$lam_up = 1-$lam_p;
$ititr = 0;
$iline = 0;
$Nframe =0;

while (<INFILE>) {
  @lambda = split(" ",$_);
  if ($lambda[0] =~ /#/) {
    if ($lambda[1] =~ /ires/) {
      shift @lambda;
      @ires = @lambda;
    }
    if ($lambda[1] =~ /itauto/) {
      shift @lambda;
      @iTauto = @lambda;
      $Ntitr = @iTauto -1; # $iTauto[0]=itaut
      for ($i=1; $i <= $Ntitr; $i++) {
	$Nunprot[$i] = 0; $Nprot[$i] = 0; $Nmix[$i] = 0;
      }
    }
  }
  else {
    $iline ++;
    if ($iline <= $end && $iline >=$start) {
      $Nframe ++;
      $ititr = 0;
      if ($lambda[0] !~ /\./) {
        shift @lambda;
      }
      foreach $lam(@lambda) {
	$ititr ++;
	$LamVal[$ititr] = $lam;
	# pure
	if ($lam >= $lam_up) {$Nunprot[$ititr] ++;}
	if ($lam <= $lam_p) {$Nprot[$ititr] ++;}
	# mixed
	if ($lam < $lam_up && $lam > $lam_p) {
	  $Nmix[$ititr] ++;
	  # hsp: unprotonated state needs to be pure tautomer
	  if ($iTauto[$ititr] == 2 && $LamVal[$ititr-1] > $lam_up) {
	    $Nunprot[$ititr-1] = $Nunprot[$ititr-1]-1;
	    $Nmix[$ititr-1] ++;
	  }
	  if ($iTauto[$ititr] == 2 && $LamVal[$ititr-1] < $lam_p) {
	    $Nprot[$ititr-1] = $Nprot[$ititr-1]-1;
	    $Nmix[$ititr-1] ++;
	  }
	  # asp: protonated state needs to be pure tautomer
	  if ($iTauto[$ititr] == 4 && $LamVal[$ititr-1] < $lam_p ){
	    $Nprot[$ititr-1] = $Nprot[$ititr-1]-1;
	    $Nmix[$ititr-1] ++;
	  }
	  if ($iTauto[$ititr] == 4 && $LamVal[$ititr-1] > $lam_up ){
	    $Nunprot[$ititr-1] = $Nunprot[$ititr-1]-1;
	    $Nmix[$ititr-1] ++;
	  }
	} # mixed
      } # each lambda
    } # if within start and end
  } # lambda lines
} # while

printf "pH %4d frames %8d totres %4d\n", $pH, $Nframe, $Ntitr;
printf OUTFILE "  # %5s %6s %6s %6s %6s\n",
"ires", "pH", "unprot", "pure", "mixed",;

# compute fraction of time in unprot states
for ($i=1; $i <= $Ntitr; $i++) {
    print "grp $i Nunprot $Nunprot[$i] Nprot $Nprot[$i] mixed $Nmix[$i]\n";
    $S[$i] = $Nunprot[$i] + $Nprot[$i];
    $PurePercent[$i] = $S[$i]/$Nframe;
    $MixPercent[$i] = $Nmix[$i]/$Nframe;
    if ($S[$i] > 0) {
	$S[$i] = $Nunprot[$i]/$S[$i];
	print "s= $S[$i]\n";
  }
  else {
    $S[$i] = -1;
  }
  printf OUTFILE "%3d %5d %6.1f %6.2f %6.2f %6.2f\n",
    $i, $ires[$i], $pH, $S[$i], $PurePercent[$i], $MixPercent[$i];
}
