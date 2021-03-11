#load packages
library(tidyverse)
library(scales)

##load data
treaty_tags<-read.csv("\treaty_tags .csv", header = TRUE, stringAsFactors=FALSE)

#recoding errors
treaty_tags<-treaty_tags%>%mutate("multilateral? (YN)"=recode("multilateral? (YN)",
                                                              "IO"="Y"))%>%
                         mutate("precision 1 (Y/N)"=recode("Precision 1 (Y/N)",
                                     "n"="N"))%>%
                       mutate("precision 4 (y/N)"=recode("Precision 4 (y/N)",
                                    "17"="Y", "y"="Y", "Y?"="Y", "n"="N"))%>%
                      mutate("obligation 1 (Y/N)"=recode("obligation 1 (Y/N)",
                                    "y"="Y", "Y?"="Y"))%>%
                  mutate("obligation 5 (Y/N)"=recode("obligation 5 (Y/N)",
                                    "M"="N", "y"="Y", "Y?"="Y", "n"="N"))%>%
                mutate("delegation 1 (Y/N)"=recode("delegation 1 (Y/N)",
                                     "M"="N", "n"="N"))%>%
            mutate("delegation 2 (Y/N)"=recode("delegation 2 (Y/N)",
                                   "n"="N"))%>%
          mutate("delegation 3 (Y/N)"=recode("delegation 3 (Y/N)",
                                     "n"="N", "y"="Y"))%>%
          mutate(recode("N/A"="NaN"))

#rescale values
treaty_tags<-treaty_tags%>%mutate("precision 2 (1-4)", rescale("precision 2 (1-4)", to =c(0.25:1)))%>%
  mutate("obligation 5 (1-5)", rescale("obligation (1-5)", to =c(0.2:1)))

  
  
 
  

