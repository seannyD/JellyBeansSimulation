setwd("~/Documents/MPI/JellyBeans/pyBeans/")

d = read.table("experSettings_Sort_PunishGap.txt",sep=',',header=TRUE)

d$totMoney = apply(d[,c('money1','money2')],1,sum)

# Only look at punish gap results
d = d[d$full_full==-1,]

getMeanMoney = function(x,y,data=d){
	m = d[sum(c(d$s1,d$s2) %in% c(x,y))==2,c('money1','money2')]
	
}

levs = as.character(levels(factor(d$s1)))

# get rid of sorted-first strategies
#levs = levs[!levs %in% grep("_SORT",levs,value=TRUE)]

mat = matrix(nrow=length(levs),ncol=length(levs))
for(i in 1:length(levs)){
	for(j in 1:length(levs)){
		ix = levs[i]
		jx = levs[j]
		mat[i,j] = mean(d[(d$s1==ix & d$s2==jx) | (d$s1==jx & d$s2==ix),]$totMoney)
	}
}

#par(mar=c(12,12,4,2))
#image(mat,xaxt='n',yaxt='n')
#axis(1,at=(0:(length(levs)-1))/(length(levs)-1),labels=levs,las=2)
#axis(2,at=(0:(length(levs)-1))/(length(levs)-1),labels=levs,las=2)

totalScores = tapply(d[d$s1 %in% levs & d$s2 %in% levs,]$totMoney,d[d$s1 %in% levs & d$s2 %in% levs,]$s1,sum)+tapply(d[d$s1 %in% levs & d$s2 %in% levs,]$totMoney,d[d$s1 %in% levs & d$s2 %in% levs,]$s2,sum)
totalScores = totalScores[!is.na(totalScores)]
totalScores[order(totalScores)]

mat.sorted = mat[order(totalScores),order(totalScores)]
par(mar=c(12,12,4,2))
image(mat.sorted,xaxt='n',yaxt='n')
axis(1,at=(0:(length(levs)-1))/(length(levs)-1),labels=levs[order(totalScores)],las=2)
axis(2,at=(0:(length(levs)-1))/(length(levs)-1),labels=levs[order(totalScores)],las=2)




##########################

levs = as.character(levels(factor(d$s1)))
mat.self = matrix(nrow=length(levs),ncol=length(levs))
for(i in 1:length(levs)){
	for(j in 1:length(levs)){
		ix = levs[i]
		jx = levs[j]
		mat.self[i,j] = mean(c(d[(d$s1==ix & d$s2==jx),]$money1,d[(d$s2==ix & d$s1==jx),]$money2)) 
	}
}

totalScores = tapply(d$money1,d$s1,sum)+tapply(d$money2,d$s2,sum)
totalScores[order(totalScores)]

mat.self.sorted = mat.self[order(totalScores),order(totalScores)]
par(mar=c(12,12,4,2))
image(mat.self.sorted,xaxt='n',yaxt='n')
axis(1,at=(0:(length(levs)-1))/(length(levs)-1),labels=levs[order(totalScores)],las=2)
axis(2,at=(0:(length(levs)-1))/(length(levs)-1),labels=levs[order(totalScores)],las=2)