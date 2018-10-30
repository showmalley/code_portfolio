

### Sean O'Malley
### Ayaviri 2018 Med Mission

############ Start ############

### Packages

require(dplyr)
require(ggplot2)
require(beeswarm)
require(xlsxjars)
require(xlsx)
require(wordcloud)
require(slam)
require(tm)
require(RColorBrewer)

### Ingest

df <- read.csv("/Users/SeanOMalley1/AnacondaProjects/MedMissions/AY2018/AyaviriMaster2018.csv")

df <- df[1:1072,2:27]

### EDA

summary(df)

glimpse(df)

############ Clean ############

df$Day <- as.factor(df$Day)
df$edad <- as.numeric(df$edad)
df$diagnostico_3 <- as.factor(df$diagnostico.3)

# normalize consult text

levels(df$consultorio_1) <- tolower(levels(df$consultorio_1))
levels(df$consultorio_2) <- tolower(levels(df$consultorio_2))
levels(df$consultorio_3) <- tolower(levels(df$consultorio_3))

# normalize diagnostic text

levels(df$diagnostico_1) <- tolower(levels(df$diagnostico_1))
levels(df$diagnostico_2) <- tolower(levels(df$diagnostico_2))
levels(df$diagnostico_3) <- tolower(levels(df$diagnostico_3))
levels(df$diagnostico_4) <- tolower(levels(df$diagnostico_4))

# 1
df$count_1 <- as.character(df$count_1)
df$medicina_1 <- as.character(df$medicina_1)
df$medicina_1 <- ifelse(nchar(df$count_1) > 3, df$count_1, df$medicina_1)
df$count_1 <- ifelse(nchar(df$count_1) > 3, "0", df$count_1)
df$count_1 <- ifelse(is.na(df$count_1) == T, "0", df$count_1)
df$count_1 <- as.numeric(df$count_1)

# 2
df$count_2 <- as.character(df$count_2)
df$medicina_2 <- as.character(df$medicina_2)
df$medicina_2 <- ifelse(nchar(df$count_2) > 3, df$count_2, df$medicina_2)
df$count_2 <- ifelse(nchar(df$count_2) > 3, "0", df$count_2)
df$count_2 <- ifelse(is.na(df$count_2) == T, "0", df$count_2)
df$count_2 <- as.numeric(df$count_2)
# 3
df$count_3 <- as.character(df$count_3)
df$medicina_3 <- as.character(df$medicina_3)
df$medicina_3 <- ifelse(nchar(df$count_3) > 3, df$count_3, df$medicina_3)
df$count_3 <- ifelse(nchar(df$count_3) > 3, "0", df$count_3)
df$count_3 <- ifelse(is.na(df$count_3) == T, "0", df$count_3)
df$count_3 <- as.numeric(df$count_3)

# 4
df$count_4 <- as.character(df$count_4)
df$medicina_4 <- as.character(df$medicina_4)
df$medicina_4 <- ifelse(nchar(df$count_4) > 3, df$count_4, df$medicina_4)
df$count_4 <- ifelse(nchar(df$count_4) > 3, "0", df$count_4)
df$count_4 <- ifelse(is.na(df$count_4) == T, "0", df$count_4)
df$count_4 <- as.numeric(df$count_4)

# 5
df$count_5 <- as.character(df$count_5)
df$medicina_5 <- as.character(df$medicina_5)
df$medicina_5 <- ifelse(nchar(df$count_5) > 3, df$count_5, df$medicina_5)
df$count_5 <- ifelse(nchar(df$count_5) > 3, "0", df$count_5)
df$count_5 <- ifelse(is.na(df$count_5) == T, "0", df$count_5)
df$count_5 <- as.numeric(df$count_5)

# clean seguimiento

df$necesita.seguimiento <- as.character(df$necesita.seguimiento)
df$specialidad <- as.character(df$specialidad)
df$specialidad <- ifelse(nchar(df$necesita.seguimiento) > 2, df$necesita.seguimiento, df$specialidad)
df$necesita.seguimiento <- ifelse(nchar(df$necesita.seguimiento) > 1, "1", df$necesita.seguimiento)
df$necesita.seguimiento <- ifelse(is.na(df$necesita.seguimiento) == T, "0", df$necesita.seguimiento)
df$necesita.seguimiento <- as.factor(df$necesita.seguimiento)

# finalize df clean up

df <- df %>%
          select(Day,nombre,apellido,dni,edad,sexo,communidad,
                 consultorio_1,consultorio_2,consultorio_3,
                 diagnostico_1,diagnostico_2,diagnostico.3,diagnostico_4,
                 medicina_1,count_1,medicina_2,count_2,medicina_3,count_3,medicina_4,count_4,medicina_5,count_5,
                 necesita.seguimiento, specialidad) %>%
          unique() # remove duplicates

############ Create Subsets ############

### isolate medicines & counts

medicine_stack <- as.data.frame(mapply(c,select(df, medicina_1, count_1), select(df, medicina_2, count_2),
                                       select(df, medicina_3, count_3), select(df, medicina_4, count_4),
                                       select(df, medicina_5, count_5)))

names(medicine_stack) <- c("medicina","count")

medicine_stack <- medicine_stack %>% filter(is.na(medicina) == F)

medicine_stack$count <- as.numeric(medicine_stack$count)
levels(medicine_stack$medicina) <- tolower(levels(medicine_stack$medicina))

medicine_stack_sum <-  aggregate(medicine_stack$count, by=list(medicina=medicine_stack$medicina), FUN=sum)
names(medicine_stack_sum) <- c("medicina","count_sum")
medicine_stack_count <-  aggregate(medicine_stack$count, by=list(medicina=medicine_stack$medicina), FUN=NROW)
names(medicine_stack_count) <- c("medicina","n_perscribed")

medicine_stack_summary <- medicine_stack_sum %>% left_join(medicine_stack_count, by = c("medicina","medicina"))
medicine_stack_summary$count_sum[medicine_stack_summary$medicina == "acetaminophen 500mg pills"] <- 164*11

### isolate consults

consult_stack <-   df %>%
                        select(consultorio_1) %>%
                        rbind(list(df$consultorio_2)) %>%
                        rbind(list(df$consultorio_3))

names(consult_stack) = c("consultorio")
consult_stack <- consult_stack %>% filter(is.na(consultorio) == F)

consult_stack_summary <- c<-  aggregate(consult_stack$consultorio, by=list(consultorio=consult_stack$consultorio), FUN=NROW)
names(consult_stack_summary) = c("consultorio","consults")

### isolate diognostics

diagnostic_stack <-   df %>%
                      select(diagnostico_1) %>%
                      rbind(list(df$diagnostico_2)) %>%
                      rbind(list(df$diagnostico_3)) %>%
                      rbind(list(df$diagnostico_4))

names(diagnostic_stack) = c("diagnosis")
diagnostic_stack <- diagnostic_stack %>% filter(is.na(diagnosis) == F)

diagnostic_stack_summary <- c<-  aggregate(diagnostic_stack$diagnosis, by=list(diagnosis=diagnostic_stack$diagnosis), FUN=NROW)
names(diagnostic_stack_summary) = c("diagnosis","n_diagnosis")

### isolate sequimiento & specialty

seguimiento_stack <- df %>% 
                        select(necesita.seguimiento,specialidad) %>%
                        mutate(specialidad = as.factor(specialidad),
                               necesita.seguimiento = as.factor(necesita.seguimiento))


############ Place Results into XLSX ############

setwd("/Users/SeanOMalley1/AnacondaProjects/MedMissions/AY2018")

wb = createWorkbook()
sheet = createSheet(wb, "main")
addDataFrame(df, sheet=sheet, startColumn=1, row.names=FALSE)
sheet = createSheet(wb, "medicine_stack_summary")
addDataFrame(medicine_stack_summary, sheet=sheet, startColumn=1, row.names=FALSE)
sheet = createSheet(wb, "consult_stack")
addDataFrame(consult_stack, sheet=sheet, startColumn=1, row.names=FALSE)
sheet = createSheet(wb, "consult_stack_summary")
addDataFrame(consult_stack_summary, sheet=sheet, startColumn=1, row.names=FALSE)
sheet = createSheet(wb, "diagnostic_stack")
addDataFrame(diagnostic_stack, sheet=sheet, startColumn=1, row.names=FALSE)
sheet = createSheet(wb, "diagnostic_stack_summary")
addDataFrame(diagnostic_stack_summary, sheet=sheet, startColumn=1, row.names=FALSE)
sheet = createSheet(wb, "seguimiento_stack")
addDataFrame(seguimiento_stack, sheet=sheet, startColumn=1, row.names=FALSE)

############ Visualize ############

### Medical Mission Day to Day Patients

ggplot(df,aes(x = Day)) + 
      geom_bar(col = "darkgrey", alpha = 0.7, fill = "darkred") + 
      theme_minimal() 

### Community Representation

community <- aggregate(df$communidad, by=list(community_c=df$communidad), FUN=NROW)
community <- community %>% arrange(desc(x)) %>% filter(x>2)
names(community) <- c("community","count")

ggplot(community, aes(x = reorder(community, count), y = count)) + 
  geom_bar(stat = "identity", col = "darkgrey", alpha = 0.7, fill = "darkred") + 
  coord_flip() +
  theme_minimal()

### Consult Viz

ggplot(consult_stack_summary,aes(x = reorder(consultorio, consults), y = consults)) + 
      geom_bar(stat = "identity", col = "darkgrey", alpha = 0.7, fill = "darkred") + 
      coord_flip() +
      theme_minimal()

### Age and Gender Viz

beeswarm(edad ~ sexo, data=df, col=sample(colors(), 27), pch=19, method="swarm", cex=0.5)

### Top 25 Diagnosis Viz

diagnostic_stack_summary_viz <- diagnostic_stack_summary %>%
                                        arrange(desc(n_diagnosis)) %>%
                                        head(25)

ggplot(diagnostic_stack_summary_viz, aes(x = reorder(diagnosis, n_diagnosis), y = n_diagnosis)) + 
  geom_bar(stat = "identity", col = "darkgrey", alpha = 0.7, fill = "darkred") + 
  coord_flip() +
  theme_minimal()

### Medications Viz

medicine_stack_summary_viz <- medicine_stack_summary %>%
                                            arrange(desc(count_sum)) %>%
                                            head(25)

ggplot(medicine_stack_summary_viz,aes(x = reorder(medicina, count_sum), y = count_sum)) + 
    geom_bar(stat = "identity", col = "darkgrey", alpha = 0.7, fill = "darkred") + 
    coord_flip() +
    theme_minimal()

### Seguimiento Viz

seguimiento_stack_viz <- seguimiento_stack %>% filter(is.na(specialidad) == F)

seguimiento_stack_viz <-iconv(seguimiento_stack_viz$specialidad, to = "utf-8")

pal2 <- brewer.pal(10,"Dark2")
wordcloud(seguimiento_stack_viz, random.order=T, rot.per=.15, colors=pal2, vfont=c("sans serif","plain"))


############ Forecast Drug Needs ############

phm_inv <- read.xlsx("AyPharmacy2018.xlsx", sheetIndex = 3, StringsAsFactors = F)

head(phm_inv)

phm_inv$medicina <- paste(phm_inv$medicine,phm_inv$dose, sep = " ")
phm_inv$medicina <- paste(phm_inv$medicina,phm_inv$dose_unit, sep = "")
phm_inv$medicina <- paste(phm_inv$medicina,phm_inv$dose_type, sep = " ")

phm_inv$medicina <- as.character(tolower(phm_inv$medicina))
medicine_stack_summary$medicina <- as.character(medicine_stack_summary$medicina)

phm_full <- phm_inv %>%
                filter(is.na(medicine) == F) %>%
                select(box, medicina,med_count,expiration, box_count, extra_units, total.units) %>%
                full_join(medicine_stack_summary, by = c("medicina")) %>%
                mutate(amount_needed = ifelse((count_sum - total.units)>0,count_sum - total.units,0)) %>%
                rename(amount_used = count_sum, amount_storage = total.units)

phm_clean <- phm_full %>% select(box, medicina, amount_storage, amount_used, amount_needed)

# add sheet to dataframe
sheet = createSheet(wb, "phm_clean")
addDataFrame(phm_clean, sheet=sheet, startColumn=1, row.names=FALSE)

############ Determine Drug Cost ############

phm_cost <- read.xlsx("AyPharmacy2018.xlsx", sheetIndex = 2)

head(phm_cost)
glimpse(phm_cost)
summary(phm_cost)

# normalize
phm_cost$Medicine.Name.Full <- as.character(tolower(phm_cost$Medicine.Name.Full))

# clean naming
phm_cost <- phm_cost %>%
                  select(Category,Type_medicine,Medicine.Name.Full,Price_unit) %>%
                  rename(category = Category, type = Type_medicine,
                         medicina = Medicine.Name.Full, unit_price = Price_unit)

phm_final <- phm_cost %>%
                  full_join(phm_full, by = c("medicina"))

phm_final <- phm_final %>%
                  mutate(spend_per_drug = unit_price*amount_used)

phm_final$spend_per_drug <- ifelse(is.na(phm_final$spend_per_drug)==F,phm_final$spend_per_drug,0)

print(paste("recorded pharmacy cost in USD $", round(sum(phm_final$spend_per_drug)/3,2), sep = ""))

# add sheet to dataframe xlsx
sheet = createSheet(wb, "phm_final")
addDataFrame(phm_final, sheet=sheet, startColumn=1, row.names=FALSE)

saveWorkbook(wb, "AyaviriClean2018.xlsx")

############ Determine Per Patient Cost ############

# normalize medicines

df$medicina_1 <- tolower(df$medicina_1)
df$medicina_2 <- tolower(df$medicina_2)
df$medicina_3 <- tolower(df$medicina_3)
df$medicina_4 <- tolower(df$medicina_4)
df$medicina_5 <- tolower(df$medicina_5)


phm_minimal <- phm_final %>% select(category,type, medicina, unit_price)

# if med match do count * cost of that med    df$cost_1 <- ifelse()

head(phm_final)
head(df)

############ Forecast Doctor Needs ############





############ Model ############
