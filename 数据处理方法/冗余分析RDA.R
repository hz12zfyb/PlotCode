library("vegan")
library(readxl)
library(ggplot2)
library(ggrepel)
sheetname = 'Sheetall'
environment_pre <- as.matrix(read_excel("D:/Refresh/data/CHINARE-36/cca_R/environment.xlsx",sheet = sheetname))
flage <- as.matrix(read_excel("D:/Refresh/data/CHINARE-36/cca_R/flage.xlsx",sheet = sheetname))

#rda
#a <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
#a <- c(1,2,3,4,5,15,16)
#environment = environment_pre[,a]
data.rda = rda(flage,environment_pre)
data.rda
plot(data.rda) #简易画�?
envfit(data.rda,environment,permutations = 999)
#cca
#data.cca <- cca(flage,environment)
#data.cca
#plot(data.cca) #简易画�?
#envfit(data.cca,environment,permutations = 999)
#permutest(data.rda,permutations = 999)

ii = summary(data.rda)
sp=as.data.frame(ii$species[,1:2])###提取相应变量坐标，乘�?5是使图美观，不影响分�?
st=as.data.frame(ii$sites[,1:2])###提取样方坐标，有两种模式，可根据自己数据探索：二选一即可
yz=as.data.frame(ii$biplot[,1:2])###提取解释变量坐标

#grp=as.data.frame( read_excel("D:/Refresh/data/CHINARE-35/cca_R/environment.xlsx",
#                             sheet = "Sheet_label",range = "A1:A37"))###对样方分�?
#colnames(grp)="group"###重命名列�?


ggplot() +
#  geom_point(data = st,aes(RDA1,RDA2,color=grp$group,fill=grp$group),size=2)+###此处修改
  geom_segment(data = sp,aes(x = 0, y = 0, xend = RDA1, yend = RDA2), 
               arrow = arrow(angle=22.5,length = unit(0.35,"cm"),
                             type = "closed"),linetype=1, size=0.6,colour = "red")+
  geom_text_repel(data = sp,aes(RDA1,RDA2,label=row.names(sp)))+
  geom_segment(data = yz,aes(x = 0, y = 0, xend = RDA1, yend = RDA2), 
               arrow = arrow(angle=22.5,length = unit(0.35,"cm"),
                             type = "closed"),linetype=1, size=0.6,colour = "blue")+
  geom_text_repel(data = yz,aes(RDA1,RDA2,label=row.names(yz)))+
  labs(x="RDA1  44.6%",y="RDA2  7.1%")+
  geom_hline(yintercept=0,linetype=3,size=1) + 
  geom_vline(xintercept=0,linetype=3,size=1)+
#  guides(shape=guide_legend(title=NULL),
#         fill=guide_legend(title=NULL))+###此处修改
  theme_bw()+theme(panel.grid=element_blank())
fig_name = paste(sheetname,".png")
ggsave(filename = fig_name,width = 12,height = 9)