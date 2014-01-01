8 July


        Edited recursion perl script to allow cycling through population within each chromosome. Writes size of each LD block to file, one block per line for import into python script for graphing.


Figured out weirdness with snps in stop codon but not in exon... maybe. Many are in exons, just weren’t included in total file for whatever reason.


Todo: Add export of per-population trees


10 July


    Recursion program:
        global variables for file handlers
                


  Issue where every LD block is only 1
    fixed... issue finding snp2 in chr22, non-existent in chr21
    chr21 issue gone


Output totals.txt file easily importable into R for graphing as histogram (<variable> <- read.table(<file>)
  very left-tailed, majority of LD blocks are 0-20 members large




11 July


~/Downloads/snp_result.txt : file downloaded from 


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
  


12 July


  For Emily: add hashmap to code to create index/list of members of LD block


  Me: Find number of eQTLs in DHS
    make sure chromosome positions are same for both
    Go through each study, compare positions with different versions
Save RS numbers
select RS,chr,position from gtex,dhsp2 where chr=dhs_chr and position>=dhs_start and position<=dhs_end group by RS into outfile "/tmp/eqtl_in_dhs2.txt";


LiftOver http://genome.sph.umich.edu/wiki/LiftOver#Lift_dbSNP_rs_numbers


http://gvs.gs.washington.edu/GVSBatch137/






16 July


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


17 July


Starting perl script to find eQTLs associated with DHS.


Already have .txt of eQTLs directly within DHS.


Need to find if any SNPs from LD table are in DHS, and if any eQTLs are in LD with those.




Once Emily done with LD block index, make new table for those
        Columns: RSID , LD Block , Chromosome , Location , Population


Create new indexes on existing tables(?)
        LD.SNP1_pos
        LD.SNP2_pos


        dhsp2.dhs_chr
        dhsp2.dhs_start
        dhsp2.dhs_end
        dhsp2.dhs_id
  
18 July


Uploaded population LD maps.
Now using “update_ld_hash.pl” script to add coordinates and chromosome to each position.


After those uploaded, have Emily write a new script to calculate the distances of SNPs in the same LD block from each other. (Averages and stdev of range, too?)


Currently only Chr22 is uploaded (since is smallest and easiest to work with). Eventually we’d want to include uploading to the ld_blocks table within the rec.pl script once we run through every chromosome.














19 July


Perl script not updating correctly
Running sql command:


update ld_blocks,ld set ld_blocks.location = (select SNP1_pos from ld where SNP1_rs = ld_blocks.rsid limit 1) where ld_blocks.chrom is null or ld_blocks.location is null;


Sql command doesn’t work.


Modified rec_Final.pl to include inserting rows into ld_blocks
        Uploads after hash is created


22 July


Modify rec_Final.pl to insert row during recursive subroutine




Starting work on identifying eQTLs in DHS, including those linked to SNPs in DHS


Once done, crosscheck eQTL rsids with those in ld_blocks to see if any eQTLs present and assigned an ld block number.


23 July


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
        


Create index for each column on ld_blocks.




24 July


Script finished, ld_blocks updated.


Creating indexes via source script.


Started running snp_in_eqtl.pl script at 10:30, was still running around 3:30.
ld_in_dhs.txt output repeat values
        fetchrow instead of fetchrow_array at line 40 




25 July


0842: Running test of snp_in_eqtl.pl, only running for chr22.
        Output of ld_in_dhs.txt containing rsids of SNPs not in DHS, need to test to make sure dhsid is being assigned.


Do not use while to get results from fetchrow, esp if only one result expected


ld_in_dhs.txt contains rsid of SNP in the ld table, dhsid of DHS in which SNP falls




Edit snp_in_eqtl.pl to remove finding eqtls in DHS (since that can be done with an sql query)




26 July


SQL query to find ld snps in dhs running longtemps.


Using an iPython session to find SNPs in dhs. (Used sql to output a list of dhs locations and snp locations)
In [19]: for loc in ld_dict.values():
    loc = int(loc)
    for start in dhs_dict.keys():
        if loc>=int(start):
            if loc <= int(dhs_dict.values()[dhs_dict.keys().index(start)]):
                print loc


ld_dict{rsid => location}
dhs_dict{dhs_start => dhs_end}


Found ld_blocks has some duplicate entries within same population




Add gencode data to search for eQTLs in and near (~500bp) of TSS




30 July


Discovered on the 29th that the ld_blocks table had been uploaded incorrectly:
ld_number didn’t reset to 1 for different populations in the same chromosome, so Emily’s script wouldn’t work.


Reuploading taking about 2 days...


Once finished, Emily’s script will output 22x11 txt files. Each line corresponds to an ld block, and contains a distance array between consecutive SNPs in each block.


Will use these txt files to create histograms of distances between SNPs for each chromosome and group.


----Before running script, put in way to skip blocks of size 1. insert NULL instead of values... $#array gives last index, not length!




1 Aug


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




15 Aug


Back from vacation


First goal: run R scrip to generate pictures of each plots
        Using ggplot2 package to make and save histograms
        Update R from 2.15.2 to 3.0.1


26 Aug


Installed BEDTools, used intersect to find eQTLs in DHS’
  In file intersect.txt, 6088 lines.


8 Sep


SNAP LD Blocks vs Ones I created
        SNAP: https://www.broadinstitute.org/mpg/snap/ldsearch.php
                -not all HapMap SNPs included
                -Need .txt of unique RS numbers from CEU, YRI, CHBJPT
                -Need files of ld blocks
                -Compare ld block file to one generated by SNAP (use r-square cutoff)


        Cursory search showed matches, but different r-squred values for SNAP (most lower) than ones from HapMap.
        1000Genomes vs HapMap




10 Sep


Interesting: some rsids in multiple ld_blocks per population per chrom, check to make sure code will prevent this.


Otherwise 1000genomes data matching mostly to my blocks


When redoing recursive program, make it use seed rsids as SNP2_rs (find SNP1_rs for which rsid is SNP2_rs)


16 Sep


Fixed SNPs appearing in multiple LD blocks by saving each rsid to a .txt and greping to find if a subsequent SNP was already found.


Tested to find duplicates, none found after modified code.
Also ran recursion backwards in findrs1 sub.


Testing on chr22 now. It works! No duplicates. Next test with SNAP data.




22 Sep


Fixed ld blocks by writing each rsid to a .txt file and greping within perl to find subsequent snps. The back recursion subroutine also works.


Now writing each rsid to .txt and uploading to SNAP proxy search to pull their ld blocks.




21 Oct


Added column to gtex: in_hapmap 
Stores boolean for if gtex rsid is in the hapmap ld dataset


93% of gtex snps are in ld data




Winter break 


Use curl to send Post string to SNAP. Save ld pair data to file. 
Import file and see if each pair are in same or different blocks in my data. 
Save results to 3 files : match, nomatch, dne. 


Count match vs total over many different boot strap runs. Find average and std and do stats. 


1000 runs: [0.66458024331259213, 0.30047392086132024]


100 runs: