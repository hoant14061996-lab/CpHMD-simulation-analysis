#!/usr/bin/perl
# Jana K. Shen and Jason A. Wallace
# University of Oklahoma
# July 2009

# compute pKa values using HH or generalized HH equation
# cptpKa.pl [name] [.sx file 1] [.sx file 2]...
#           name = name of protein or project
# output: all.pka (if multiple titration data points are given)
#         file.pka (if only one titration data point is given)

sub usage {
	   printf STDERR "Usage : cptpKa.pl [name] [.sx file 1] [.sx file 2]\n";
	   printf STDERR "                  [name] = name of protein or project\n";
           exit 1;
}


if(!$ARGV[0]){
      &usage();
}

while (@ARGV) {
    if ($ARGV[0] eq "-help" || $ARGV[0] eq "-h") {
       &usage();
    }
    $file = shift @ARGV;
    push (@files, $file); 
}

$name = shift @files;
$nfile = @files;

print "Total number of .sx files is $nfile\n";
system "rm -f $name-res-*.dat $name-res-*.fit";

# For only .sx, pKa is calculated using HH equation
# S = 1/(1+10^(pka-pH))

if ($nfile == 1){
    $nres = 0; 
    $oldres = 0;
    open INP, "<$file";
    $pKaFile = $file; $pKaFile =~ s/\.sx/\.pka/;
    if (-e "$pKaFile") {system "rm -f $pKaFile";}
    open (OUT,">>$pKaFile");

    while (<INP>) {
        (/#/) && (next);
        @L = split(/\s+/,$_); 
        ($L[0] !~ /\d/) && (shift @L);
        ($L[1] == $oldres) && (next);
        $nres++;
        $resnum = $L[1]; $pH = $L[2]; $S = $L[3]; $oldres = $L[1];

	if (($S < 0.01) || ($S > 0.99)) {
	    printf OUT "%4d NAN\n", $resnum;
	    next;
	}

        $S = 1/$S - 1;
        $pKa = $pH + log($S)/log(10);
        printf OUT "%4d %5.2f 1.0\n", $resnum, $pKa;
    }
    print "Total number of titrating residues is $nres\n";
    exit;
}

# If there are two or more .sx files, 
# we first collect S values at different pH for each titrating residue

foreach $file (@files) {
    $nres = 0; 
    $oldres = 0;
    open INP, "<$file";

    while (<INP>) {
        (/#/) && (next);
        @L = split(/\s+/,$_); 
        ($L[0] !~ /\d/) && (shift @L);
        ($L[1] == $oldres) && (next);
        $nres++;
        $resnum = $L[1]; $pH = $L[2]; $S = $L[3]; $oldres = $L[1];
        $ires[$nres] = $resnum;
        $outf = "$name-res-$resnum.dat";
        open (OUT, ">>$outf");
        printf OUT  "%4.1f  %5.2f\n", $pH, $S;
    }
}
close OUT;
print "Total number of titrating residues is $nres\n";

# Prepare Xmgrace template file for fitting to generalized HH equation
# S = 1/(1+10^(n*(pka-pH)))

if (-e "xmgrace_template") {system "rm -f xmgrace_template";}
open (OUT, ">> xmgrace_template");
print OUT 'fit formula "y = 1/(1 + 10^( a0*(a1-x)))"';
print OUT "\nfit with 2 parameters";
print OUT "\nfit prec 0.001";
print OUT "\na0 = 1.0\na0 constraints on";
print OUT "\na0min = 0.1\na0max = 2.0\n";
print OUT "\na1 = 4.0\na1 constraints on";
print OUT "\na1min = 0\na1max = 14\nnonlfit (s0, 5)\n";
close OUT;

# Compute pKa's using Xmgrace fitting

for ($nn=1; $nn <= $nres; $nn++) {
    $resnum = $ires[$nn];
    system "xmgrace -hardcopy $name-res-$resnum.dat -batch xmgrace_template > $name-res-$resnum.fit";
    system "rm -f $name-res-$resnum.ps";
    system "cancel -a";
}

# Make gnuplots for S vs pH with the fitted curve and data points
# We first prepare a gnuplot template for plotting 

if (-e "gnuplot_template") {system "rm -f gnuplot_template";}
open (OUT, ">> gnuplot_template");
print OUT "set terminal png\n";
print OUT "set output 'NAME.png'; set title 'NAME' font 'Arial-Bold,14' textcolor rgb 'blue'; set pointsize 2.5\n"; 
print OUT "set xlabel 'pH' font 'Arial-Bold,14' textcolor rgb 'blue'; set xtics font 'Arial-Bold,14' textcolor rgb 'blue'; set ylabel 'S' font 'Arial-Bold,14' textcolor rgb 'blue';set ytics font 'Arial-Bold,14' textcolor rgb 'blue'; set xrange [0:14]; set yrange [-.1:1.1]\n";
print OUT "set key right bottom\n";
print OUT "plot 'NAME.dat' ti 'data' pt 2, 1 / (1 + 10**(HILL*(PKA-x))) ti 'fit'\n";
close OUT;

# Write out pKa values in a file and make gnuplot plots

if (-e "$name.pka") {system "rm -f $name.pka"};
open (OUT, ">>$name.pka");

for ($nn=1; $nn <= $nres; $nn++) {
    $resnum = $ires[$nn];
    open INP, "< $name-res-$resnum.fit";
    $fit = 0;
    while (<INP>) {
        if (/Computed values/) {$fit = 1; next;}
        if ($fit == 1) {
            if (/a1 = /) {
                @L = split(/\s+/,$_); ($L[0] !~ /\w/) && (shift @L);
                $pka = $L[2]; print "res $resnum pka $pka\n";
            }        
            if (/a0 = /) {
                @L = split(/\s+/,$_); ($L[0] !~ /\w/) && (shift @L);
                $hill = $L[2]; print "res $resnum hill $hill\n";
            }
        }
        if (/Correlation/) {
        @L = split(/\s+/,$_); ($L[0] !~ /\w/) && (shift @L);
        $correl = $L[2]; print "res $resnum correlation $correl\n";print "\n";
        }
    }
    printf OUT  "%4d  %5.2f  %5.2f  %5.2f\n", $resnum, $pka, $hill, $correl;
    system "sed s/NAME/$name-res-$resnum/g gnuplot_template | sed s/HILL/$hill/ | sed s/PKA/$pka/ > $name-gnuplot";
    system "gnuplot $name-gnuplot";
}
system "rm -f $name-gnuplot gnuplot_template xmgrace_template";

exit;
