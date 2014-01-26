# 25 Jan
Make more stringent cutoff when comparing with SNAP, compare to less stringent.

Since 1kG data is deeper for the 4 populations, compare number of snps which would be missing when using a less complete test.
Prove that there are cases in which 1kG data would give positive results where HapMap results wouldn't.



# 23 Jan

Created a test script to make sure that the RSIDs and Block numbers in nomatch pairs match up correctly
Currently tests 30%, no reason it can't test all

Next step is to write a script to find if SNP2s associated to same SNP1 are associated with each other

Establish statistics
 - edit statistic cutoff
 
SNPs in DHS hapmap vs 1kg

# 22 Jan

In compareResults() need to make sure blocks are correctly associated with rsids, order in query is not necessarily order returned.
Putting results in dict with rsid as key and block number as value, edited if statements to correctly index

Still some errors with blocks and rsids being swapped. 
Error from unclosed brackets (oops)

For nomatch pairs:
Want to find sets of SNPs linked to SNP1 where my dataset says they are not linked and 1kg says they are



# 8 July


Edited recursion perl script to allow cycling through population within each chromosome. Writes size of each LD block to file, one block per line for import into python script for graphing.


Figured out weirdness with snps in stop codon but not in exon... maybe. Many are in exons, just weren’t included in total file for whatever reason.


Todo: Add export of per-population trees


# 10 July


    Recursion program:
        global variables for file handlers
                


  Issue where every LD block is only 1
    fixed... issue finding snp2 in chr22, non-existent in chr21
    chr21 issue gone


Output totals.txt file easily importable into R for graphing as histogram (<variable> <- read.table(<file>)
  very left-tailed, majority of LD blocks are 0-20 members large




# 11 July


~/Downloads/snp result.txt : file downloaded from 


NCBI help on SNP features https://www.ncbi.nlm.nih.gov/books/NBK44466/


Assumption for SNP in exon:
  if SNP implicated in STOP-loss, STOP-gain, missense, cds-synon, frameshift, cds-indel, 


Assumption for SNP in stop codon
  Function class is STOP-GAIN or STOP-loss




Next steps:


  Keep array of found SNPs?  
  Dictionary of SNPs: associate each rsid to LD block


  Find percentage of eQTLs in DH sites
  Distance of linked SNPs


  R script to graph data
  


# 12 July


  For Emily: add hashmap to code to create index/list of members of LD block


  Me: Find number of eQTLs in DHS
    make sure chromosome positions are same for both
    Go through each study, compare positions with different versions
Save RS numbers
select RS,chr,position from gtex,dhsp2 where chr=dhs chr and position>=dhs start and position<=dhs end group by RS into outfile "/tmp/eqtl in dhs2.txt";


LiftOver http://genome.sph.umich.edu/wiki/LiftOver#Lift dbSNP rs numbers


http://gvs.gs.washington.edu/GVSBatch137/






# 16 July


Gtex Tissue Sample 
Lymphoblastoid Assembly:GRCh37.p10 build:104.0
Liver GRCh37.p10 build:104.0
Brain Cerebellum GRCh37.p10 build:104.0
Brain Frontal Cortex GRCh37.p10 build:104.0
Brain Temporal Cortex GRCh37.p10 build:104.0
Brain Pons GRCh37.p10 build:104.0
Lymphoblastoid GRCh37.p10 build:104.0


GRCh37 is same as HG19(?) - yes


Sheffield et al, 2013 DHS mapped to hg19/GRCh37 (http://www.nature.com/nature/journal/v489/n7414/full/nature11232.html)


Find more DNase Hypersensitivity sites(?)


# 17 July


Starting perl script to find eQTLs associated with DHS.


Already have .txt of eQTLs directly within DHS.


Need to find if any SNPs from LD table are in DHS, and if any eQTLs are in LD with those.




Once Emily done with LD block index, make new table for those
        Columns: RSID , LD Block , Chromosome , Location , Population


Create new indexes on existing tables(?)
        LD.SNP1 pos
        LD.SNP2 pos


        dhsp2.dhs chr
        dhsp2.dhs start
        dhsp2.dhs end
        dhsp2.dhs id
  
# 18 July


Uploaded population LD maps.
Now using “update ld hash.pl” script to add coordinates and chromosome to each position.


After those uploaded, have Emily write a new script to calculate the distances of SNPs in the same LD block from each other. (Averages and stdev of range, too?)


Currently only Chr22 is uploaded (since is smallest and easiest to work with). Eventually we’d want to include uploading to the ld blocks table within the rec.pl script once we run through every chromosome.


# 19 July


Perl script not updating correctly
Running sql command:


update ld blocks,ld set ld blocks.location = (select SNP1 pos from ld where SNP1 rs = ld blocks.rsid limit 1) where ld blocks.chrom is null or ld blocks.location is null;


Sql command doesn’t work.


Modified rec Final.pl to include inserting rows into ld blocks
Uploads after hash is created


# 22 July


Modify rec Final.pl to insert row during recursive subroutine

Starting work on identifying eQTLs in DHS, including those linked to SNPs in DHS

Once done, crosscheck eQTL rsids with those in ld blocks to see if any eQTLs present and assigned an ld block number.


# 23 July


Script progress as of 7:30am: Chromosomes 1,10-19, and 2 uploaded


Script finished around 10am.
Script still running as of 1045, started on chr3 (still chr4-9 left).


12:24 - cluster lost connection to mysql database, stopped part way through chr3
Editing code to resume upload starting from chr3


Interesting to see if any populations have unique ld block members.


Instructed Emily to write script to return distances between adjacent SNPs in same block.


Will eventually use in R script to return average distances/size of blocks.
Distance between adjacent SNPs per block
Average per block
Average per chrom per population
Differences between populations
Distance between end SNPs of block
Average within population and chrom
Average compared to other populations in same chrom
        


Create index for each column on ld blocks.




# 24 July


Script finished, ld blocks updated.


Creating indexes via source script.


Started running snp in eqtl.pl script at 10:30, was still running around 3:30.
ld in dhs.txt output repeat values
fetchrow instead of fetchrow array at line 40 




# 25 July


0842: Running test of snp in eqtl.pl, only running for chr22.
Output of ld in dhs.txt containing rsids of SNPs not in DHS, need to test to make sure dhsid is being assigned.


Do not use while to get results from fetchrow, esp if only one result expected


ld in dhs.txt contains rsid of SNP in the ld table, dhsid of DHS in which SNP falls




Edit snp in eqtl.pl to remove finding eqtls in DHS (since that can be done with an sql query)




# 26 July


SQL query to find ld snps in dhs running longtemps.


Using an iPython session to find SNPs in dhs. (Used sql to output a list of dhs locations and snp locations)

```
	In [19]: for loc in ld dict.values():
	  loc = int(loc)
	  for start in dhs dict.keys():
	    if loc>=int(start):
	      if loc <= int(dhs dict.values()[dhs dict.keys().index(start)]):
	      print loc
```

ld dict{rsid => location}
dhs dict{dhs start => dhs end}


Found ld blocks has some duplicate entries within same population




Add gencode data to search for eQTLs in and near (~500bp) of TSS




# 30 July

Discovered on the 29th that the ld blocks table had been uploaded incorrectly:
ld number didn’t reset to 1 for different populations in the same chromosome, so Emily’s script wouldn’t work.


Reuploading taking about 2 days...


Once finished, Emily’s script will output 22x11 txt files. Each line corresponds to an ld block, and contains a distance array between consecutive SNPs in each block.


Will use these txt files to create histograms of distances between SNPs for each chromosome and group.


Before running script, put in way to skip blocks of size 1. insert NULL instead of values... $#array gives last index, not length!




# 1 Aug


Ran into some problems while initially running Emily’s script:
Main problem was using the same increment variable in nested for loops
Another was, for blocks of size 1, I was inserting the string “NULL”, which caused problems when importing into R for graphing


R:
  
Import data as table (file <- data.table(“path”))
Convert to matrix (matrix <- data.matrix(na.omit(file))
Remove 0 values (matrix[matrix == 0] <- NA)
hist(na.omit(matrix))
Add titles
Save as image




# 15 Aug


Back from vacation


First goal: run R scrip to generate pictures of each plots
        Using ggplot2 package to make and save histograms
        Update R from 2.15.2 to 3.0.1


# 26 Aug


Installed BEDTools, used intersect to find eQTLs in DHS’
In file intersect.txt, 6088 lines.


# 8 Sep


SNAP LD Blocks vs Ones I created
SNAP: https://www.broadinstitute.org/mpg/snap/ldsearch.php
* not all HapMap SNPs included
* Need .txt of unique RS numbers from CEU, YRI, CHBJPT
* Need files of ld blocks
* Compare ld block file to one generated by SNAP (use r-square cutoff)  


Cursory search showed matches, but different r-squred values for SNAP (most lower) than ones from HapMap.
1000Genomes vs HapMap




# 10 Sep


Interesting: some rsids in multiple ld blocks per population per chrom, check to make sure code will prevent this.


Otherwise 1000genomes data matching mostly to my blocks


When redoing recursive program, make it use seed rsids as SNP2 rs (find SNP1 rs for which rsid is SNP2 rs)


# 16 Sep


Fixed SNPs appearing in multiple LD blocks by saving each rsid to a .txt and greping to find if a subsequent SNP was already found.


Tested to find duplicates, none found after modified code.
Also ran recursion backwards in findrs1 sub.


Testing on chr22 now. It works! No duplicates. Next test with SNAP data.




# 22 Sep


Fixed ld blocks by writing each rsid to a .txt file and greping within perl to find subsequent snps. The back recursion subroutine also works.


Now writing each rsid to .txt and uploading to SNAP proxy search to pull their ld blocks.




# 21 Oct


Added column to gtex: in hapmap 
Stores boolean for if gtex rsid is in the hapmap ld dataset


93% of gtex snps are in ld data




# Winter break 


Use curl to send Post string to SNAP. Save ld pair data to file. 
Import file and see if each pair are in same or different blocks in my data. 
Save results to 3 files : match, nomatch, dne. 


Count match vs total over many different boot strap runs. Find average and std and do stats. 


1000 runs: [0.66458024331259213, 0.30047392086132024]


100 runs:

## Later on

Error in running script for 10,000 runs: if SNAP server is down, returns error message and script fails.

Added check for script: if fails, run again keeping place. If fails >100 times: quit for good.

# 6 Jan

Email from Killdevil saying my job was idle. Just because of time.sleep(10)
Stopped it early after it went through ~3500 loops.
Restarted this morning.

# 8 Jan
Idea: Take nomatch pairs and figure out why they don't match
Make new file for output: SNP1 \t block SNP2 \t block

Make separate import for connecting to database

# 14 Jan
Reduced sleep time to 1 second
Changed nomatch pairs to only save 10% of data

Use 
      
      with
	
when opening files (automatically closes outside of block)

http://effbot.org/pyref/with.htm

# 15 Jan

ld blocks database is not working.
Too many entries in block 0, which shouldn't exist.

Changing initial function while loop to loop over array instead of fetchrow results.
Changing how $LD number variable is incremented.

## Problem with nomatch pairs.txt

If rsid is in block 0, then it does not exist in my dataset for that particular population. Should go to dne.

# 18 Jan

Running code with time report to find how long different number of loops will take

# 20 Jan

Ideas for kd comp.py efficiency:

* Reduce number of sql queries
* Write fh in in compareResults() to list, loop over list instead of file

# 21 Jan
Created indexes on ld.blocks

Using Python's cProfile to measure running times.

In get random rsids, set maxblock values instead of having a query

Added fetchall for test rsids query return

