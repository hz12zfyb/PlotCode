library(mgcv)
library(readxl)
library(car)
library(ggplot2)
## 导入数据
dat = read_excel("D:/Refresh/data/GAMM/environment_AS.xlsx",sheet = "Sheet2")
dat$NP = dat$NO3/dat$PO4
dat$NSI = dat$NO3/dat$Si 
dat$SIP = dat$Si/dat$PO4
## 多重共线性 VIF检验,去除vif>5或10 的变量（至少留一个）
pigment_name = 'Hex-Fuco'
vif_test <- lm(hex~lon+lat+mld+par+depth+Si+NP,data = dat)
vif(vif_test)
#去除零值
#dat = dat[which(dat[pigment_name]>0),]
dat$Fuco = dat$Fuco + 0.01
dat$hex = dat$hex + 0.01
dat$Allo = dat$Allo + 0.01
dat$Peri = dat$Peri +0.01
dat$Lut = dat$Lut +0.01
## 对数转换
dat$depth1000 <- dat$BotDepth/1000
dat$chla <- log(dat$chla)
dat$Fuco <- log(dat$Fuco)
dat$hex <- log(dat$hex)
dat$Allo <- log(dat$Allo)
dat$Peri = log(dat$Peri)
dat$Lut = log(dat$Lut)

dat$fMonth <- as.factor(dat$month)

lmc <- lmeControl(niterEM = 520000, msMaxIter = 520000)
formula1<-formula(hex~s(lon,lat,k=8)
                  +s(chla,bs='cr',k=8)
                  +te(Temperature,Salinity,k=c(8,8))+s(NSI,bs='cr',k=8)
                  +s(depth1000,bs='cr',k=8)
                  +s(par,bs='cr',k=8))
gamm8<-gamm(formula1,
            random=list(HPLC=~1), #不同HPLC仪器测量带来的随机误差
            method='REML',
            data=dat, control=lmc,
            weights=varIdent(form=~1|fMonth))

x_value = 'Salinity'
y_value = 'Temperature'
vis.gam(gamm8$gam, view=c(x_value,y_value),
        plot.type="contour",color="topo",
        xlab=x_value,ylab=y_value,
        n.grid = 500,too.far =  1,#500为佳
        main = pigment_name)
save(gamm8,file="gamm8_hex_AS.rda",compress = 'xz')
#输出结果
a <- c('')
arr <- array(0:0, dim=c(dim(dat)[1],10))
for (i in array(0:10)){
    predict_dat = data.frame(lon = dat$lon,
                             lat = dat$lat,
                             chla = dat$chla,
                             Temperature = dat$Temperature + i/10,
                             NSI = dat$NSI,
                             Salinity = dat$Salinity ,
                             depth1000 = dat$depth1000,
                             par = dat$par)
    p0 = predict(gamm8$gam,predict_dat)
    arr[,i] = exp(p0)
    a <- c(a,list(mean(exp(p0))))}
z = data.frame(T = a)
write.csv(arr,'D:/Refresh/data/GAMM/result_hex_t+0-1_AS.csv')

###输出模型结果
z = data.frame(g8_fp = gamm8[["gam"]][["fitted.values"]]
               )
write.csv(z,'D:/Refresh/data/GAMM/result.csv')

#保存gamm结果
save(gamm8,file="gamm8.rda",compress = 'xz')
load("gamm_fuco.rda")



