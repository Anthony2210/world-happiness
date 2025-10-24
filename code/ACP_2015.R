# ACP

require(FactoMineR)
library(ggplot2)

data <- "C:/Users/antoc/world-happiness/data/raw/world_happiness_2015.csv"
df <- read.csv(data, header = TRUE, sep = ";", dec = ",", stringsAsFactors = FALSE)

# On enlève les colonnes non utilisées dans l’ACP (identifiants + score global)
no_var <- c("Ranking", "Country", "Regional.indicator", "Happiness.score")
pays <- df$Country
X <- df[, !(names(df) %in% no_var), drop = FALSE]
X <- as.data.frame(lapply(X, function(x) as.numeric(as.character(x))))
rownames(X) <- pays
X <- X[complete.cases(X), , drop = FALSE]

n<-nrow(X)
p<-ncol(X)

head(X)
head(n)
head(p)

res <- PCA(X, scale.unit = TRUE, ncp = ncol(X), graph = FALSE)

X<-as.matrix(X)
moy<-apply(X,2,mean)
ecartype<-apply(X,2,sd) *sqrt((n-1)/n) 

ecartype

Z<-scale(X,center=moy,scale=ecartype)
apply(Z,2,mean)
apply(Z,2,sd)*sqrt((n-1)/n)


###### Calcul de la matrice des corrélations ######

N<-diag(rep(1/n,n)) # matrice des poids des individus (1/n pour chacun)
R<-t(Z)%*%N%*%Z # matrice de corrélation des p variables

#Vérification R = t(Z)%*%N%*%Z est la matrice de corrélation
round(R,3)

round(cor(X),3)

corrplot(as.matrix(R)) # représentation graphique de la matrice de corrélation

###### Décomposition spectrale avec la fonction eigen() ######
e<-eigen(R)

#valeurs propres lambda_1, ...
lambda<-e$values
sum(lambda) #Vérif sum(lambda_i)=3

#matrice des vecteurs propres v_1, v_2, ... (en colonne)
V <- e$vectors

sum(V[,1]*V[,2])

round(t(V)%*%V, 3) # t(V) %*% V #Vérif : les vecteurs propres sont bien orhonormés (=I_3)

###### Matrice des coordonnées factorielles des individus 
##(des scores F = ZMV, avec M = Id )######

F<-Z%*%V

apply(F,2,mean) #verification de la nullité des moyennes

apply(F,2,var)*(n-1)/n #verif même valeurs que evalues ci-après
lambda

pc1 <- 100 * lambda[1] / sum(lambda)
pc2 <- 100 * lambda[2] / sum(lambda)
pc3 <- 100 * lambda[3] / sum(lambda)

# cos**2 sur les plans
cos2_12 <- rowSums(F[, 1:2]^2) / rowSums(F^2)
cos2_23 <- rowSums(F[, 2:3]^2) / rowSums(F^2)

# on prend les 25 meilleurs (tester à 15/30 selon lisibilité)
k <- 15
lab12 <- names(sort(cos2_12, decreasing = TRUE))[1:k]
lab23 <- names(sort(cos2_23, decreasing = TRUE))[1:k]

par(mfrow = c(1, 2))

## Plan (1,2)
plot(F[,1], F[,2],
     xlab = sprintf("Dim 1 (%.1f%%)", pc1),
     ylab = sprintf("Dim 2 (%.1f%%)", pc2),
     main = "Individus - plan (1,2)",
     pch = 16, cex = 0.6)
abline(h = 0, v = 0, lty = 3)
# labels uniquement pour les mieux projetés
text(F[lab12,1], F[lab12,2], labels = lab12, pos = 3, cex = 0.7)

## Plan (2,3)
plot(F[,2], F[,3],
     xlab = sprintf("Dim 2 (%.1f%%)", pc2),
     ylab = sprintf("Dim 3 (%.1f%%)", pc3),
     main = "Individus - plan (2,3)",
     pch = 16, cex = 0.6)
abline(h = 0, v = 0, lty = 3)
text(F[lab23,2], F[lab23,3], labels = lab23, pos = 3, cex = 0.7)

res<-prcomp(X,center=TRUE,scale=ecartype)
res<-prcomp(X,center=TRUE,scale=TRUE)
res$sdev^2 #racines des valeurs propres donc au carré. 

res$x

res<-princomp(X,cor=TRUE)
res$sdev^2 #racines des valeurs propres donc au carré. 

res$scores

res<-PCA(X)

res$eig

res$ind

res$ind$coord

# ---------- pas fini ----------

# % d’inertie expliquée
perc <- 100 * lambda / sum(lambda)
perc_cum <- cumsum(perc)

barplot(lambda, main = "Éboulis des valeurs propres", xlab = "Composantes", ylab = "Valeur propre")





