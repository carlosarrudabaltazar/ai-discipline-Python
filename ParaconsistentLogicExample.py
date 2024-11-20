from ParaAnalyzer import CreateDataBase
from ParaAnalyzer import LPA2v
from ParaAnalyzer import MPD
from ParaAnalyzer import QUPCLPA2v
from ParaAnalyzer import QUPCMPD

createdb = CreateDataBase("teste")
createdb.ReadDataBaseFromCSV("./database.csv",';')
lpa = LPA2v(createdb)
lpa.CalculateDecision(["S3","S1","S2","S3","S1","S2","S3","S1"])
print("LPA2v = |Gcer: "+ str(lpa.decision.gCer) +" & GUnc: "+ str(lpa.decision.gUnc) +"| => "+ lpa.decision.lowDefinitionState)
qupc = QUPCLPA2v(lpa,"./","LPA2v")
qupc.WriteQUPC()

mpd = MPD(createdb)
mpd.CalculateDecision(["S3","S1","S2","S3","S1","S2","S3","S1"])
print("MPD = |Gcer: "+ str(mpd.decision.gCer) +" & GUnc: "+ str(mpd.decision.gUnc) +"| => "+ mpd.decision.lowDefinitionState)
qupc = QUPCMPD(mpd,"./","MPD")
qupc.WriteQUPC()