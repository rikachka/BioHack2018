#!/usr/bin/env Rscript

# запуск через терминал "Rscript --vanilla repfilter.R input.faa input.rep output.txt"
options(repos = c(CRAN = "https://cran.rstudio.com")) # без этой опции из командной строки не работает, т.к. пользуется внешним пакетом
args = commandArgs(trailingOnly=TRUE)
if("seqinr" %in% rownames(installed.packages()) == FALSE) {install.packages(c("ade4", "seqinr"))}
library("seqinr") # подключает пакет, в котором пользуется read.fasta()

vogs_with_anno_and_vq <- read.table("vogs_with_anno_and_vq.txt") # берет таблицу с размеченными VOGами из VOG_filter.R
vogs_with_anno_and_vq <- vogs_with_anno_and_vq[vogs_with_anno_and_vq$Viral.Quotient>0.85,] # отсеивает слишком похожих на бактерию

fasta <- read.fasta(args[1]) # читает фасту, в питоне это делается какой-то из функций пакета biopython
protein_names <- as.data.frame(names(fasta)) # достает последовательность названий белков
colnames(protein_names) <- "query name"
protein_names$ID <- seq.int(nrow(protein_names)) # раздаю всем ID, потому что функция merge() беспощадно всех перемешивает

# это костыль, который приводит названия белков к единому стилю
# проблема кроется в HMMERе, который выводит accession gene_2|GeneMark.hmm|263_aa|-|1029|1820 если заголовок в fasta
# имел вид >gene_2|GeneMark.hmm|263_aa|-|1029|1820	>NC_002947.4 Pseudomonas putida KT2440 chromosome, complete genome
# а вот с названиями белков типа >NC_004088.1 проблем нет
if (grepl(".*>.*", protein_names$`query name`[1])==T){
  protein_names$`query name` <- gsub("(.*)>(.*)", "\\1", protein_names$`query name`)
  protein_names$`query name` <- gsub('[\r\n\t]', '', protein_names$`query name`)
}

rep <- read.table(args[2])[,c(1,3,5)] # читает file.rep
colnames(rep) <- c("target name",  "query name", "E-value")

# делает left join. к строкам таблицы rep добавляется информация про VOGи (если они есть)
rep_w_anno <- merge(rep, vogs_with_anno_and_vq, by.x = "target name", by.y = "VOG.number", all.x=T)[,c(1,2,3,11,14)]

proteins_sequence <- unique(rep$`query name`) # создает последовательность из белков, у которых есть VOGи
filtered_data <- rep_w_anno[0,] # сюда пойдет выход функции
# берет лучшие VOGи, т.к. с белками обычно совпадает несколько. отсеивает по E-value
for (i in proteins_sequence){
  x <- rep_w_anno[rep_w_anno$`query name`== i,] # в каждой итерации проверяется выборка строк про один и тот же белок
  # если E-value > 10^3 или у всех отсутствует VQ (мало ли), берет VOG с наименьшим E-value и заменяет название VOGа на "bacterial protein"
  if ((all(x$'E-value'>1e-3)) | (all(is.na(x$Viral.Quotient)==T))) {
    x <- x[x$'E-value'==min(x$`E-value`),]
    x[,1] <- "bacterial_protein"
    filtered_data <- rbind(filtered_data, x[1,]) # x[1,] потому что бывают и одинаковые E-value)
  }
  # если же с E-value и VQ все хорошо, то
  #   если хотя бы в одно значение в столбце коротких аннотаций не пустое, 
  #     то берет из отобранных по наличию аннотаций VOGов тот, у которого меньше E-value
  #   если аннотаций ни у кого нет, то просто берет VOG с наименьшим E-value 
  else {
    # если у белка нет короткой аннотации
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

# outer join таблицы с названиями белков и таблицы из предыдущей функции 
filtered_data <- merge(protein_names, filtered_data, by='query name', all=T)
filtered_data$`target name` <- as.character(filtered_data$`target name`)
filtered_data[is.na(filtered_data$`target name`)==T,]$'target name' <- "bacterial_protein" # заполняет все образовавшиеся NA осмысленным названием
filtered_data$`target name` <- as.factor(filtered_data$`target name`)
filtered_data <- filtered_data[order(filtered_data$ID),] # упорядочивает перемешанную таблицу по заранее созданному ID

target_vector <- filtered_data[,c(1,2,3)] # достает выборку столбцов
colnames(target_vector) <- c("query_name",	"ID", "target_name")

write.table(target_vector, file=args[3])
