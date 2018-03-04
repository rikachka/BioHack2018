#!/usr/bin/env Rscript
options(repos = c(CRAN = "https://cran.rstudio.com"))
args = commandArgs(trailingOnly=TRUE)
if("seqinr" %in% rownames(installed.packages()) == FALSE) {install.packages(c("ade4", "seqinr"))}
library("seqinr")

vogs_with_anno_and_vq <- read.table("vogs_with_anno_and_vq.txt")
vogs_with_anno_and_vq <- vogs_with_anno_and_vq[vogs_with_anno_and_vq$Viral.Quotient>0.85,]

fasta <- read.fasta(args[1])
protein_names <- as.data.frame(names(fasta))
colnames(protein_names) <- "query name"
protein_names$ID <- seq.int(nrow(protein_names))

if (grepl(".*>.*", protein_names$`query name`[1])==T){
  protein_names$`query name` <- gsub("(.*)>(.*)", "\\1", protein_names$`query name`)
  protein_names$`query name` <- gsub('[\r\n\t]', '', protein_names$`query name`)
}

rep <- read.table(args[2])[,c(1,3,5)]
colnames(rep) <- c("target name",  "query name", "E-value")

rep_w_anno <- merge(rep, vogs_with_anno_and_vq, by.x = "target name", by.y = "VOG.number", all.x=T)[,c(1,2,3,11,14)]

proteins_sequence <- unique(rep$`query name`)
filtered_data <- rep_w_anno[0,]
for (i in proteins_sequence){
  x <- rep_w_anno[rep_w_anno$`query name`== i,]
  if ((all(x$'E-value'>1e-3)) | (all(is.na(x$Viral.Quotient)==T))) {
    x <- x[x$'E-value'==min(x$`E-value`),]
    x[,1] <- "bacterial_protein"
    filtered_data <- rbind(filtered_data, x[1,])
  }
  else {
    if (any(is.na(x$Short.Annotations)==F)) {
      x <- x[x$`E-value`==min(x[is.na(x$Short.Annotations)==F,]$'E-value'),]
      x[,1] <- x[,4]
      filtered_data <- rbind(filtered_data, x[1,])
    }
    else {
        x <- x[x$'E-value'==min(x$`E-value`),]
        x[,1] <- "VOG"
        filtered_data <- rbind(filtered_data, x[1,])
    }
  }
}

filtered_data <- merge(protein_names, filtered_data, by='query name', all=T)
filtered_data$`target name` <- as.character(filtered_data$`target name`)
filtered_data[is.na(filtered_data$`target name`)==T,]$'target name' <- "bacterial_protein"
filtered_data$`target name` <- as.factor(filtered_data$`target name`)
filtered_data <- filtered_data[order(filtered_data$ID),]

target_vector <- filtered_data[,c(1,2,3)]
colnames(target_vector) <- c("query_name",	"ID", "target_name")

output_filename <- gsub("(.*)\\.(.*)","\\1",args[1])
write.table(target_vector, file=args[3])
