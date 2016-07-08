#############################################
########PROJECTE POSTGRAU DATASCIENCE########
#############################################

#Llibreries

library(ggplot2)
library(lubridate)
library(lme4)
library(dplyr)
library(locfit)

#Lectura de dades

setwd("C:/Users/usuario/Desktop/POSTGRAU_DATA_SCIENCE/PROJECTE_POSTGRAU/R")
dades <- read.csv("C:/Users/usuario/Desktop/POSTGRAU_DATA_SCIENCE/PROJECTE_POSTGRAU/data.csv")


#Manipulació de dades
#creem el ID
dades$Id_bitllet <- as.factor(paste(dades$ID_Vuelo, dades$fecha_salida, dades$hora_salida, dades$fecha_llegada, dades$hora_llegada, sep = '/'))
length(levels(dades$Id_bitllet))
dades$Id_bitllet <- as.numeric(dades$Id_bitllet)
length(unique(dades$Id_bitllet))

#filtratge
dades$dias_antelacion <- dades$dias_antelacion*-1
dades$fecha_salida_dia_setmana <- weekdays(as.Date(dades$fecha_salida))
dades$fecha_llegada_dia_setmana <- weekdays(as.Date(dades$fecha_llegada))
dades$dia_query_dia_setmana <- weekdays(as.Date(dades$dia_query))
dades$demanda<-as.factor(dades$demanda)
dades$p_adultos <- dades$p_ninos <- dades$divisa <- dades$p_viejos <- dades$p_bebes_brazos <- dades$p_bebes_sentados <- NULL
dades <- subset(dades, tipo_cabina == 'COACH')
dades <- subset(dades, aerolinia%in%levels(dades$aerolinia)[c(5,6,11,4)]) #només ens quedem aquestes aerolinies
length(unique(dades$Id_bitllet))

#dades
dades <- dades[,c("ID_Vuelo", "Id_bitllet", "dia_query", "dia_query_dia_setmana", "dias_antelacion", "aerolinia", 
                  "nombre_ciudad_origen", "nombre_ciudad_destino", "precio", "fecha_salida", "fecha_salida_dia_setmana", 
                  "hora_salida", "fecha_llegada", "fecha_llegada_dia_setmana","hora_llegada", "duracion", "demanda")]
names(dades)

#Creació variables

dades <- dades[order(dades$dias_antelacion),]
dades <- dades[order(dades$Id_bitllet),]
dades$baixada_preu <- as.factor(as.numeric(unlist(tapply(dades$precio, dades$Id_bitllet, FUN = function(y) cummin(y[length(y):1])[length(y):1]==y))))

#write.csv(dades, "dades_4_07_2016.csv")
